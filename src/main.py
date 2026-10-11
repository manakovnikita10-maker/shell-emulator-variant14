"""Этап 1: простой GUI-эмулятор командной оболочки."""

import getpass
import shlex
import socket
import tkinter as tk


WINDOW_WIDTH = 78
WINDOW_HEIGHT = 22


def parse_line(line):
    """Разделяет строку на команду и аргументы с учётом кавычек."""
    return shlex.split(line)


def run_command(parts):
    """Выполняет команды, доступные на первом этапе."""
    if not parts:
        return True, "", False

    command = parts[0]
    args = parts[1:]

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
    """Графическое окно, похожее на UNIX-подобный терминал."""

    def __init__(self, root):
        """Сохраняет данные ОС и создаёт элементы интерфейса."""
        self.root = root
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.root.title(f"Эмулятор - [{self.user}@{self.host}]")
        self._build_interface()
        self.write("Введите команду. Доступно: ls, cd, exit\n")

    def _build_interface(self):
        """Создаёт поле вывода и строку ввода."""
        self.output = tk.Text(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        )
        self.output.pack(padx=10, pady=10)

        self.entry = tk.Entry(
            self.root,
            width=WINDOW_WIDTH,
        )
        self.entry.pack(padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def write(self, text):
        """Добавляет текст в область терминала."""
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def on_enter(self, _event=None):
        """Считывает и выполняет одну команду после Enter."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        prompt = f"{self.user}@{self.host}:~$ "
        self.write(prompt + line + "\n")

        try:
            parts = parse_line(line)
        except ValueError as error:
            self.write(f"Ошибка: {error}\n")
            return

        _ok, message, should_exit = run_command(parts)
        if message:
            self.write(message + "\n")
        if should_exit:
            self.root.destroy()


def main():
    """Запускает графический эмулятор."""
    root = tk.Tk()
    EmulatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
