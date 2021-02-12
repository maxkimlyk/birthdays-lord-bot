import os

from . import exceptions


class Share:
    def __init__(self, share_dir: str):
        self._share_dir = share_dir

    def get_file(self, file_path: str) -> bytes:
        file = open(os.path.join(self._share_dir, file_path), 'rb')
        if not file:
            raise exceptions.ResourceNotFound('{} not found'.format(file_path))
        content = file.read()
        file.close()
        return content
