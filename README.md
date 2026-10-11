# Конфигурационное управление — вариант 14

## Этап 1. GUI REPL

На первом этапе реализован минимальный графический эмулятор UNIX-подобной
командной оболочки.

### Реализовано

- GUI на `tkinter`;
- заголовок `Эмулятор - [username@hostname]` из реальных данных ОС;
- разбор строки через `shlex`, включая аргументы в кавычках;
- сообщения об ошибках парсинга, неизвестной команде и неверных аргументах;
- команды-заглушки `ls` и `cd`;
- команда `exit`.

### Структура

```text
src/
  __init__.py
  main.py
tests/
  test_stage1.py
.gitignore
README.md
run.sh
```

### Запуск

```bash
./run.sh
```

Для демонстрации:

```text
ls
cd test
cd "my folder"
unknown
exit test
exit
```

### Тесты

```bash
python3 -m unittest discover -s tests -v
```
