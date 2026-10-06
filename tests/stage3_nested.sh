#!/bin/sh
python3 tests/make_vfs.py
python3 -m src.main --vfs tmp/nested.zip --script tests/stage3.txt
