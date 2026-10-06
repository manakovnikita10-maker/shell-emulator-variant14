"""Тесты первого этапа."""

import unittest

from src.main import parse_line, run_command


class StageOneTests(unittest.TestCase):
    """Проверяет парсер, заглушки, ошибки и exit."""

    def test_quoted_argument(self):
        """Текст в кавычках должен быть одним аргументом."""
        parts = parse_line('cd "my folder"')
        self.assertEqual(parts, ["cd", "my folder"])

    def test_stub_command(self):
        """Заглушка ls должна вывести имя и аргументы."""
        ok, message, should_exit = run_command(["ls", "docs"])
        self.assertTrue(ok)
        self.assertEqual(message, "ls: ['docs']")
        self.assertFalse(should_exit)

    def test_unknown_command(self):
        """Неизвестная команда должна вернуть ошибку."""
        ok, message, _should_exit = run_command(["unknown"])
        self.assertFalse(ok)
        self.assertIn("неизвестная команда", message)

    def test_exit(self):
        """Команда exit должна запросить завершение приложения."""
        ok, message, should_exit = run_command(["exit"])
        self.assertTrue(ok)
        self.assertEqual(message, "")
        self.assertTrue(should_exit)


if __name__ == "__main__":
    unittest.main()
