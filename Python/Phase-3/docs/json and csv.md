# Phase 3, Topic 8: JSON & CSV

## 1. What is it

`json` and `csv` are stdlib modules for serializing/deserializing two of the most common data-interchange formats — JSON for nested/structured data (APIs, configs), CSV for flat tabular data (spreadsheets, exports, logs). At senior level this matters because real production code constantly crosses format boundaries with external systems, and interviewers probe whether you understand the *edge cases* — encoding issues, type coercion surprises, streaming large files, and security concerns — not just `json.load()`.

## 2. Core concepts table

| Concept | What it does |
|---|---|
| `json.dumps()` | Python object → JSON string |
| `json.loads()` | JSON string → Python object |
| `json.dump()` / `json.load()` | Same, but read/write directly to a file object |
| `default=` param | Custom serializer for non-JSON-native types (e.g., `datetime`) |
| `object_hook=` param | Custom deserializer — transforms dicts during parsing |
| `cls=` param | Custom `JSONEncoder`/`JSONDecoder` subclass |
| `indent=` / `sort_keys=` | Pretty-printing options |
| `csv.reader()` / `csv.writer()` | Row-by-row, list-based CSV I/O |
| `csv.DictReader()` / `csv.DictWriter()` | Row-by-row, dict-based CSV I/O (uses header row as keys) |
| `Dialect` / `delimiter=` | Controls separators, quoting rules (e.g., TSV, semicolon-CSV) |
| `newline=''` | Required file-open flag on `open()` for correct CSV line handling |
| `quoting=` | Controls when/how fields get quoted (`QUOTE_MINIMAL`, `QUOTE_ALL`, etc.) |

## 3. Syntax & code examples

### Basic usage

```python
import json

data = {"name": "Sumanth", "role": "AI Engineer", "years": 4}

# Python object → JSON string
json_str = json.dumps(data, indent=2)
print(json_str)
# → {
#     "name": "Sumanth",
#     "role": "AI Engineer",
#     "years": 4
#   }

# JSON string → Python object
parsed = json.loads(json_str)
print(parsed["years"])
# → 4
```

```python
import csv

rows = [["name", "role"], ["Sumanth", "AI Engineer"], ["Alex", "PM"]]

# newline='' is REQUIRED on Windows to avoid extra blank rows —
# csv module handles its own line endings internally
with open("people.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

with open("people.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
# → ['name', 'role']
# → ['Sumanth', 'AI Engineer']
# → ['Alex', 'PM']
```

### Common real-world pattern — DictReader/Writer for real datasets

```python
import csv

with open("people.csv") as f:
    reader = csv.DictReader(f)   # uses first row as field names automatically
    for row in reader:
        print(row["name"], "-", row["role"])
# → Sumanth - AI Engineer
# → Alex - PM

with open("out.csv", "w", newline="") as f:
    fieldnames = ["name", "role"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"name": "Priya", "role": "Data Scientist"})
```

```python
import json
from datetime import datetime

# JSON has no native datetime type — must handle it explicitly
def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

payload = {"created_at": datetime.now(), "event": "login"}
print(json.dumps(payload, default=default_serializer))
# → {"created_at": "2026-07-08T14:32:01.123456", "event": "login"}
```

### Senior-level / non-obvious usage

```python
import json

# object_hook lets you transform data DURING parsing, not after —
# useful for reviving custom types or catching malformed data early
def revive_dates(d):
    if "created_at" in d:
        from datetime import datetime
        d["created_at"] = datetime.fromisoformat(d["created_at"])
    return d

raw = '{"event": "login", "created_at": "2026-07-08T14:32:01"}'
parsed = json.loads(raw, object_hook=revive_dates)
print(type(parsed["created_at"]))
# → <class 'datetime.datetime'>
```

```python
import csv

# Streaming a huge CSV without loading it all into memory —
# csv.reader is already a generator/iterator under the hood, don't
# materialize it with list() unless you actually need random access
def sum_column(filepath, column_name):
    total = 0
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:              # one row in memory at a time
            total += float(row[column_name])
    return total

# For MULTI-GB csv files, this pattern keeps memory flat regardless of file size.
```

```python
import json

# json.JSONDecoder with object_pairs_hook to DETECT duplicate keys —
# json.loads silently keeps only the LAST duplicate key by default,
# which can hide bugs/security issues (e.g. two "role" fields in a payload)
def no_duplicates(pairs):
    seen = set()
    result = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError(f"Duplicate key detected: {k}")
        seen.add(k)
        result[k] = v
    return result

json.loads('{"role": "user", "role": "admin"}', object_pairs_hook=no_duplicates)
# → ValueError: Duplicate key detected: role
# (default json.loads would have silently returned {"role": "admin"})
```

## 4. Internals — how it works under the hood

```
json.loads(text)
   │
   ▼
1. C-accelerated scanner (_json module, C extension) tokenizes the
   raw text character by character — falls back to pure-Python
   scanner if C extension unavailable (rare, e.g. some embedded builds)
   ▼
2. Recursive-descent parse: {  →  start dict
                              "  →  parse string
                              :  →  expect value
                              ,  →  next pair
                              }  →  close dict
   ▼
3. Each JSON type maps DIRECTLY to a Python type:
      object → dict     array  → list     string → str
      number → int/float   true/false → bool   null → None
   ▼
4. If object_hook given, called on EVERY dict as it's built,
   bottom-up (innermost objects processed first)
```

```
csv.reader(file)
   │
   ▼
Returns an ITERATOR (not a list!) — reads and parses ONE line at
a time from the underlying file object, tracking quote/delimiter
state across the line (handles embedded newlines inside quoted
fields, which naive f.readlines().split(",") would break on)
   │
   ▼
Each __next__() call:
   - reads next physical line(s) from file (may span multiple
     physical lines if a quoted field contains a newline)
   - splits on delimiter, respecting quotechar/escapechar rules
   - returns a list[str] — csv.reader NEVER infers types;
     everything is a string, always
```

Key internals:

- **`json.dumps`/`loads` use a C accelerator (`_json`) by default** — this is why JSON parsing in Python is much faster than most people expect for a "pure Python" stdlib module; the pure-Python fallback (`json.decoder.py`) exists mainly for PyPy/restricted environments.
- **CSV has no type system at all.** Every field read via `csv.reader`/`DictReader` is a `str`, even if it "looks like" a number — this is one of the most common junior mistakes (forgetting to `int()`/`float()` cast, then getting `TypeError` or wrong sort order downstream).
- **`csv.reader` correctly handles embedded delimiters/newlines inside quoted fields** by tracking quoting state across the raw stream — a naive `line.split(",")` approach breaks the moment a field contains a comma or a newline inside quotes, which is why hand-rolled CSV parsing is a classic senior-interview red flag.
- **`json.dumps` with duplicate dict keys can't even happen in Python** (dicts can't have duplicate keys), but *parsing* JSON *text* with duplicate keys is valid JSON syntax and Python's default behavior silently keeps the last one — a subtle spot where JSON's spec is looser than Python's data model.

## 5. Interview questions

**Q1: Why does `csv.reader` return everything as strings, and how would you handle type conversion cleanly at scale?**
A: CSV as a format has no concept of types — it's just delimited text, so `csv.reader` can't know if `"42"` should become an `int` or stay a `str`; converting on your behalf would require guessing, and Python explicitly avoids implicit guessing here. At scale, the clean pattern is to define an explicit schema (e.g., a dict of `{column: converter_function}` or a `dataclass` with typed fields) and map each row through it during ingestion, rather than sprinkling ad-hoc `int()`/`float()` calls, and to validate/handle conversion failures (`ValueError`) per-row rather than letting one bad row crash the whole pipeline.

**Q2: How would you serialize a Python object that isn't JSON-native, like a `datetime` or a custom class instance?**
A: Pass a `default=` callable to `json.dumps` — it's invoked only for objects the encoder doesn't know how to serialize natively, and should return a JSON-serializable representation (commonly `.isoformat()` for dates, or `obj.__dict__`/a custom `to_dict()` method for classes). For the reverse direction, use `object_hook` in `json.loads` to detect and revive those representations back into real objects during parsing, rather than post-processing the whole parsed structure afterward.

**Q3: What's a security concern with parsing JSON or CSV from untrusted sources?**
A: For JSON: extremely deeply nested structures can cause stack overflow / DoS on parsing (json.loads has no built-in nesting-depth limit by default in older versions — this has caused real CVEs), and blindly trusting `object_hook`/`cls` custom deserializers to reconstruct arbitrary classes can enable object-injection style attacks if not carefully scoped. For CSV: opening CSV files in spreadsheet software can trigger "CSV injection" if a field starts with `=`, `+`, `-`, or `@` and gets interpreted as a formula by Excel/Sheets when the file is later opened by a human — a real vulnerability class in exported user-generated CSV data, mitigated by prefixing risky leading characters or explicitly quoting all fields.

**Q4: Why is `newline=''` required when opening files for `csv` reading/writing?**
A: The `csv` module manages its own line-ending logic internally (it needs full control to correctly detect embedded newlines inside quoted fields), so it expects the underlying file to *not* perform Python's universal newline translation. If you open in default text mode on Windows, `\n` inside the written data can get translated to `\r\n`, and combined with the csv module's own `\r\n` line terminator, you end up with doubled `\r` characters and blank rows appearing between every real row.

**Q5: How do you handle a JSON file too large to fit comfortably in memory?**
A: Standard `json.load()` requires the entire document in memory at once because JSON's grammar isn't naturally line-delimited — but there are two common senior-level approaches: (1) if you control the data format, prefer **JSON Lines (JSONL)** — one JSON object per line — so you can stream and `json.loads()` line by line without ever holding the whole file in memory; (2) if you must consume arbitrary large JSON as-is, use a streaming parser library like `ijson`, which emits events incrementally (similar to SAX-style XML parsing) instead of building the full object tree upfront.

## 6. Practice problems

**Beginner** — `json_csv_prac01_convert_json_to_csv.py`
Given a list of dicts representing users:
```python
users = [
    {"name": "Sumanth", "role": "AI Engineer", "years": 4},
    {"name": "Priya", "role": "Data Scientist", "years": 2},
]
```
Write a function `json_list_to_csv(users, filepath)` that writes this to a CSV file with a header row, using `csv.DictWriter`. Then write a function `csv_to_json_list(filepath)` that reads it back and returns a list of dicts with `"years"` correctly converted back to `int`.

Expected:
```python
json_list_to_csv(users, "users.csv")
csv_to_json_list("users.csv")
# → [{"name": "Sumanth", "role": "AI Engineer", "years": 4},
#     {"name": "Priya", "role": "Data Scientist", "years": 2}]
```

**Senior** — `json_csv_prac02_streaming_log_aggregator.py`
You have a large JSONL log file (`events.jsonl`, one JSON object per line) where each line looks like:
```json
{"user_id": "u1", "event": "purchase", "amount": 49.99, "timestamp": "2026-07-08T10:00:00"}
```
Write a function `aggregate_purchases(filepath) -> dict` that:
- Streams the file line by line (must NOT load the whole file into memory — process one line at a time).
- Skips and logs (prints a warning, doesn't crash) any line that fails `json.loads` (malformed data) or is missing the `"amount"`/`"event"` keys.
- Returns a dict mapping `user_id → total purchase amount`, considering only rows where `event == "purchase"`.
- Also write a `write_summary_csv(summary: dict, filepath)` function that dumps that aggregated dict to a CSV with columns `user_id, total_amount`, sorted by `total_amount` descending.

Expected behavior (with a mix of valid and malformed lines in the input file): malformed lines are skipped with a warning printed, valid purchase amounts are correctly summed per user, and the output CSV is sorted highest-spender first.

## 7. Common mistakes & senior traps

- **Forgetting CSV fields are always strings.** Comparing/sorting numeric-looking CSV columns as strings gives wrong results.

  ```python
  # WRONG
  rows = sorted(reader, key=lambda r: r["amount"])
  # → sorts "9" after "100" lexicographically ("1" < "9" as characters)

  # RIGHT
  rows = sorted(reader, key=lambda r: float(r["amount"]))
  ```

- **Opening CSV files without `newline=''`**, causing blank rows on Windows or double line-endings when writing.

  ```python
  # WRONG
  with open("out.csv", "w") as f:
      writer = csv.writer(f)

  # RIGHT
  with open("out.csv", "w", newline="") as f:
      writer = csv.writer(f)
  ```

- **Loading an entire huge JSON/CSV file into memory with `json.load()` / `list(csv.reader(...))`** when a streaming/generator-based approach would keep memory flat.

- **Not handling `default=` for non-native types and getting `TypeError: Object of type datetime is not JSON serializable`** in production, discovered only at runtime instead of anticipated during design.

- **Assuming `json.loads` fails loudly and completely on any bad input rather than checking exact behavior around edge cases** — e.g., duplicate keys are *silently* resolved to the last occurrence rather than raising an error, which can hide real data-integrity bugs from upstream systems.

- **Manually parsing CSV with `.split(",")`** instead of the `csv` module — breaks immediately on any field containing a comma or a quoted embedded newline, which is exactly why the `csv` module exists and is a near-guaranteed "why not just split on commas?" interview follow-up.

Say "next" when you're ready to move to **HTTP requests**.