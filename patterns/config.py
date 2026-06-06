"""Factory for chat-model clients used by the Patterns pipeline.

The factory abstracts over two back-ends:

* **Ollama** (local) — used when ``model_name`` is anything other than a
  Gemini identifier.  No API key is required.
* **Google Gemini** — used when ``model_name`` starts with ``"gemini"``
  (case-insensitive).  Requires the ``GEMINI_API_KEY`` environment
  variable to be set.
"""

import os

try:
    # Preferred import path (langchain-community is being sunset).
    from langchain_ollama import ChatOllama
except ImportError:  # pragma: no cover - fallback for older installs
    from langchain_community.chat_models import ChatOllama

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:  # pragma: no cover - explicit failure if missing
    ChatGoogleGenerativeAI = None  # type: ignore[assignment]


class ModelFactory:
    """Build chat-model clients on demand."""

    @staticmethod
    def get_model(model_name: str = "llama3", temperature: float = 0.7):
        """Return a chat-model instance for the given ``model_name``.

        Parameters
        ----------
        model_name:
            Either a Gemini model name (e.g. ``"gemini-2.5-flash"``) or the
            name of a model already pulled into the local Ollama
            installation.
        temperature:
            Sampling temperature forwarded to the underlying client.
        """
        print(f"Initializing Model: {model_name} (Temp: {temperature})")

        if model_name.lower().startswith("gemini"):
            if ChatGoogleGenerativeAI is None:
                raise ValueError(
                    "langchain-google-genai is not installed. "
                    "Install it with `pip install langchain-google-genai`."
                )
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError(
                    "GEMINI_API_KEY not found in environment variables. "
                    "Set it in your shell or in a .env file."
                )

            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                google_api_key=api_key,
                # Gemini rejects system-only messages on some endpoints.
                convert_system_message_to_human=True,
            )

        return ChatOllama(model=model_name, temperature=temperature)
