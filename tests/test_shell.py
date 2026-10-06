"""Тесты основных команд этапа 4."""

import base64
import unittest

from src.shell import Shell
from src.vfs import VirtualFileSystem


def encode_text(text):
    """Кодирует текст так же, как файлы внутри VFS."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def make_shell():
    """Создаёт небольшую VFS для тестирования команд."""
    vfs = VirtualFileSystem()
    vfs.directories.add("/docs")
    vfs.files["/docs/numbers.txt"] = encode_text("1\n2\n3\n")
    vfs.files["/repeat.txt"] = encode_text("a\na\nb\nb\nc\n")
    return Shell(vfs)


class ShellTests(unittest.TestCase):
    """Проверяет ls, cd, tac и uniq."""

    def test_ls(self):
        """ls должен показать содержимое корня."""
        shell = make_shell()
        ok, message, _should_exit = shell.execute("ls")
        self.assertTrue(ok)
        self.assertIn("docs", message)
        self.assertIn("repeat.txt", message)

    def test_cd_and_tac(self):
        """cd должен сменить каталог, а tac перевернуть строки."""
        shell = make_shell()
        shell.execute("cd docs")
        ok, message, _should_exit = shell.execute("tac numbers.txt")
        self.assertTrue(ok)
        self.assertEqual(message, "3\n2\n1")

    def test_uniq(self):
        """uniq должен удалить соседние одинаковые строки."""
        shell = make_shell()
        ok, message, _should_exit = shell.execute("uniq repeat.txt")
        self.assertTrue(ok)
        self.assertEqual(message, "a\nb\nc")


if __name__ == "__main__":
    unittest.main()
