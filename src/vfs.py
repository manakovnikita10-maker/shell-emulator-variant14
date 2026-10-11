"""Этап 3: виртуальная файловая система в оперативной памяти."""

import base64
import posixpath
import zipfile


class VirtualFileSystem:
    """Хранит ZIP-VFS в словарях и множествах оперативной памяти."""

    def __init__(self):
        """Создаёт пустую виртуальную файловую систему."""
        self.files = {}
        self.directories = {"/"}

    def clear(self):
        """Очищает содержимое VFS перед новой загрузкой."""
        self.files.clear()
        self.directories = {"/"}

    def load_zip(self, archive_path):
        """Загружает ZIP в память без распаковки на диск."""
        self.clear()
        try:
            with zipfile.ZipFile(archive_path, "r") as archive:
                self._read_archive(archive)
        except zipfile.BadZipFile as error:
            raise ValueError("неверный формат ZIP") from error

    def _read_archive(self, archive):
        """Переносит содержимое ZIP в структуры VFS."""
        for info in archive.infolist():
            path = "/" + info.filename.strip("/")
            if path == "/":
                continue
            if info.is_dir():
                self._add_directory(path)
                continue
            self._store_file(path, archive.read(info.filename))

    def _store_file(self, path, data):
        """Сохраняет бинарные данные файла в base64."""
        clean_path = self._clean(path)
        encoded = base64.b64encode(data).decode("ascii")
        self.files[clean_path] = encoded
        self._add_parents(clean_path)

    def _add_directory(self, path):
        """Добавляет каталог и его родительские каталоги."""
        clean_path = self._clean(path)
        self.directories.add(clean_path)
        self._add_parents(clean_path)

    def _add_parents(self, path):
        """Добавляет все родительские каталоги указанного пути."""
        parent = posixpath.dirname(path)
        while parent and parent != "/":
            self.directories.add(parent)
            parent = posixpath.dirname(parent)
        self.directories.add("/")

    def _clean(self, path):
        """Приводит путь к абсолютному UNIX-виду."""
        result = posixpath.normpath(path)
        if not result.startswith("/"):
            result = "/" + result
        return result

    def file_count(self):
        """Возвращает количество файлов в VFS."""
        return len(self.files)
