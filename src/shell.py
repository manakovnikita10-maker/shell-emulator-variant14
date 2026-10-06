"""Этап 5: все команды UNIX-подобного эмулятора."""

import shlex


ONE_ARGUMENT = 1
TWO_ARGUMENTS = 2


def parse_command(line):
    """Разделяет строку на команду и аргументы с учётом кавычек."""
    return shlex.split(line)


class Shell:
    """Разбирает и выполняет команды внутри VFS."""

    def __init__(self, vfs):
        """Сохраняет VFS и начинает работу из корня."""
        self.vfs = vfs
        self.cwd = "/"

    def execute(self, line):
        """Разбирает и выполняет одну командную строку."""
        try:
            parts = parse_command(line)
        except ValueError as error:
            return False, f"Ошибка: {error}", False

        if not parts:
            return True, "", False

        # Первый элемент — команда, остальные — её аргументы.
        command = parts[0]
        args = parts[1:]
        try:
            return self._dispatch(command, args)
        except ValueError as error:
            return False, f"Ошибка: {error}", False

    def _dispatch(self, command, args):
        """Выбирает метод для введённой команды."""
        commands = {
            "ls": self.command_ls,
            "cd": self.command_cd,
            "tac": self.command_tac,
            "uniq": self.command_uniq,
            "chown": self.command_chown,
            "touch": self.command_touch,
            "exit": self.command_exit,
        }
        # По имени команды выбираем соответствующий метод.
        handler = commands.get(command)
        if handler is None:
            message = f"Ошибка: неизвестная команда {command}"
            return False, message, False
        return handler(args)

    def command_ls(self, args):
        """Показывает содержимое каталога."""
        if len(args) > ONE_ARGUMENT:
            message = "Ошибка: ls принимает не более 1 аргумента"
            return False, message, False

        path = args[0] if args else self.cwd
        names = self.vfs.list_dir(path, self.cwd)
        return True, "\n".join(names), False

    def command_cd(self, args):
        """Изменяет текущий рабочий каталог."""
        if len(args) != ONE_ARGUMENT:
            return False, "Ошибка: cd требует 1 аргумент", False

        self.cwd = self.vfs.change_dir(args[0], self.cwd)
        return True, "", False

    def command_tac(self, args):
        """Выводит строки файла в обратном порядке."""
        if len(args) != ONE_ARGUMENT:
            return False, "Ошибка: tac требует 1 аргумент", False

        text = self.vfs.read_text(args[0], self.cwd)
        lines = text.splitlines()
        return True, "\n".join(reversed(lines)), False

    def command_uniq(self, args):
        """Удаляет соседние повторяющиеся строки файла."""
        if len(args) != ONE_ARGUMENT:
            return False, "Ошибка: uniq требует 1 аргумент", False

        text = self.vfs.read_text(args[0], self.cwd)
        result = []
        # Как UNIX uniq, удаляем только соседние повторы.
        for line in text.splitlines():
            if not result or result[-1] != line:
                result.append(line)
        return True, "\n".join(result), False

    def command_chown(self, args):
        """Изменяет владельца файла или каталога в памяти."""
        if len(args) != TWO_ARGUMENTS:
            message = "Ошибка: chown требует OWNER и PATH"
            return False, message, False

        target = self.vfs.chown(args[0], args[1], self.cwd)
        return True, f"Владелец {target}: {args[0]}", False

    def command_touch(self, args):
        """Создаёт пустой файл только в памяти VFS."""
        if len(args) != ONE_ARGUMENT:
            return False, "Ошибка: touch требует 1 аргумент", False

        target = self.vfs.touch(args[0], self.cwd)
        return True, f"touch: {target}", False

    def command_exit(self, args):
        """Запрашивает завершение работы эмулятора."""
        if args:
            return False, "Ошибка: exit не принимает аргументы", False
        return True, "", True
