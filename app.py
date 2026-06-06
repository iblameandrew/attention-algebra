"""Patterns — Gradio front-end.

Wires the three pipeline layers (Algebra → Composition → Code) into a
simple three-pane interface.  Each model is instantiated lazily on the
first request and cached for the lifetime of the process, since
constructing a LangChain ``ChatOllama`` client spins up a subprocess
shim and is not free.
"""

import os
import re
import subprocess

import gradio as gr
from dotenv import load_dotenv

from patterns.algebra import AlgebraAnalyst
from patterns.code import CodeGenerator
from patterns.composition import Composer
from patterns.config import ModelFactory

load_dotenv()

# --- CONSTANTS -------------------------------------------------------------

GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-pro-preview"]

# The "no Ollama available" sentinel is exposed as a string option in the
# dropdown so the user can still see *why* the call will fail.  Any
# model name that starts with this prefix is rejected by ``process_pattern``.
NO_OLLAMA_SENTINEL = "Ollama Not Installed"
DEFAULT_OLLAMA_MODEL = "llama3"

# --- HELPERS ---------------------------------------------------------------


def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> blocks.  Kept for backward-compat."""
    if not text:
        return ""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


def _clean_latex_formatting(text: str) -> str:
    """Make LLM output a little more presentable in the MathJax pane."""
    if not text:
        return ""

    text = text.replace("```latex", "").replace("```markdown", "").replace("```", "")
    text = text.replace("[$", "(").replace("$]", ")")

    pattern = r"(?si)(.*?)(?:[\*\#\s]*Intercalation Dynamics\s*:?[\*\#\s]*)(.*)"
    match = re.search(pattern, text)
    if match:
        preamble = match.group(1).strip()
        equation_raw = match.group(2).strip()
        equation_raw = equation_raw.replace("**", "").replace("*", "")
        if not (equation_raw.startswith("$$") or equation_raw.startswith("\\[")):
            equation_section = f"$$\n{equation_raw}\n$$"
        else:
            equation_section = equation_raw
        return f"{preamble}\n\n**Intercalation Dynamics:**\n\n{equation_section}"

    return re.sub(r"`(\$+.*?\$+)`", r"\1", text)


def _get_ollama_models():
    """Return the list of locally-pulled Ollama models, with fallbacks."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ):
        return [NO_OLLAMA_SENTINEL]

    lines = result.stdout.strip().splitlines()
    if len(lines) <= 1:
        return []
    return [line.split()[0] for line in lines[1:] if line.strip()]


def _provider_model_defaults(provider: str) -> tuple[list[str], str]:
    """Return ``(choices, default)`` for the model ``Dropdown``."""
    if provider == "Google Gemini":
        return list(GEMINI_MODELS), GEMINI_MODELS[0]

    models = _get_ollama_models()
    if not models:
        models = [NO_OLLAMA_SENTINEL]
    return models, models[0]


def _provider_model_choices(provider: str):
    """Build a Gradio ``Dropdown`` update for the selected provider."""
    choices, default = _provider_model_defaults(provider)
    return gr.Dropdown(choices=choices, value=default, interactive=True)


# --- MODEL CACHE -----------------------------------------------------------

# A small LRU-by-key cache.  Constructing LangChain chat models is
# surprisingly expensive (each ChatOllama spins up a subprocess shim),
# and the Gradio app can serve many sequential calls.
_MODEL_CACHE: dict[tuple[str, float], object] = {}


def _get_analyst(model_name: str) -> AlgebraAnalyst:
    key = (model_name, "algebra")
    if key not in _MODEL_CACHE:
        _MODEL_CACHE[key] = AlgebraAnalyst(model_name=model_name)
    return _MODEL_CACHE[key]


def _get_composer(model_name: str) -> Composer:
    key = (model_name, "composer")
    if key not in _MODEL_CACHE:
        _MODEL_CACHE[key] = Composer(model_name=model_name)
    return _MODEL_CACHE[key]


def _get_coder(model_name: str) -> CodeGenerator:
    key = (model_name, "coder")
    if key not in _MODEL_CACHE:
        _MODEL_CACHE[key] = CodeGenerator(model_name=model_name)
    return _MODEL_CACHE[key]


# --- PIPELINE --------------------------------------------------------------


def process_pattern(text: str, model_name: str):
    """Run the three-layer pipeline and return ``(algebra, math, code)``."""
    if not text or not text.strip():
        return "Please enter text.", "", ""

    if not model_name:
        return "Error: no model selected.", "", ""

    if model_name == NO_OLLAMA_SENTINEL:
        return (
            "Error: Ollama is not installed (or returned no models). "
            "Install Ollama and `ollama pull <model>` first, or switch to Gemini.",
            "",
            "",
        )

    if model_name.lower().startswith("gemini") and not os.getenv("GEMINI_API_KEY"):
        return "Error: GEMINI_API_KEY missing in environment.", "", ""

    algebraic_expr = ""
    math_report = ""
    pytorch_code = ""

    # Layer 1 — Algebra
    try:
        print(f"--- L1: Algebra ({model_name}) ---")
        analyst = _get_analyst(model_name)
        algebraic_expr = _strip_think_tags(analyst.analyze(text))
    except Exception as exc:  # noqa: BLE001 — surface the message verbatim
        return f"Error L1: {exc}", "", ""

    # Layer 2 — Composition
    try:
        print("--- L2: Composition ---")
        composer = _get_composer(model_name)
        composition = composer.compose(algebraic_expr)

        if isinstance(composition, dict):
            raw_report = composer.format_latex_report(composition)
            math_report = _clean_latex_formatting(raw_report)
        else:
            math_report = f"Error parsing JSON: {composition}"
            composition = {}  # make layer 3 still emit a sensible error
    except Exception as exc:  # noqa: BLE001
        return algebraic_expr, f"Error L2: {exc}", ""

    # Layer 3 — Code
    try:
        print("--- L3: Code Gen ---")
        coder = _get_coder(model_name)
        pytorch_code = coder.generate_code(composition)
    except Exception as exc:  # noqa: BLE001
        return algebraic_expr, math_report, f"Error L3: {exc}"

    return algebraic_expr, math_report, pytorch_code


# --- UI --------------------------------------------------------------------

custom_css = """
<style>
.container { max-width: 1100px; margin: auto; }
h1 { text-align: center; color: #2d3748; }

#expr_output textarea {
    font-family: 'Courier New', monospace;
    font-size: 18px;
    font-weight: bold;
    color: #2c5282 !important;
    background-color: #ebf8ff !important;
}

#math_output {
    background-color: #ffffff !important;
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 8px;
    --body-text-color: #000000 !important;
    --prose-body: #000000 !important;
}

#math_output * { color: #000000 !important; }

#math_output table {
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
}
#math_output th, #math_output td {
    border: 1px solid #d1d5db !important;
    padding: 8px;
    color: #000000 !important;
    background-color: #ffffff !important;
}

.MathJax, .mjx-chtml, .mjx-char, .mjx-container {
    color: #000000 !important;
    fill: #000000 !important;
    font-size: 115% !important;
}

#math_output code {
    background-color: transparent !important;
    color: #000000 !important;
    border: none !important;
    font-family: inherit;
    font-size: 100%;
}
</style>
"""


def build_ui() -> gr.Blocks:
    """Construct the Gradio Blocks app."""
    initial_choices, initial_default = _provider_model_defaults("Ollama (Local)")

    with gr.Blocks(title="Patterns Engine") as demo:
        gr.HTML(custom_css)

        with gr.Column(elem_classes=["container"]):
            gr.Markdown("# Patterns: Cognitive Transpiler")

            with gr.Row():
                txt_input = gr.Textbox(label="Context", lines=4)
                with gr.Column():
                    provider = gr.Radio(
                        ["Ollama (Local)", "Google Gemini"],
                        value="Ollama (Local)",
                        label="Provider",
                    )
                    model = gr.Dropdown(
                        choices=initial_choices,
                        value=initial_default,
                        label="Model",
                    )
                    btn = gr.Button("Analyze", variant="primary")

            gr.Markdown("---")

            gr.Markdown("### Layer 1: Algebra")
            out1 = gr.Textbox(label="Algebra", elem_id="expr_output", show_label=False)

            gr.Markdown("### Layer 2: Harmonic Schedule")
            out2 = gr.Markdown(
                elem_id="math_output",
                latex_delimiters=[
                    {"left": "$$", "right": "$$", "display": True},
                    {"left": "$", "right": "$", "display": False},
                    {"left": "\\[", "right": "\\]", "display": True},
                    {"left": "\\(", "right": "\\)", "display": False},
                ],
            )

            gr.Markdown("### Layer 3: Code")
            out3 = gr.Code(language="python")

        provider.change(_provider_model_choices, inputs=[provider], outputs=[model])
        btn.click(
            process_pattern, inputs=[txt_input, model], outputs=[out1, out2, out3]
        )

    return demo


if __name__ == "__main__":
    build_ui().launch()


# Make the factory importable for tests / external callers.
__all__ = [
    "GEMINI_MODELS",
    "NO_OLLAMA_SENTINEL",
    "ModelFactory",
    "build_ui",
    "process_pattern",
]
