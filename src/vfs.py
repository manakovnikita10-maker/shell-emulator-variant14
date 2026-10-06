"""Этап 4: VFS с операциями чтения и навигации."""

import base64
import posixpath
import zipfile


class VirtualFileSystem:
    """Хранит ZIP-VFS и выполняет операции только в памяти."""

    def __init__(self):
        """Создаёт пустую виртуальную файловую систему."""
        self.files = {}
        self.directories = {"/"}

    def clear(self):
        """Очищает содержимое виртуальной файловой системы."""
        self.files.clear()
        self.directories = {"/"}

    def load_zip(self, archive_path):
        """Загружает ZIP без распаковки файлов на диск."""
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

            data = archive.read(info.filename)
            self._store_file(path, data)

    def _store_file(self, path, data):
        """Сохраняет файл в памяти в формате base64."""
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
        """Добавляет все родительские каталоги заданного пути."""
        parent = posixpath.dirname(path)
        while parent and parent != "/":
            self.directories.add(parent)
            parent = posixpath.dirname(parent)
        self.directories.add("/")

    def _clean(self, path):
        """Приводит путь к единому UNIX-виду."""
        result = posixpath.normpath(path)
        if not result.startswith("/"):
            result = "/" + result
        return result

    def resolve(self, path, cwd):
        """Преобразует относительный путь в абсолютный путь VFS."""
        if not path:
            return cwd
        if path.startswith("/"):
            return self._clean(path)
        return self._clean(posixpath.join(cwd, path))

    def list_dir(self, path, cwd):
        """Возвращает содержимое каталога или имя одного файла."""
        target = self.resolve(path, cwd)
        if target in self.files:
            return [posixpath.basename(target)]
        if target not in self.directories:
            raise ValueError("путь не найден")
        return self._children(target)

    def _children(self, directory):
        """Находит непосредственных потомков каталога."""
        prefix = "/" if directory == "/" else directory + "/"
        children = set()
        paths = list(self.directories) + list(self.files)

        for path in paths:
            if not path.startswith(prefix) or path == directory:
                continue
            rest = path[len(prefix):]
            if rest:
                children.add(rest.split("/", 1)[0])

        return sorted(children)

    def change_dir(self, path, cwd):
        """Проверяет каталог и возвращает новый рабочий путь."""
        target = self.resolve(path, cwd)
        if target not in self.directories:
            raise ValueError("каталог не найден")
        return target

    def read_text(self, path, cwd):
        """Читает текстовый файл из VFS."""
        target = self.resolve(path, cwd)
        if target not in self.files:
            raise ValueError("файл не найден")

        raw = base64.b64decode(self.files[target])
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("файл не является текстовым") from error

    def file_count(self):
        """Возвращает количество файлов в VFS."""
        return len(self.files)
