"""Этап 1: простой GUI-эмулятор командной оболочки."""

import getpass
import shlex
import socket
import tkinter as tk


def parse_line(line):
    """Разделяет строку на команду и аргументы с учётом кавычек."""
    # shlex понимает кавычки: cd "my folder" -> один аргумент.
    return shlex.split(line)


def run_command(parts):
    """Выполняет команды, доступные на первом этапе."""
    if not parts:
        return True, "", False

    command = parts[0]
    args = parts[1:]

    # На первом этапе ls и cd являются только заглушками.
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
        """Создаёт элементы интерфейса и настраивает окно."""
        self.root = root
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.root.title(f"Эмулятор - [{self.user}@{self.host}]")

        # Большое поле показывает историю команд и результаты.
        self.output = tk.Text(root, width=78, height=22)
        self.output.pack(padx=10, pady=10)

        # Однострочное поле используется для ввода команды.
        self.entry = tk.Entry(root, width=78)
        self.entry.pack(padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self.write("Введите команду. Доступно: ls, cd, exit\n")

    def write(self, text):
        """Добавляет текст в область терминала."""
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def on_enter(self, _event=None):
        """Считывает одну команду после нажатия Enter."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)

        # Приглашение имитирует обычную UNIX-командную строку.
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
