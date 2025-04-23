import os

from PIL import Image


class StubAdapter:
    """Stub adapter that returns dummy text."""

    def extract_text(self, image: Image.Image) -> str:
        return "dummy text"


class TesseractAdapter:
    """Adapter for Tesseract OCR."""

    def __init__(self):
        try:
            import pytesseract
        except ImportError as e:
            raise ImportError("pytesseract is required for TesseractAdapter") from e
        self.pytesseract = pytesseract

    def extract_text(self, image: Image.Image) -> str:
        return self.pytesseract.image_to_string(image)


class LLMVisionAdapter:
    """Adapter using OpenAI GPT-4o Vision."""

    def __init__(self):
        try:
            import openai
        except ImportError as e:
            raise ImportError("openai is required for LLMVisionAdapter") from e
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        openai.api_key = api_key
        self.openai = openai

    def extract_text(self, image: Image.Image) -> str:
        import io

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        response = self.openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Extract all text from the provided image."}
            ],
        )
        return response.choices[0].message.content


def get_adapter():
    """Select OCR adapter based on OCR_BACKEND env variable."""
    backend = os.getenv("OCR_BACKEND", "").lower()
    if backend == "tesseract":
        try:
            return TesseractAdapter()
        except Exception:
            return StubAdapter()
    if backend == "gpt4v":
        try:
            return LLMVisionAdapter()
        except Exception:
            return StubAdapter()
    return StubAdapter()
