"""Тесты команд touch и chown этапа 5."""

import unittest

from src.shell import Shell
from src.vfs import VirtualFileSystem


def make_shell():
    """Создаёт пустую VFS с одним каталогом."""
    vfs = VirtualFileSystem()
    vfs.directories.add("/docs")
    vfs.owners["/docs"] = "user"
    return Shell(vfs)


class StageFiveTests(unittest.TestCase):
    """Проверяет изменения VFS только в оперативной памяти."""

    def test_touch_creates_file(self):
        """touch должен создать пустой файл в словаре VFS."""
        shell = make_shell()
        ok, _message, _should_exit = shell.execute("touch new.txt")
        self.assertTrue(ok)
        self.assertIn("/new.txt", shell.vfs.files)

    def test_touch_checks_parent(self):
        """touch должен проверять существование родителя."""
        shell = make_shell()
        ok, message, _should_exit = shell.execute(
            "touch missing/file.txt"
        )
        self.assertFalse(ok)
        self.assertIn("родительский каталог", message)

    def test_chown_changes_owner(self):
        """chown должен менять владельца только в словаре owners."""
        shell = make_shell()
        shell.execute("touch file.txt")
        ok, _message, _should_exit = shell.execute(
            "chown student file.txt"
        )
        self.assertTrue(ok)
        owner = shell.vfs.get_owner("file.txt", "/")
        self.assertEqual(owner, "student")


if __name__ == "__main__":
    unittest.main()
