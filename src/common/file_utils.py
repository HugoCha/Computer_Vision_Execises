#!/usr/bin/python3

import os
from pathlib import Path
from typing import Optional

def is_path_valid(path: Optional[str] ) -> bool:
    if path is None:
        return False
    
    try:
        Path(path)
        return True
    except (TypeError, ValueError):
        return False

def get_files_by_extension(directory: str, extension: str) -> list[str]:
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(extension)
    ] 