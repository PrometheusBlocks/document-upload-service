import base64
import json
from service.core import process_document

SAMPLE_PDF_B64 = "JVBERi0xLjAKJUVPRgo="


def test_process_document(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    user_id = "testuser"
    file_bytes = base64.b64decode(SAMPLE_PDF_B64)
    doc = process_document(file_bytes, user_id)
    assert doc.user_id == user_id
    assert isinstance(doc.document_id, str) and len(doc.document_id) > 0
    assert len(doc.pages) == 1
    assert doc.pages[0].text == "dummy text"
    raw_path = tmp_path / "uploads" / user_id / f"{doc.document_id}.pdf"
    assert raw_path.exists()
    extracted_path = tmp_path / "extracted" / user_id / f"{doc.document_id}.json"
    assert extracted_path.exists()
    data = json.loads(extracted_path.read_text())
    assert data["user_id"] == user_id
    assert isinstance(data["document_id"], str)
    assert data["pages"][0]["text"] == "dummy text"
