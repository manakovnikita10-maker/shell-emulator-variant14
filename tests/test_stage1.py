"""Проверки функций первого этапа в итоговой архитектуре этапа 4."""

import unittest

from src.shell import Shell, parse_command
from src.vfs import VirtualFileSystem


class StageOneTests(unittest.TestCase):
    """Проверяет кавычки, неизвестную команду и exit."""

    def test_quoted_argument(self):
        """Текст в кавычках должен быть одним аргументом."""
        parts = parse_command('cd "my folder"')
        self.assertEqual(parts, ["cd", "my folder"])

    def test_unknown_command(self):
        """Неизвестная команда должна вернуть ошибку."""
        shell = Shell(VirtualFileSystem())
        ok, message, _should_exit = shell.execute("unknown")
        self.assertFalse(ok)
        self.assertIn("неизвестная команда", message)

    def test_exit(self):
        """Команда exit должна запросить закрытие приложения."""
        shell = Shell(VirtualFileSystem())
        ok, message, should_exit = shell.execute("exit")
        self.assertTrue(ok)
        self.assertEqual(message, "")
        self.assertTrue(should_exit)


if __name__ == "__main__":
    unittest.main()
