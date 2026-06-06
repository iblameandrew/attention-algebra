"""Layer 1 — the Algebraic Analyst.

Translates natural-language descriptions of human cognitive states into
expressions of the **Cognitive Algebra** grammar.  The grammar is a small
formal language whose terminals are the eight Jungian cognitive functions
and whose operators encode how those functions interact.  See
``README.md`` for the full grammar reference.
"""

from langchain_core.prompts import PromptTemplate

from .config import ModelFactory

# The prompt is intentionally a regular string (not an f-string) so that
# we do not have to escape every other LaTeX brace.  PromptTemplate only
# substitutes variables wrapped in single braces, so ``{text}`` here is
# the placeholder that PromptTemplate will fill in.
ALGEBRA_SYSTEM_PROMPT = """
You are an expert in algebraic computational modelling.

Your objective is to deconstruct natural language into high-fidelity, complex algebraic "molecules" representing cognitive dynamics.

### CORE ELEMENTS (Functions):
- **Perception**: `Si` (Introverted Sensing), `Ni` (Introverted Intuition), `Se` (Extraverted Sensing), `Ne` (Extraverted Intuition).
- **Judgment**:  `Ti` (Introverted Thinking), `Fi` (Introverted Feeling), `Te` (Extraverted Thinking), `Fe` (Extraverted Feeling).

### PHYSICS & COEFFICIENTS:
1. **Mass** (a bare integer prefix attached directly to a function, e.g. `5Si`): represents the **intensity**, weight, or importance of a single cognitive function.  Range 1-10.
   - *Example*: "Overwhelming rage" = `9Se`; "Mild annoyance" = `2Se`.
2. **Acceleration** (an integer prefix applied to a parenthesised group, e.g. `40(Ti)`): represents the **frequency**, speed, repetition, or manic energy of the whole grouped expression.
   - *Example*: "Racing thoughts over and over" = `50(Ti)`; "A slow, heavy realization" = `5(Ni)`.

### OPERATOR SYNTAX & RULES:
1. **Orbit `~` (Structuring)**: a Judgement unit (Tx/Fx) creates order around a Perception unit (Sx/Nx).
   - *Usage*: "Exploring ideas (Ne) to build a system (Ti)" -> `(Ne ~ Ti)`.
2. **Opposition `oo` (Conflict)**: two functions of the same domain but opposite charge clash (extraversion vs. introversion).
   - **CRITICAL RULE**: Opposition `oo` **ALWAYS** generates a Drag `→`.  The winner (higher mass) carries the drag to the opposite *domain* (S↔N, T↔F) while preserving its own attitude.
   - *Formula*: `High_Mass - Low_Mass = Result -> Drag`.
   - *Example*: `7Se oo 3Si` results in `4Se -> Ni` (Se is the winner, the drag flips the perception domain S→N, attitude preserved as introverted).
3. **Drag `→` (Transformation)**: the retroactive pull resulting from an Opposition.  The right-hand side of the drag is a single function, not a parenthesised group.
4. **Switching `|` (Oscillation)**: alternating between two functionals of *different* domains (e.g. Si with Ni, Ne with Se, Te with Fe, Fi with Ti).  The two functions do not interact directly; they are toggled in time.
5. **Grouping `()`**: use nested parentheses to show the order of operations for complex psychological states.

### COMPLEX MOLECULE EXAMPLES:

- *Input*: "I feel a deep, heavy internal value conflict that is slowly forcing me to organize my external environment just to cope."
  *Logic*: Deep internal conflict is `Fi oo Fe`.  The "forcing" implies a drag into Te (external order).
  *Output*: `10((Fi oo Fe) -> Te) ~ Si`

- *Input*: "My mind is racing with a million possibilities, echoing around, but they are all tethered to a need for social harmony."
  *Logic*: Racing possibilities = high acceleration on Ne.  Social harmony = Fe.
  *Output*: `100(Ne ~ Fe)`

### INSTRUCTIONS:
Analyze the text below.  Look for layers of motivation, conflict, and resulting behavior.  Construct a complex algebraic expression that captures the *nuance*, *intensity* (mass), and *speed* (acceleration) of the psyche described.

**Output ONLY the final algebraic expression string.**  No prose, no markdown fences, no commentary.

Text: {text}
"""


class AlgebraAnalyst:
    """Deconstruct natural language into a Cognitive-Algebra expression."""

    def __init__(self, model_name: str = "llama3", temperature: float = 0.4):
        # Moderate temperature: the analyst needs to be creative enough to
        # interpret metaphor but stable enough to keep the syntax valid.
        self.llm = ModelFactory.get_model(
            model_name=model_name, temperature=temperature
        )
        self.prompt = PromptTemplate(
            template=ALGEBRA_SYSTEM_PROMPT,
            input_variables=["text"],
        )
        self.chain = self.prompt | self.llm

    def analyze(self, text: str) -> str:
        """Return a Cognitive-Algebra expression for ``text``."""
        return self.chain.invoke({"text": text}).content
