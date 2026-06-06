"""Layer 2 — the Harmonic Composer.

Reads the Cognitive-Algebra expression emitted by Layer 1 and maps it
into a **Mathematical Schedule**: a JSON document that pairs every
cognitive function with a concrete optimisation objective, a weight
(mass), and a global frequency (acceleration).  The schedule is the
machine-readable contract that Layer 3 turns into executable PyTorch
code.

A handful of operators in the grammar are translated into distinct
*scheduling logics*:

* ``~`` (orbit)        → Orbital
* ``→`` / ``->`` (drag) → Drag
* ``|`` (switching)     → Stochastic Switching
* ``oo`` (opposition)   → Adversarial
* ``+`` (linear)        → Linear
"""

import json
import re

from langchain_core.prompts import PromptTemplate

from .config import ModelFactory
from .utils import strip_think_tags

# Keep the prompt as a regular string.  PromptTemplate substitutes
# {algebra} once; everything else is preserved verbatim — including
# the LaTeX braces, which are not escaped.
COMPOSER_SYSTEM_PROMPT = """
You are a Mathematical Physicist and Harmonic Composer for a Computational Psychology engine.
Your task is to translate a "Cognitive Algebra" expression into a "Mathematical Schedule" of optimization objectives for a Reinforcement Learning agent.

### MAPPING LOGIC (Cognitive -> Mathematical):

1. **Functions to Objectives**:
   - **Se (Extroverted Sensing)** -> `ExplorationObjective`   | Math: $\\mathcal{H}(\\pi(a|s))$ (Maximize Entropy)
   - **Si (Introverted Sensing)** -> `GatheringObjective`    | Math: $e^{-||s - \\mu||}$ (Minimize Distance to Centroid)
   - **Ne (Extroverted Intuition)** -> `ExtrapolationObjective` | Math: $e^{||s - \\mu||}$ (Maximize Distance / Novelty)
   - **Ni (Introverted Intuition)** -> `InterpolationObjective` | Math: $\\text{proj}_{\\vec{v}}(s)$ (Trajectory Alignment)
   - **Te (Extroverted Thinking)** -> `ExploitationObjective` | Math: $\\mathbb{E}[V(s)]$ (Maximize Value)
   - **Ti (Introverted Thinking)** -> `ContrastObjective`    | Math: $|d(s, a) - d(s, b)|$ (Maximize Discrimination)
   - **Fe (Extroverted Feeling)** -> `IntegrationObjective`  | Math: $\\mathcal{H} + \\alpha V(s)$ (Balance Entropy & Value)
   - **Fi (Introverted Feeling)** -> `SelectionObjective`    | Math: $e^{-d(s, s_{t-1})}$ (Temporal Consistency)

2. **Operators to Scheduling Logic**:
   - **Orbit (`~`)**       -> "Orbital".  The weights of the functions oscillate using Sine/Cosine waves.
   - **Drag (`→` or `->`)** -> "Drag".  The first function decays exponentially, the second grows.
   - **Switching (`|`)**   -> "Stochastic Switching".  Objectives toggle on/off based on probability.
   - **Opposition (`oo`)** -> "Adversarial".  Both objectives are active, but the secondary has a negative weight.
   - **Standard (`+`)**    -> "Linear".  Constant weights.

3. **Physics (Coefficients)**:
   - **Mass** (a bare integer prefix attached directly to a function, e.g. `5Si`): becomes the `weight` of the objective.
   - **Acceleration** (an integer prefix applied to a parenthesised group, e.g. `40(...)`): becomes the `global_frequency` of the interaction.

### TASK:
Analyze the Input Algebra.  Return a JSON object describing the "Score".

**Input Algebra**: {algebra}

### OUTPUT FORMAT (Strict JSON):
{{
    "original_expression": "{algebra}",
    "schedule_logic": "Orbital" | "Drag" | "Stochastic Switching" | "Linear" | "Adversarial",
    "global_frequency": <float from acceleration coefficient, default 1.0>,
    "score": [
        {{
            "voice": "Voice 1 (Function Name)",
            "symbol": "ObjectiveClassName",
            "mass": <float>,
            "formula": "LaTeX string",
            "description": "Brief physics description"
        }},
        ...
    ],
    "math_narrative": "A short sentence describing the mathematical interaction (e.g., 'Entropy maximization oscillating against temporal consistency')."
}}
"""


_FENCE_RE = re.compile(r"^\s*```(?:json)?\s*\n?(.*?)\n?\s*```\s*$", re.DOTALL)


def _extract_json(text: str) -> str:
    """Return the JSON body from an LLM reply, stripping ```json fences."""
    match = _FENCE_RE.match(text)
    if match:
        return match.group(1).strip()
    return text.strip()


class Composer:
    """Turn a Cognitive-Algebra expression into a Mathematical Schedule."""

    def __init__(self, model_name: str = "llama3", temperature: float = 0.2):
        # Strict JSON adherence requires low temperature.  Anything above
        # ~0.3 routinely produces broken JSON on smaller local models.
        self.llm = ModelFactory.get_model(
            model_name=model_name, temperature=temperature
        )
        self.prompt = PromptTemplate(
            template=COMPOSER_SYSTEM_PROMPT,
            input_variables=["algebra"],
        )
        self.chain = self.prompt | self.llm

    def compose(self, algebra_str: str):
        """Run the LLM chain and return a parsed dict (or an error dict)."""
        raw_output = self.chain.invoke({"algebra": algebra_str}).content
        raw_output = strip_think_tags(raw_output)
        return self._parse_json_safely(raw_output)

    @staticmethod
    def _parse_json_safely(text: str):
        """Parse ``text`` as JSON, returning an error-dict on failure."""
        cleaned = _extract_json(text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            return {
                "original_expression": "Error parsing",
                "schedule_logic": "Linear",
                "global_frequency": 1.0,
                "score": [],
                "math_narrative": f"Error: {exc}",
                "raw_output": cleaned,
            }

    @staticmethod
    def format_latex_report(composition: dict) -> str:
        """Render a Mathematical Schedule as a Markdown/LaTeX report."""
        logic = composition.get("schedule_logic", "Linear")
        narrative = composition.get("math_narrative", "")
        freq = composition.get("global_frequency", 1.0)
        score = composition.get("score", [])

        report = f"### Cognitive Schedule: **{logic}**\n"
        report += f"*{narrative}* (Global Accel: $\\omega={freq}$)\n\n"

        report += "| Function | Objective Class | Math Form | Mass ($m$) |\n"
        report += "| :--- | :--- | :--- | :---: |\n"

        for track in score:
            # Escape pipes in latex for markdown table compatibility.
            clean_formula = track["formula"].replace("|", "\\|")
            report += (
                f"| {track['voice']} | `{track['symbol']}` | "
                f"${clean_formula}$ | {track['mass']} |\n"
            )

        report += "\n**Intercalation Dynamics:**\n"

        # Master equation generation.  Each branch handles the empty
        # `score` case to avoid emitting invalid LaTeX such as
        # `J(θ) = ∫ () dt`.
        terms = []
        if logic == "Orbital":
            for i, track in enumerate(score):
                trig = "\\sin" if i % 2 == 0 else "\\cos"
                terms.append(
                    f"{track['mass']} \\cdot {trig}(\\omega t) "
                    f"\\cdot [{track['formula']}]"
                )
            eq = " + ".join(terms)
            report += f"$$ J(\\theta) = \\sum_{{t}} ({eq}) $$" if eq else ""

        elif logic == "Drag":
            if score:
                t0 = score[0]
                terms.append(
                    f"({t0['mass']} \\cdot e^{{-\\lambda t}}) \\cdot [{t0['formula']}]"
                )
                for track in score[1:]:
                    terms.append(
                        f"({track['mass']} \\cdot (1 - e^{{-\\lambda t}})) "
                        f"\\cdot [{track['formula']}]"
                    )
                eq = " + ".join(terms)
                report += f"$$ J(\\theta) = \\int ({eq}) dt $$"

        elif logic == "Adversarial":
            if score:
                terms.append(f"{score[0]['mass']} \\cdot [{score[0]['formula']}]")
                for track in score[1:]:
                    terms.append(f" - {track['mass']} \\cdot [{track['formula']}]")
                eq = "".join(terms)
                report += f"$$ J(\\theta) = \\max_\\pi ({eq}) $$"

        else:  # Linear / default
            for track in score:
                terms.append(f"{track['mass']} \\cdot [{track['formula']}]")
            eq = " + ".join(terms)
            if eq:
                report += f"$$ J(\\theta) = {eq} $$"

        # Surface the raw LLM output when parsing failed so the user
        # can still see what the model said.
        if not score and "raw_output" in composition:
            report += (
                "\n\n<details><summary>Raw model output</summary>\n\n"
                f"```\n{composition['raw_output']}\n```\n\n</details>"
            )

        return report
