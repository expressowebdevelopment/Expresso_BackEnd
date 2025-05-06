# schemas/version.py
from pydantic import BaseModel


class VersionDTO(BaseModel):
    version: str
    release_date: str
    build: str
