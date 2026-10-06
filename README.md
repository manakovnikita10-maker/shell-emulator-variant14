# Конфигурационное управление — вариант 14

## Этап 5. Финальная версия

Эмулятор командной оболочки реализован в пяти последовательных Git-коммитах.
Каждый коммит содержит свой `README.md`, соответствующий состоянию проекта на
конкретном этапе.

### Реализованные этапы

1. GUI REPL: окно, `username@hostname`, кавычки, ошибки, заглушки `ls`/`cd`,
   `exit`.
2. Конфигурация: `--vfs`, `--script`, стартовый сценарий до первой ошибки.
3. ZIP-VFS: загрузка архива без распаковки, хранение данных в `base64`.
4. Основные команды: `ls`, `cd`, `tac`, `uniq`.
5. Дополнительные команды: `chown`, `touch` только в оперативной памяти.

### Простая структура проекта

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
  stage3_files.sh
  stage3_minimal.sh
  stage3_nested.sh
  stage4.txt
  stage5.txt
  test_shell.py
  test_stage1.py
  test_stage2.py
  test_stage5.py
  test_vfs.py
.gitignore
README.md
run.sh
```

Отдельных папок `scripts` и `os_scripts` нет: сценарии лежат прямо в `tests`.

### Подготовка тестовых VFS

```bash
python3 tests/make_vfs.py
```

### Запуск финальной версии

```bash
./run.sh --vfs tmp/nested.zip
```

С автоматическим стартовым сценарием:

```bash
./run.sh --vfs tmp/nested.zip --script tests/stage5.txt
```

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

### Что хранится только в памяти

- содержимое файлов VFS;
- созданные через `touch` файлы;
- владельцы, изменённые через `chown`.

Исходный ZIP не изменяется.

### Тесты

```bash
python3 -m unittest discover -s tests -v
```

### История этапов

```bash
git log --oneline --reverse
```

Для просмотра старого этапа:

```bash
git switch --detach <хеш_коммита>
```

Вернуться к финальной версии:

```bash
git switch main
```
