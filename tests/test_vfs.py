"""Тесты виртуальной файловой системы этапа 3."""

import base64
from pathlib import Path
import tempfile
import unittest
import zipfile

from src.vfs import VirtualFileSystem


class VfsTests(unittest.TestCase):
    """Проверяет загрузку ZIP в оперативную память."""

    def test_zip_is_loaded_into_memory(self):
        """Файл из ZIP должен появиться в словаре VFS."""
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "test.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("docs/file.txt", "hello")

            vfs = VirtualFileSystem()
            vfs.load_zip(archive_path)

        self.assertIn("/docs/file.txt", vfs.files)
        self.assertIn("/docs", vfs.directories)

        raw = base64.b64decode(vfs.files["/docs/file.txt"])
        self.assertEqual(raw.decode("utf-8"), "hello")

    def test_bad_zip_returns_error(self):
        """Неверный ZIP должен давать понятную ошибку."""
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = Path(temp_dir) / "bad.zip"
            archive_path.write_text("not a zip", encoding="utf-8")
            vfs = VirtualFileSystem()

            with self.assertRaises(ValueError):
                vfs.load_zip(archive_path)


if __name__ == "__main__":
    unittest.main()
