"""Этап 5: финальный GUI-эмулятор командной оболочки."""

import argparse
import getpass
import socket
import tkinter as tk

from src.shell import Shell
from src.vfs import VirtualFileSystem


def parse_args(argv=None):
    """Получает пути к VFS и стартовому скрипту."""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки"
    )
    parser.add_argument(
        "--vfs",
        default="",
        help="Путь к ZIP-VFS",
    )
    parser.add_argument(
        "--script",
        default="",
        help="Путь к стартовому скрипту",
    )
    return parser.parse_args(argv)


class EmulatorApp:
    """Графическое окно эмулятора командной оболочки."""

    def __init__(self, root, args):
        """
        Создаёт интерфейс, VFS и командную оболочку.

        Имя пользователя и имя компьютера берутся из реальной ОС.
        Команды выполняются объектом Shell внутри виртуальной файловой
        системы VirtualFileSystem.
        """
        self.root = root
        self.args = args
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.vfs = VirtualFileSystem()
        self.shell = Shell(self.vfs)

        self.root.title(
            f"Эмулятор - [{self.user}@{self.host}]"
        )

        self.output = tk.Text(
            root,
            width=78,
            height=22,
        )
        self.output.pack(
            padx=10,
            pady=10,
        )

        self.entry = tk.Entry(
            root,
            width=78,
        )
        self.entry.pack(
            padx=10,
            pady=(0, 10),
        )
        self.entry.bind(
            "<Return>",
            self.on_enter,
        )
        self.entry.focus()

        self.show_config()
        self.load_vfs()

        if self.args.script:
            self.root.after(
                100,
                self.run_startup,
            )

    def write(self, text):
        """Добавляет текст в область терминала и прокручивает её вниз."""
        self.output.insert(
            tk.END,
            text,
        )
        self.output.see(tk.END)

    def show_config(self):
        """Показывает пути к VFS и стартовому скрипту."""
        vfs_path = self.args.vfs or "не задан"
        script_path = self.args.script or "не задан"
        self.write(f"VFS: {vfs_path}\n")
        self.write(f"Стартовый скрипт: {script_path}\n")

    def load_vfs(self):
        """Загружает ZIP-VFS только в оперативную память."""
        if not self.args.vfs:
            self.write(
                "VFS не задана. Используется пустая VFS.\n\n"
            )
            return

        try:
            self.vfs.load_zip(self.args.vfs)
        except (OSError, ValueError) as error:
            self.write(
                f"Ошибка загрузки VFS: {error}\n\n"
            )
            return

        count = self.vfs.file_count()
        self.write(
            f"VFS загружена в память. Файлов: {count}\n\n"
        )

    def prompt(self):
        """Возвращает приглашение с пользователем и текущим каталогом."""
        return (
            f"{self.user}@{self.host}:"
            f"{self.shell.cwd}$ "
        )

    def execute_line(self, line):
        """Выполняет одну команду и показывает результат в окне."""
        self.write(
            self.prompt() + line + "\n"
        )

        ok, message, should_exit = self.shell.execute(line)

        if message:
            self.write(
                message + "\n"
            )

        if should_exit:
            self.root.destroy()

        return ok

    def on_enter(self, _event=None):
        """Считывает команду из поля ввода после нажатия Enter."""
        line = self.entry.get()
        self.entry.delete(
            0,
            tk.END,
        )
        self.execute_line(line)

    def run_startup(self):
        """
        Выполняет стартовый скрипт построчно до первой ошибки.

        Пустые строки пропускаются. Если команда возвращает ошибку,
        дальнейшее выполнение сценария прекращается.
        """
        try:
            with open(
                self.args.script,
                encoding="utf-8",
            ) as file:
                lines = file.readlines()
        except OSError as error:
            self.write(
                f"Ошибка скрипта: {error}\n"
            )
            return

        for raw_line in lines:
            line = raw_line.strip()

            if not line:
                continue

            if not self.execute_line(line):
                self.write(
                    "Скрипт остановлен из-за ошибки.\n"
                )
                break


def main():
    """Читает параметры и запускает графический эмулятор."""
    args = parse_args()
    root = tk.Tk()
    EmulatorApp(root, args)
    root.mainloop()


if __name__ == "__main__":
    main()
