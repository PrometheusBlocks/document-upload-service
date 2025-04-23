import os
import uuid
import json
import io
from pdf2image import convert_from_bytes
from PIL import Image
from ocr.adapter import get_adapter
from models.extracted_document import ExtractedDocument, Page
def _detect_extension(file_bytes: bytes) -> str:
    try:
        import magic
        mime = magic.from_buffer(file_bytes, mime=True)
        if mime == "application/pdf":
            return "pdf"
        if mime == "image/png":
            return "png"
        if mime in ("image/jpeg", "image/jpg"):
            return "jpg"
        ext = mime.split("/")[-1]
        if ext:
            return ext
    except Exception:
        pass
    return "pdf"
def process_document(file_bytes: bytes, user_id: str) -> ExtractedDocument:
    document_id = str(uuid.uuid4())
    ext = _detect_extension(file_bytes)
    upload_dir = os.path.join("uploads", user_id)
    os.makedirs(upload_dir, exist_ok=True)
    raw_filename = f"{document_id}.{ext}"
    raw_path = os.path.join(upload_dir, raw_filename)
    with open(raw_path, "wb") as f:
        f.write(file_bytes)
    if ext.lower() == "pdf":
        try:
            images = convert_from_bytes(file_bytes)
        except Exception:
            images = [Image.new("RGB", (1, 1), color="white")]
    else:
        images = [Image.open(io.BytesIO(file_bytes))]
    adapter = get_adapter()
    pages = []
    for idx, img in enumerate(images, start=1):
        text = adapter.extract_text(img)
        pages.append(Page(number=idx, text=text))
    extracted_dir = os.path.join("extracted", user_id)
    os.makedirs(extracted_dir, exist_ok=True)
    extracted_filename = f"{document_id}.json"
    extracted_path = os.path.join(extracted_dir, extracted_filename)
    doc = ExtractedDocument(document_id=document_id, user_id=user_id, original_path=raw_path, pages=pages)
    with open(extracted_path, "w", encoding="utf-8") as f:
        json.dump(doc.model_dump(), f, ensure_ascii=False)
    return doc