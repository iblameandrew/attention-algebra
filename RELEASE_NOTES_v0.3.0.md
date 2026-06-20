# Attention Algebra v0.3.0

Backend migration release: Ollama and Gemini are replaced by two
OpenAI-compatible providers wired through the official OpenAI SDK
(via `langchain-openai`).

## Highlights

- **OpenRouter support.** Cloud models via `OPENROUTER_API_KEY` and
  `https://openrouter.ai/api/v1`.  Curated defaults in the Gradio UI
  (`google/gemini-2.5-flash`, `anthropic/claude-sonnet-4`, etc.).
- **llama.cpp server support.** Local inference against any
  OpenAI-compatible llama.cpp endpoint.  Configure with
  `LLAMA_CPP_BASE_URL` (default `http://127.0.0.1:8080/v1`),
  `LLAMA_CPP_MODEL`, and optional `LLAMA_CPP_API_KEY`.
- **New hero image.** Replaced the README GIF with a static banner in
  `assets/attention-algebra-hero.png`.

## Breaking changes

- Removed Ollama (`langchain-ollama`, `ollama` CLI integration) and
  Google Gemini (`langchain-google-genai`, `GEMINI_API_KEY`) backends.
- `AlgebraAnalyst`, `Composer`, and `CodeGenerator` now accept an
  explicit `provider` argument (`"openrouter"` or `"llama.cpp"`).
- Default model is `google/gemini-2.5-flash` on OpenRouter.

## Dependencies

- Added: `openai`, `langchain-openai`
- Removed: `langchain-community`, `langchain-ollama`, `langchain-google-genai`, `ollama`