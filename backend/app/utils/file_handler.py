# app/utils/file_handler.py

from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile


class FileHandler:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file: UploadFile) -> str:
        extension = Path(file.filename).suffix
        filename = f"{uuid4().hex}{extension}"
        file_path = self.upload_dir / filename

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return str(file_path)


file_handler = FileHandler()
