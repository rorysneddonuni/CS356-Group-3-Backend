import os
from pathlib import Path
from typing import Iterable

from fastapi import UploadFile


def upload_file(file: UploadFile, *path_components: [Iterable[str]]) -> Path:
    """Save file to local uploads storage bucket"""
    destination = Path('/'.join(path_components)) / Path(file.filename)
    os.makedirs(destination.parent.resolve(), exist_ok=True)
    with open(destination, 'wb') as dest_file:
        dest_file.write(file.file.read())
    return destination
