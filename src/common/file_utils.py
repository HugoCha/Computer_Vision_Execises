#!/usr/bin/python3

import os

from pathlib import Path
from typing import Optional

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
DOCUMENT_EXTENSIONS = {".pdf", ".txt", ".docx", ".xlsx", ".pptx"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

def is_path_valid(path: Optional[str] ) -> bool:
    if path is None:
        return False
    
    try:
        Path(path)
        return True
    except (TypeError, ValueError):
        return False
    
def is_valid_image_extension( extension:str ):
    return extension.lower() in IMAGE_EXTENSIONS

def is_directory( path: str ) -> bool:
    return os.path.isdir( path )

def get_filename( filepath:str ) -> str:
    return os.path.basename( filepath )

def get_files_by_extension(directory: str, extension: str) -> list[str]:
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(extension)
    ] 