"""Создаёт три тестовые ZIP-VFS для демонстрации этапов 3-5."""

from pathlib import Path
import zipfile


TMP_DIR = Path("tmp")


def write_zip(path, files):
    """Создаёт ZIP-архив из словаря имя -> содержимое."""
    with zipfile.ZipFile(path, "w") as archive:
        for name, text in files.items():
            archive.writestr(name, text)


def main():
    """Создаёт минимальную, обычную и вложенную VFS."""
    TMP_DIR.mkdir(exist_ok=True)

    write_zip(TMP_DIR / "minimal.zip", {"hello.txt": "hello\n"})
    write_zip(
        TMP_DIR / "files.zip",
        {
            "numbers.txt": "1\n2\n3\n",
            "repeat.txt": "a\na\nb\nb\nc\n",
        },
    )
    write_zip(
        TMP_DIR / "nested.zip",
        {
            "docs/readme.txt": "demo\n",
            "level1/level2/level3/file.txt": "deep\n",
            "numbers.txt": "1\n2\n3\n",
            "repeat.txt": "a\na\nb\nb\nc\n",
        },
    )


if __name__ == "__main__":
    main()
