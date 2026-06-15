Here's **Phase 2 — Topic 12: File I/O** in notes-friendly format:

---

# Phase 2 — Topic 12: File I/O (`open()`, read, write, `with` statement)

## What is it?
File I/O lets your program read from and write to files on disk. Python's `open()` function returns a file object. The `with` statement ensures the file is always closed properly — even if an error occurs. Senior devs must understand file modes, buffering, encoding, and memory-efficient reading of large files.

---

## 1. Opening Files — `open()` and Modes

```python
# open(filename, mode, encoding)
# returns a file object

# MODE TABLE
# "r"  — read (default) — file must exist
# "w"  — write — creates file, OVERWRITES if exists
# "a"  — append — creates file, adds to end if exists
# "x"  — exclusive create — fails if file already exists
# "rb" — read binary
# "wb" — write binary
# "r+" — read AND write

# Always use with statement — auto closes file
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

---

## 2. `with` Statement — Why Always Use It

```python
# WITHOUT with — risky
f = open("data.txt", "r")
content = f.read()
# if exception here — f.close() never called
# file handle leaked!
f.close()


# WITH with — safe
with open("data.txt", "r") as f:
    content = f.read()
# file ALWAYS closed here — even if exception occurs
# with calls __enter__ on open, __exit__ closes automatically


# Opening multiple files at once
with open("input.txt", "r") as fin, open("output.txt", "w") as fout:
    fout.write(fin.read())
```

---

## 3. Reading Files — All Ways

```python
# Assume data.txt contains:
# Hello World
# Python is great
# File I/O is easy

# Way 1 — read() — entire file as ONE string
with open("data.txt", "r") as f:
    content = f.read()
print(content)
# "Hello World\nPython is great\nFile I/O is easy"
# ❌ bad for large files — loads everything into memory


# Way 2 — readlines() — list of lines (with \n)
with open("data.txt", "r") as f:
    lines = f.readlines()
print(lines)
# ["Hello World\n", "Python is great\n", "File I/O is easy"]
# ❌ still loads everything into memory


# Way 3 — readline() — one line at a time
with open("data.txt", "r") as f:
    line = f.readline()       # "Hello World\n"
    line = f.readline()       # "Python is great\n"


# Way 4 — iterate directly (BEST for large files)
with open("data.txt", "r") as f:
    for line in f:            # lazy — one line at a time
        print(line.strip())   # strip removes \n
# ✅ memory efficient — only one line in RAM at a time


# Way 5 — read with size limit
with open("data.txt", "r") as f:
    chunk = f.read(1024)   # read 1024 bytes at a time
    while chunk:
        process(chunk)
        chunk = f.read(1024)
```

---

## 4. Writing Files

```python
# Write mode — OVERWRITES existing content
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")      # write string — no auto newline
    f.write("Python is great\n")

# writelines — writes list of strings (no auto newline either)
lines = ["line 1\n", "line 2\n", "line 3\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)


# Append mode — ADDS to existing content
with open("output.txt", "a") as f:
    f.write("New line added\n")


# Exclusive create — fails if file exists (safe write)
try:
    with open("output.txt", "x") as f:
        f.write("New file only!")
except FileExistsError:
    print("File already exists!")
```

---

## 5. File Pointer — `seek()` and `tell()`

```python
with open("data.txt", "r") as f:
    print(f.tell())       # 0  ← position at start

    content = f.read(5)   # read 5 characters
    print(content)        # "Hello"
    print(f.tell())       # 5  ← position moved

    f.seek(0)             # move pointer back to start
    print(f.tell())       # 0

    f.seek(6)             # jump to position 6
    print(f.read(5))      # "World"

# seek(0) = go to start
# seek(0, 2) = go to end of file
```

---

## 6. Working With JSON — Most Common in Real World

```python
import json

# Python dict → JSON file
data = {
    "name": "Arjun",
    "age": 22,
    "skills": ["Python", "Django", "SQL"]
}

# Write JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
# {
#     "name": "Arjun",
#     "age": 22,
#     "skills": ["Python", "Django", "SQL"]
# }


# Read JSON
with open("data.json", "r") as f:
    loaded = json.load(f)

print(loaded["name"])     # Arjun
print(type(loaded))       # <class 'dict'>


# json.dumps — dict to JSON STRING (no file)
json_str = json.dumps(data, indent=4)

# json.loads — JSON STRING to dict (no file)
data = json.loads(json_str)
```

---

## 7. Working With CSV

```python
import csv

# Write CSV
students = [
    ["Name",  "Score", "Grade"],
    ["Arjun", 85,      "B"],
    ["Priya", 92,      "A"],
    ["Ravi",  76,      "C"],
]

with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(students)


# Read CSV
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)   # skip header row
    for row in reader:
        print(row)
    # ['Arjun', '85', 'B']
    # ['Priya', '92', 'A']


# DictReader — each row as dict (most useful)
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["Name"], row["Score"])
# Arjun 85
# Priya 92
```

---

## 8. File System Operations — `os` and `pathlib`

```python
import os
from pathlib import Path

# Check if file exists
os.path.exists("data.txt")          # True/False
Path("data.txt").exists()           # same — more modern

# Get file info
os.path.getsize("data.txt")         # size in bytes
os.path.basename("/home/arjun/file.txt")  # "file.txt"
os.path.dirname("/home/arjun/file.txt")   # "/home/arjun"

# pathlib — modern, cleaner
path = Path("/home/arjun/data.txt")
print(path.name)        # data.txt
print(path.stem)        # data
print(path.suffix)      # .txt
print(path.parent)      # /home/arjun

# List all files in directory
for f in Path(".").iterdir():
    print(f)

# Find all .py files recursively
for f in Path(".").rglob("*.py"):
    print(f)

# Create/delete
Path("newdir").mkdir(exist_ok=True)
Path("temp.txt").unlink(missing_ok=True)
```

---

## 9. Large File — Memory Efficient Pattern

```python
# 10GB log file — DON'T load into memory

# BAD — loads entire file
with open("huge.log") as f:
    lines = f.readlines()      # ❌ 10GB in RAM

# GOOD — process line by line
with open("huge.log") as f:
    error_count = 0
    for line in f:             # ✅ one line in RAM at a time
        if "ERROR" in line:
            error_count += 1

print(f"Total errors: {error_count}")


# Generator pattern — even cleaner
def read_errors(filepath):
    with open(filepath) as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip()

for error in read_errors("huge.log"):
    print(error)
```

---

## Interview Questions They Actually Ask

**Q1: Why use `with` for file handling instead of manual `open`/`close`?**
> `with` guarantees the file is closed via `__exit__` — even if an exception is raised inside the block. Manual `f.close()` is skipped if an exception occurs before it. Unclosed files leak file descriptors, which are a limited OS resource.

**Q2: What's the difference between `read()`, `readline()`, and `readlines()`?**
> `read()` loads entire file as one string. `readline()` reads one line per call. `readlines()` loads all lines into a list. For large files, iterate directly over the file object — it reads lazily, one line at a time, using O(1) memory.

**Q3: What's the difference between `w` and `a` mode?**
> `w` (write) opens file and **truncates** (deletes all existing content) before writing. `a` (append) opens file and positions the pointer at the **end** — existing content is preserved.

**Q4: What's `json.dump` vs `json.dumps`?**
> `json.dump(data, file)` writes JSON directly to a **file object**. `json.dumps(data)` returns JSON as a **string** — useful for APIs, logging, or in-memory processing.

**Q5: Why `newline=""` when writing CSV?**
> Without `newline=""`, Python adds extra blank lines on Windows because `csv.writer` adds `\r\n` and Python's universal newline mode adds another `\n`. Always use `newline=""` with CSV operations.

---

## Practice Problems

**Beginner — `p2_t12_prac01_file_basics.py`**
Write a program that:
1. Creates a file `students.txt` and writes 5 student names (one per line)
2. Reads the file back and prints each name with its line number
3. Appends one more student
4. Counts total number of students

```python
# expected output:
# 1. Arjun
# 2. Priya
# 3. Ravi
# 4. Sneha
# 5. Kiran
# New student added: Divya
# Total students: 6
```

---

**Senior level — `p2_t12_prac02_log_analyzer.py`**
Write a log analyzer that reads a large log file line by line (using a generator) and:
- Counts total lines
- Counts lines by level (INFO, WARNING, ERROR)
- Extracts all ERROR messages into a separate `errors.txt`
- Outputs a JSON summary file

```python
# log format:
# 2024-01-15 10:23:45 INFO Server started
# 2024-01-15 10:24:01 ERROR Database connection failed
# 2024-01-15 10:24:05 WARNING High memory usage

# expected errors.txt:
# Database connection failed
# ...

# expected summary.json:
# {
#     "total_lines": 1000,
#     "INFO": 850,
#     "WARNING": 100,
#     "ERROR": 50
# }
```

---

## Common Mistakes & Senior Traps

- **Not using `with`** — forgetting `f.close()` leaks file descriptors. Always use `with`.
- **Encoding issues** — always specify `encoding="utf-8"` explicitly — default encoding varies by OS (Windows often uses `cp1252` which breaks on special characters).
- **`write()` doesn't add newlines** — `f.write("hello")` doesn't add `\n`. You must add it: `f.write("hello\n")`.
- **`w` mode deletes existing content** — accidentally opening an existing file in `"w"` mode wipes it instantly. Use `"a"` to append or `"x"` to safely create only new files.
- **Reading after writing without `seek(0)`** — if you write to a file in `"r+"` mode then try to read, the pointer is at the end — you get empty string. Use `f.seek(0)` to reset.
- **`readlines()` includes `\n`** — strip when processing: `[line.strip() for line in f.readlines()]`.

---

Say **next** for Topic 13: Exception Handling!