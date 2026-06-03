import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze_with_ollama(model: str, prompt: str, timeout: int = 120) -> str:
    """
    Send a prompt to Ollama and return the response text.
    Uses streaming=False for simplicity.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 1024,
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response received from model.")

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Cannot connect to Ollama. Please start it with: ollama serve"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError(
            f"Ollama timed out after {timeout}s. Try a smaller model or increase timeout."
        )
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(
                f"Model '{model}' not found. Pull it with: ollama pull {model}"
            )
        raise RuntimeError(f"Ollama API error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error calling Ollama: {e}")


def check_ollama_running() -> bool:
    """Check if Ollama server is running."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def list_available_models() -> list:
    """Return list of locally available Ollama models."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        data = r.json()
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []
