"""Тесты параметров второго этапа."""

import unittest

from src.main import parse_args


class StageTwoTests(unittest.TestCase):
    """Проверяет параметры командной строки."""

    def test_default_arguments(self):
        """Без параметров должны использоваться пустые пути."""
        args = parse_args([])
        self.assertEqual(args.vfs, "")
        self.assertEqual(args.script, "")

    def test_both_arguments(self):
        """Оба параметра должны считываться одновременно."""
        args = parse_args(
            ["--vfs", "test.zip", "--script", "tests/stage2.txt"]
        )
        self.assertEqual(args.vfs, "test.zip")
        self.assertEqual(args.script, "tests/stage2.txt")


if __name__ == "__main__":
    unittest.main()
