# Patterns v0.2.0

A bug-fix and infrastructure release that also reframes the project
as a formal grammar for lifting natural language into a
higher-dimensional space of cognitive functional constituents.

## Highlights

- **Reframed documentation.** The README is now organised around the
  idea of *Patterns as a grammar*: an explicit terminal/operator
  reference, a worked BNF, a description of the four-dimensional
  functional space it lives in, and a `parse → compose → emit`
  pipeline diagram.
- **`patterns.utils` module.** A single home for the
  `strip_think_tags` and `strip_code_fences` helpers used across all
  three layers.

## Bug fixes

- `CodeGenerator.generate_code` now actually strips the Markdown
  fences from the LLM response — previously the saved `.py` file
  started with `​```python`, making it un-importable.
- `CodeGenerator.generate_code` no longer crashes on a non-dict
  schedule (the JSON-parse error path from Layer 2).
- `process_pattern` no longer tells the user `GOOGLE_API_KEY` is
  missing when the variable is `GEMINI_API_KEY`.
- `get_ollama_models` no longer silently returns `["llama3"]` when
  Ollama is missing; the UI now shows a clear error and refuses to
  call the LLM with a fake model.
- `process_pattern` validates the selected model name and refuses to
  start the pipeline with an empty / sentinel value.
- `AlgebraAnalyst`, `Composer`, and `CodeGenerator` are now cached
  per model name instead of being re-instantiated on every request.
- `Composer._parse_json_safely` no longer leaves a leading newline in
  the cleaned JSON body.
- `Composer.format_latex_report` no longer emits invalid LaTeX
  (e.g. `J(θ) = ∫ () dt`) when the `score` list is empty.  When JSON
  parsing fails, the raw LLM output is now surfaced in a collapsible
  block in the report.
- Stale `print(self.prompt)` debug line removed from `Composer.__init__`.
- The legacy `langchain_core.prompts.prompt` import path (no longer
  present in modern langchain-core) has been replaced with
  `langchain_core.prompts` everywhere.
- Layer temperatures have been tuned: 0.4 for the algebra analyst,
  0.2 for the JSON composer and the code generator.
- The algebra prompt no longer needs every LaTeX brace double-escaped
  (it used to be an f-string); the documentation of `mass` vs.
  `acceleration` is now consistent with the worked examples.

## Infrastructure

- Migrated `ChatOllama` to the new `langchain-ollama` package
  (`langchain-community` is being sunset).  The old import path is
  kept as a fallback.
- `requirements.txt`: removed unused `numpy`; added minimum versions
  and `langchain-ollama`.
- `app.py`: `build_ui()` is now a factory so the Gradio app can be
  embedded in tests.
- The public `patterns` package re-exports `strip_think_tags`,
  `strip_code_fences`, `ModelFactory`, and the three layer classes;
  `__version__` is set to `0.2.0`.
