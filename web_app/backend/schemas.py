"""Modelos de request/response de la API."""

from pydantic import BaseModel

from config import DEFAULT_TOP_K


class SourceIn(BaseModel):
    text: str


class ChatIn(BaseModel):
    message: str
    top_k: int = DEFAULT_TOP_K
