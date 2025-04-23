from pydantic import BaseModel


class Page(BaseModel):
    number: int
    text: str


class ExtractedDocument(BaseModel):
    document_id: str
    user_id: str
    original_path: str
    pages: list[Page]
