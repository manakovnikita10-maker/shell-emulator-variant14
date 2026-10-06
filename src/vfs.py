"""Этап 5: VFS с чтением и изменениями только в памяти."""

import base64
import posixpath
import zipfile


DEFAULT_OWNER = "user"


class VirtualFileSystem:
    """Хранит файлы, каталоги и владельцев в оперативной памяти."""

    def __init__(self):
        """Создаёт пустую виртуальную файловую систему."""
        self.files = {}
        self.directories = {"/"}
        self.owners = {"/": DEFAULT_OWNER}

    def clear(self):
        """Очищает содержимое виртуальной файловой системы."""
        self.files.clear()
        self.directories = {"/"}
        self.owners = {"/": DEFAULT_OWNER}

    def load_zip(self, archive_path):
        """
        Загружает ZIP-архив в память без распаковки на диск.

        Перед загрузкой старое содержимое VFS очищается. Повреждённый
        ZIP преобразуется в понятную ошибку ValueError.
        """
        self.clear()

        try:
            with zipfile.ZipFile(archive_path, "r") as archive:
                self._read_archive(archive)
        except zipfile.BadZipFile as error:
            raise ValueError("неверный формат ZIP") from error

    def _read_archive(self, archive):
        """Переносит содержимое ZIP-архива в структуры VFS."""
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
        """Сохраняет файл в памяти в кодировке base64."""
        clean_path = self._clean(path)
        encoded = base64.b64encode(data).decode("ascii")
        self.files[clean_path] = encoded
        self.owners[clean_path] = DEFAULT_OWNER
        self._add_parents(clean_path)

    def _add_directory(self, path):
        """Добавляет каталог и все его родительские каталоги."""
        clean_path = self._clean(path)
        self.directories.add(clean_path)
        self.owners.setdefault(
            clean_path,
            DEFAULT_OWNER,
        )
        self._add_parents(clean_path)

    def _add_parents(self, path):
        """Добавляет в VFS все родительские каталоги заданного пути."""
        parent = posixpath.dirname(path)

        while parent and parent != "/":
            self.directories.add(parent)
            self.owners.setdefault(
                parent,
                DEFAULT_OWNER,
            )
            parent = posixpath.dirname(parent)

        self.directories.add("/")

    def _clean(self, path):
        """Приводит путь к единому абсолютному UNIX-виду."""
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

        return self._clean(
            posixpath.join(cwd, path)
        )

    def exists(self, path):
        """Проверяет наличие файла или каталога в VFS."""
        return (
            path in self.files
            or path in self.directories
        )

    def list_dir(self, path, cwd):
        """Возвращает содержимое каталога или имя указанного файла."""
        target = self.resolve(path, cwd)

        if target in self.files:
            return [posixpath.basename(target)]

        if target not in self.directories:
            raise ValueError("путь не найден")

        return self._children(target)

    def _children(self, directory):
        """Возвращает непосредственных потомков указанного каталога."""
        prefix = (
            "/"
            if directory == "/"
            else directory + "/"
        )
        children = set()
        paths = list(self.directories) + list(self.files)

        for path in paths:
            if not path.startswith(prefix) or path == directory:
                continue

            rest = path[len(prefix):]

            if rest:
                children.add(
                    rest.split("/", 1)[0]
                )

        return sorted(children)

    def change_dir(self, path, cwd):
        """Проверяет каталог и возвращает новый рабочий путь."""
        target = self.resolve(path, cwd)

        if target not in self.directories:
            raise ValueError("каталог не найден")

        return target

    def read_text(self, path, cwd):
        """Читает текстовый файл из VFS и декодирует его как UTF-8."""
        target = self.resolve(path, cwd)

        if target not in self.files:
            raise ValueError("файл не найден")

        raw = base64.b64decode(
            self.files[target]
        )

        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(
                "файл не является текстовым"
            ) from error

    def touch(self, path, cwd):
        """
        Создаёт пустой файл только в оперативной памяти VFS.

        Исходный ZIP-архив не изменяется. Перед созданием проверяется,
        что целевой путь не является каталогом и родитель существует.
        """
        target = self.resolve(path, cwd)

        if target in self.directories:
            raise ValueError(
                "нельзя применить touch к каталогу"
            )

        parent = posixpath.dirname(target) or "/"

        if parent not in self.directories:
            raise ValueError(
                "родительский каталог не найден"
            )

        if target not in self.files:
            self.files[target] = base64.b64encode(
                b""
            ).decode("ascii")
            self.owners[target] = DEFAULT_OWNER

        return target

    def chown(self, owner, path, cwd):
        """
        Изменяет владельца объекта только в оперативной памяти VFS.

        Данные о владельцах хранятся отдельно от файлов в словаре
        owners и не изменяют исходный ZIP-архив.
        """
        if not owner:
            raise ValueError("владелец не указан")

        target = self.resolve(path, cwd)

        if not self.exists(target):
            raise ValueError("путь не найден")

        self.owners[target] = owner
        return target

    def get_owner(self, path, cwd):
        """Возвращает владельца файла или каталога."""
        target = self.resolve(path, cwd)

        if not self.exists(target):
            raise ValueError("путь не найден")

        return self.owners.get(
            target,
            DEFAULT_OWNER,
        )

    def file_count(self):
        """Возвращает количество файлов в виртуальной системе."""
        return len(self.files)
