"""Layer 3 — the Mechanic / Code Generator.

Takes the Mathematical Schedule produced by Layer 2 and asks an LLM to
emit the body of a custom ``AlgebraAgent`` that derives from a PPO
implementation living in the (out-of-tree) ``capo`` library.  The
generated code is meant to be saved as ``algebra_agent.py`` and run
directly.
"""

import json
import logging

from langchain_core.prompts import PromptTemplate

from .config import DEFAULT_OPENROUTER_MODEL, ModelFactory, Provider
from .utils import strip_code_fences, strip_think_tags

log = logging.getLogger(__name__)

CODING_SYSTEM_PROMPT = """
You are an expert Reinforcement Learning Engineer and Computational Psychologist.
Your task is to generate a Python file implementing a dynamic `AlgebraAgent` class based on a provided "Harmonic Schedule" JSON.

### CONTEXT:
You are extending a library called `capo.py`.
- **Base Class**: `PPOAgent`
- **Config Class**: `ObjectiveConfig(name, enabled, weight, mode, metadata)`
- **Available Objectives**: `ExplorationObjective`, `ExploitationObjective`, `GatheringObjective`, `ExtrapolationObjective`, `InterpolationObjective`, `ContrastObjective`, `IntegrationObjective`, `SelectionObjective`.

### INPUT DATA (The Harmonic Schedule):
You will receive a JSON object containing:
1. `score`: objectives with `symbol`, `mass`, `voice`, optional `role` (stem/loop/bulge/primary/secondary).
2. `schedule_logic`: dominant dynamics type (see list below).
3. `global_frequency`: acceleration/speed float.
4. `nodes`: optional tree of sub-structures — recurse when present.
5. `fold_energy`: optional MFE value from `fold[]` expressions.

### SCHEDULE LOGIC IMPLEMENTATIONS:

**Sequential (original):**
- **"Orbital"**: `sin`/`cos` phase-offset weight modulation on `step_count * global_frequency`.
- **"Drag"**: exponential decay on first objective, growth on second.
- **"Stochastic Switching"** / **"Domain Switching"**: `random.random() < frequency` toggles `enabled`.
- **"Adversarial"**: negative weight on secondary objectives.
- **"Linear"**: constant weights.

**RNA-inspired:**
- **"Cooperative Binding"**: stem objectives share `weight * exp(-distance/lambda)`; loop objectives at `(1 - exp(-distance/lambda)) * mass`.  Store distance in metadata.
- **"Feedback Loop"**: `weight * exp(-alpha * step_count)` plus blend with previous-step objective via metadata history.
- **"Partial Adversarial"**: primary weight unchanged; bulge objective at `epsilon * mass` (epsilon=0.1).
- **"Crossing Constraints"**: adversarial weights with constraint flag in metadata; scale secondary by 0.5 when constraint active.
- **"Softmax Junction"**: compute softmax over all objective masses each step; set weights to `mass * softmax_prob`.
- **"Amplified Binding"**: multiply all weights by `gamma=1.5`.
- **"Global Equilibrium"**: use `fold_energy` to scale all weights by `exp(-fold_energy / 10)`.
- **"Sequential Commitment"**: enable objectives progressively — objective `i` activates when `step_count >= i * commit_interval` (default interval=10).

### INSTRUCTIONS:

1. **Imports**: Import `math`, `random`, and the necessary classes from `capo`.
2. **Class Definition**: Define `class AlgebraAgent(PPOAgent):`.

3. **__init__(self, config)**:
   - Store `self.global_frequency`, `self.schedule_logic`, `self.fold_energy`, `self.nodes` from JSON.
   - Initialize `self.step_count = 0`, `self.prev_weights = {{}}`.
   - Build `self.objective_configs` from `score` via `ObjectiveConfig(name, enabled, weight, mode, metadata)`.
   - Call `super().__init__(config)`.

4. **get_action(self, state)**:
   - Increment `self.step_count`.
   - Apply dominant `schedule_logic` dynamics (and recurse `nodes` if nested).
   - Update `self.objective_configs[name].weight` or `.enabled` before `super().get_action(state)`.
   - Return `super().get_action(state)`.

5. **Execution Block**: `if __name__ == "__main__":` with config dict and instantiation.

### OUTPUT RULES:
- Output **ONLY** valid Python code.  No Markdown backticks.
- Handle `score` with 1 or multiple items and optional `nodes` tree.

### INPUT JSON:
{schedule_json}
"""


class CodeGenerator:
    """Generate a stand-alone ``AlgebraAgent`` module from a schedule."""

    def __init__(
        self,
        model_name: str = DEFAULT_OPENROUTER_MODEL,
        provider: Provider = "openrouter",
        temperature: float = 0.2,
    ):
        self.llm = ModelFactory.get_model(
            model_name=model_name,
            provider=provider,
            temperature=temperature,
        )
        self.prompt = PromptTemplate(
            template=CODING_SYSTEM_PROMPT,
            input_variables=["schedule_json"],
        )
        self.chain = self.prompt | self.llm

    def generate_code(self, composition) -> str:
        """Return the cleaned Python source for ``AlgebraAgent``."""
        if isinstance(composition, dict):
            schedule_json = json.dumps(composition, indent=2, default=str)
        elif isinstance(composition, str):
            schedule_json = composition
        else:
            schedule_json = json.dumps({"error": "unknown schedule type"})

        raw_code = self.chain.invoke({"schedule_json": schedule_json}).content
        cleaned = strip_code_fences(strip_think_tags(raw_code))

        log.debug("Generated %d characters of agent code", len(cleaned))
        return cleaned