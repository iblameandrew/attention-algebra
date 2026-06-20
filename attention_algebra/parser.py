"""Lightweight validator for Cognitive Algebra expressions.

The full grammar is prompt-specified; this module provides programmatic
well-typedness checks for terminals, complementarity pairs, and common
operator constraints.  It is intentionally conservative — it flags
likely errors but does not attempt full parsing of nested RNA structures.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

TERMINALS = frozenset({"Se", "Si", "Ne", "Ni", "Te", "Ti", "Fe", "Fi"})

PERCEPTION = frozenset({"Se", "Si", "Ne", "Ni"})
JUDGMENT = frozenset({"Te", "Ti", "Fe", "Fi"})

SENSING = frozenset({"Se", "Si"})
INTUITION = frozenset({"Ne", "Ni"})
THINKING = frozenset({"Te", "Ti"})
FEELING = frozenset({"Fe", "Fi"})

ATTITUDE_PAIRS: dict[str, str] = {
    "Se": "Si",
    "Si": "Se",
    "Ne": "Ni",
    "Ni": "Ne",
    "Te": "Ti",
    "Ti": "Te",
    "Fe": "Fi",
    "Fi": "Fe",
}

CROSS_AXIS_PAIRS: dict[str, str] = {
    "Se": "Ni",
    "Ni": "Se",
    "Si": "Ne",
    "Ne": "Si",
    "Te": "Fi",
    "Fi": "Te",
    "Ti": "Fe",
    "Fe": "Ti",
}

TERMINAL_RE = re.compile(r"(?<![A-Za-z])(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)(?![A-Za-z])")


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    terminals: list[tuple[str, int | None]] = field(default_factory=list)


def _domain(term: str) -> str:
    if term in PERCEPTION:
        return "perception"
    if term in JUDGMENT:
        return "judgment"
    return "unknown"


def _sub_axis(term: str) -> str:
    if term in SENSING:
        return "sensing"
    if term in INTUITION:
        return "intuition"
    if term in {"Te", "Ti"}:
        return "thinking"
    if term in {"Fe", "Fi"}:
        return "feeling"
    return "unknown"


def _attitude(term: str) -> str:
    return "extraverted" if term[1] == "e" else "introverted"


def are_complementary(a: str, b: str) -> bool:
    """Return True if ``a`` and ``b`` form a valid stem pair under Regime A or B."""
    return ATTITUDE_PAIRS.get(a) == b or CROSS_AXIS_PAIRS.get(a) == b


def extract_terminals(expr: str) -> list[tuple[str, int | None]]:
    """Return ``(terminal, mass)`` tuples in left-to-right order."""
    found: list[tuple[str, int | None]] = []
    for match in TERMINAL_RE.finditer(expr):
        mass_str, term = match.groups()
        mass = int(mass_str) if mass_str else None
        found.append((term, mass))
    return found


def validate_expression(expr: str) -> ValidationResult:
    """Validate a Cognitive Algebra expression string."""
    errors: list[str] = []
    warnings: list[str] = []

    if not expr or not expr.strip():
        return ValidationResult(False, ["Expression is empty"])

    expr = expr.strip()
    terminals = extract_terminals(expr)

    if not terminals:
        errors.append("No recognised terminals (Se, Si, Ne, Ni, Te, Ti, Fe, Fi) found")
        return ValidationResult(False, errors, warnings, terminals)

    for term, mass in terminals:
        if mass is not None and not (1 <= mass <= 10):
            warnings.append(f"Mass {mass} on {term} is outside documented range 1-10")

    # Orbit: look for X ~ Y patterns with two adjacent terminals
    for match in re.finditer(
        r"(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)\s*~\s*(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)",
        expr,
    ):
        left, right = match.group(2), match.group(4)
        if _domain(left) == _domain(right):
            errors.append(f"Orbit `~` requires Perception + Judgment, got {left} ~ {right}")

    # Opposition
    for match in re.finditer(
        r"(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)\s*oo\s*(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)",
        expr,
    ):
        left, right = match.group(2), match.group(4)
        if _sub_axis(left) != _sub_axis(right):
            errors.append(f"Opposition `oo` requires same sub-axis, got {left} oo {right}")
        elif _attitude(left) == _attitude(right):
            errors.append(f"Opposition `oo` requires opposite attitude, got {left} oo {right}")

    # Axis switch |
    for match in re.finditer(
        r"(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)\s*\|\s*(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)",
        expr,
    ):
        left, right = match.group(2), match.group(4)
        if _domain(left) != _domain(right):
            errors.append(f"Axis switch `|` requires same domain, got {left} | {right}")
        elif _sub_axis(left) == _sub_axis(right):
            errors.append(f"Axis switch `|` requires different sub-axis, got {left} | {right}")

    # Ambiguous `+`: domain switch (P+J) vs conjunction (any)
    switch_expr = re.sub(r"fold\[[^\]]*\]", "", expr)
    for match in re.finditer(
        r"(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)\s*\+\s*(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)",
        switch_expr,
    ):
        left, right = match.group(2), match.group(4)
        if _domain(left) != _domain(right):
            pass  # valid domain switch
        elif _sub_axis(left) == _sub_axis(right):
            warnings.append(
                f"`{left} + {right}` may be conjunction; prefer `&` for linear sums"
            )

    # Stem pairs ::
    for match in re.finditer(
        r"(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)\s*::\s*(\d+)?(Se|Si|Ne|Ni|Te|Ti|Fe|Fi)",
        expr,
    ):
        left, right = match.group(2), match.group(4)
        if not are_complementary(left, right):
            errors.append(f"Stem pair `::` requires complementary terminals, got {left} :: {right}")

    # Drag must not target a parenthesised group
    if re.search(r"->\s*\(", expr) or re.search(r"→\s*\(", expr):
        errors.append("Drag `->` right-hand side must be a single function, not a group")

    return ValidationResult(len(errors) == 0, errors, warnings, terminals)