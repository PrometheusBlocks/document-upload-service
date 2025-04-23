# document-upload-service

Generic “ingest ⇢ OCR” block for the PrometheusBlocks ecosystem  
(convertible to any project that needs PDF / image text extraction).

---

## What it does   🚀

| Step | Action |
|------|--------|
| 1 | Saves the raw file under `uploads/<user_id>/<uuid>.<ext>` |
| 2 | Splits PDFs into page-images (via **pdf2image**) or opens images directly (Pillow) |
| 3 | Runs OCR per page through a pluggable adapter:<br>• `stub` → returns *dummy text* (CI safe)<br>• `tesseract` → local Tesseract engine<br>• `gpt4v` → OpenAI GPT-4 Vision (or compatible) |
| 4 | Writes an **ExtractedDocument** JSON package to `extracted/<user>/<uuid>.json` and returns the same data as a Pydantic object |

---

## Quick start

```bash
# activate your venv first
pip install -r requirements.txt          # pdf2image, pillow, pydantic, etc.

export OCR_BACKEND=stub                  # or tesseract / gpt4v
python - <<'PY'
from pathlib import Path
from service.core import process_document

pdf = Path("sample.pdf").read_bytes()
doc = process_document(pdf, user_id="demo")
print(doc.model_dump_json(indent=2)[:400], "…")
PY
