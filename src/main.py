"""Этап 2: настраиваемый GUI-эмулятор командной оболочки."""

import argparse
import getpass
import shlex
import socket
import tkinter as tk


def parse_line(line):
    """Разделяет строку на команду и аргументы с учётом кавычек."""
    # shlex понимает кавычки: cd "my folder" -> один аргумент.
    return shlex.split(line)


def parse_args(argv=None):
    """Получает пути к VFS и стартовому скрипту."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки")
    parser.add_argument("--vfs", default="", help="Путь к VFS")
    parser.add_argument(
        "--script",
        default="",
        help="Путь к стартовому скрипту",
    )
    return parser.parse_args(argv)


def run_command(parts):
    """Выполняет команды, доступные до подключения VFS."""
    if not parts:
        return True, "", False

    command = parts[0]
    args = parts[1:]

    # До этапа 4 команды ls и cd остаются заглушками.
    if command in ("ls", "cd"):
        return True, f"{command}: {args}", False

    if command == "exit":
        if args:
            message = "Ошибка: exit не принимает аргументы"
            return False, message, False
        return True, "", True

    message = f"Ошибка: неизвестная команда {command}"
    return False, message, False


class EmulatorApp:
    """Графическое окно эмулятора командной оболочки."""

    def __init__(self, root, args):
        """Создаёт интерфейс и сохраняет параметры запуска."""
        self.root = root
        self.args = args
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.root.title(f"Эмулятор - [{self.user}@{self.host}]")

        self.output = tk.Text(root, width=78, height=22)
        self.output.pack(padx=10, pady=10)
        self.entry = tk.Entry(root, width=78)
        self.entry.pack(padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        # По заданию параметры показываются сразу после запуска.
        self.show_config()
        if self.args.script:
            self.root.after(100, self.run_startup)

    def write(self, text):
        """Добавляет текст в область терминала."""
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def show_config(self):
        """Показывает переданные программе параметры."""
        vfs_path = self.args.vfs or "не задан"
        script_path = self.args.script or "не задан"
        self.write(f"VFS: {vfs_path}\n")
        self.write(f"Стартовый скрипт: {script_path}\n\n")

    def execute_line(self, line):
        """Разбирает и выполняет одну команду."""
        prompt = f"{self.user}@{self.host}:~$ "
        self.write(prompt + line + "\n")

        try:
            parts = parse_line(line)
        except ValueError as error:
            self.write(f"Ошибка: {error}\n")
            return False

        ok, message, should_exit = run_command(parts)
        if message:
            self.write(message + "\n")
        if should_exit:
            self.root.destroy()
        return ok

    def on_enter(self, _event=None):
        """Обрабатывает команду, введённую пользователем."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.execute_line(line)

    def run_startup(self):
        """Выполняет стартовый скрипт до первой ошибки."""
        try:
            with open(self.args.script, encoding="utf-8") as file:
                lines = file.readlines()
        except OSError as error:
            self.write(f"Ошибка скрипта: {error}\n")
            return

        # Команды выполняются по очереди как при ручном вводе.
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if not self.execute_line(line):
                self.write("Скрипт остановлен из-за ошибки.\n")
                break


def main():
    """Читает параметры и запускает графический эмулятор."""
    args = parse_args()
    root = tk.Tk()
    EmulatorApp(root, args)
    root.mainloop()


if __name__ == "__main__":
    main()
