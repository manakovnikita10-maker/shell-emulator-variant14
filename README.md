# Конфигурационное управление — вариант 14

## Этап 5. Финальная версия

Эмулятор реализован ровно в пяти последовательных Git-коммитах. Каждый
коммит содержит свой `README.md`, соответствующий состоянию проекта на этапе.

### Реализованные этапы

1. GUI REPL: окно, данные `username@hostname`, кавычки, ошибки, заглушки
   `ls`/`cd`, `exit`.
2. Конфигурация: `--vfs`, `--script`, стартовый сценарий до первой ошибки.
3. ZIP-VFS: загрузка без распаковки и хранение файлов в `base64`.
4. Основные команды: `ls`, `cd`, `tac`, `uniq`.
5. Команды изменения памяти: `chown`, `touch`.

### Структура проекта

```text
src/
  __init__.py
  main.py
  shell.py
  vfs.py
tests/
  make_vfs.py
  stage2.txt
  stage2_both.sh
  stage2_script.sh
  stage2_vfs.sh
  stage3.txt
  stage3_error.txt
  stage3_error.sh
  stage3_files.sh
  stage3_minimal.sh
  stage3_nested.sh
  stage4.txt
  stage4_error.txt
  stage5.txt
  stage5_error.txt
  test_shell.py
  test_stage1.py
  test_stage2.py
  test_stage5.py
  test_vfs.py
.gitignore
README.md
run.sh
```

Отдельной папки `scripts` нет: все небольшие сценарии находятся в `tests`.

### Поддерживаемые команды

```text
ls [PATH]
cd PATH
tac FILE
uniq FILE
chown OWNER PATH
touch PATH
exit
```

`touch` и `chown` изменяют только структуры в оперативной памяти. Исходный
ZIP-архив не распаковывается и не изменяется.

### Подготовка VFS

```bash
python3 tests/make_vfs.py
```

### Демонстрация успешных команд

```bash
./run.sh --vfs tmp/nested.zip --script tests/stage5.txt
```

### Демонстрация ошибки и остановки сценария

```bash
./run.sh --vfs tmp/nested.zip --script tests/stage5_error.txt
```

### Тесты

```bash
python3 -m unittest discover -s tests -v
```

### История этапов

```bash
git log --oneline --reverse
```

Для просмотра этапа:

```bash
git switch --detach <хеш_коммита>
```

Вернуться к финальной версии:

```bash
git switch main
```
