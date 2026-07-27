# Standard Library (Senior/Interview Level)

## 1. What is it

Python's standard library is a collection of **built-in modules shipped with every Python installation** — no pip install needed. At senior level, this isn't about memorizing every module; it's about knowing **which module to reach for first** before writing custom code, understanding the performance and design tradeoffs of key modules, and demonstrating that you don't reinvent wheels in production. Interviewers use this topic to separate developers who know Python deeply from those who only know its syntax — the standard library is where Python's "batteries included" philosophy actually lives.

---

## 2. Core concepts table

| Module | What it's for |
|---|---|
| `collections` | Specialized containers: `defaultdict`, `Counter`, `deque`, `OrderedDict`, `namedtuple`, `ChainMap` |
| `itertools` | Efficient iterator building blocks: `chain`, `islice`, `product`, `groupby`, `combinations`, `permutations` |
| `functools` | Higher-order function tools: `lru_cache`, `partial`, `reduce`, `wraps`, `total_ordering` |
| `pathlib` | Object-oriented file system paths — modern replacement for `os.path` |
| `os` / `os.path` | OS interaction: env vars, file/dir ops, process info |
| `sys` | Interpreter internals: `argv`, `path`, `stdin/stdout/stderr`, `exit()` |
| `datetime` | Date/time arithmetic, formatting, timezone handling |
| `time` | Low-level timing: `time()`, `sleep()`, `perf_counter()` |
| `re` | Regular expressions (covered in its own topic later) |
| `json` | JSON serialization/deserialization |
| `csv` | CSV reading/writing |
| `logging` | Production-grade logging with levels, handlers, formatters |
| `threading` / `multiprocessing` | Concurrency and parallelism |
| `subprocess` | Spawn and communicate with external processes |
| `typing` | Type hint support: `Optional`, `Union`, `List`, `Dict`, `TypeVar`, `Protocol` |
| `abc` | Abstract base classes via `ABCMeta` and `@abstractmethod` |
| `copy` | Shallow and deep copying of objects |
| `enum` | Enumerations with `Enum`, `IntEnum`, `Flag` |
| `dataclasses` | (covered previously) |
| `contextlib` | (covered previously) |
| `heapq` | Heap queue / priority queue operations |
| `bisect` | Binary search on sorted lists |
| `math` / `statistics` | Math functions, statistical computations |
| `random` | Pseudorandom number generation |
| `hashlib` | Cryptographic hashing: `md5`, `sha256`, etc. |
| `uuid` | UUID generation |
| `pprint` | Pretty-printing complex data structures |
| `textwrap` | Text wrapping and formatting |
| `io` | In-memory file-like objects: `StringIO`, `BytesIO` |

---

## 3. Syntax & code examples

### `collections` — the most interview-heavy standard library module

```python
from collections import defaultdict, Counter, deque, namedtuple, ChainMap

# defaultdict — never raises KeyError, auto-initializes missing keys
word_count = defaultdict(int)
for word in ["apple", "banana", "apple", "cherry", "banana", "apple"]:
    word_count[word] += 1
print(dict(word_count))  # → {'apple': 3, 'banana': 2, 'cherry': 1}

# Grouping with defaultdict(list)
grouped = defaultdict(list)
data = [("engineering", "Alice"), ("marketing", "Bob"), ("engineering", "Carol")]
for dept, name in data:
    grouped[dept].append(name)
print(dict(grouped))
# → {'engineering': ['Alice', 'Carol'], 'marketing': ['Bob']}


# Counter — frequency counting + set-like operations
inventory = Counter(["apple", "apple", "banana", "cherry", "apple", "banana"])
print(inventory)                     # → Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(inventory.most_common(2))      # → [('apple', 3), ('banana', 2)]
print(inventory["mango"])            # → 0  (not KeyError — this is Counter's key feature)

c1 = Counter(a=3, b=2)
c2 = Counter(a=1, b=4)
print(c1 + c2)                       # → Counter({'b': 6, 'a': 4})
print(c1 - c2)                       # → Counter({'a': 2})  (negatives dropped)
print(c1 & c2)                       # → Counter({'a': 1, 'b': 2})  (min of each)


# deque — O(1) appends and pops from BOTH ends (list is O(n) for left operations)
dq = deque([1, 2, 3], maxlen=4)      # maxlen auto-discards from opposite end
dq.appendleft(0)
print(dq)                            # → deque([0, 1, 2, 3], maxlen=4)
dq.append(99)                        # pushes 0 out (maxlen enforced)
print(dq)                            # → deque([1, 2, 3, 99], maxlen=4)
dq.rotate(1)                         # rotate right by 1
print(dq)                            # → deque([99, 1, 2, 3])


# namedtuple — immutable, memory-efficient, positionally indexable
Point = namedtuple("Point", ["x", "y"])
p = Point(3.0, 4.0)
print(p.x, p[1])                     # → 3.0  4.0 (attribute AND index access)
print(p._asdict())                   # → {'x': 3.0, 'y': 4.0}
px, py = p                           # tuple unpacking works


# ChainMap — layered lookup across multiple dicts (later dicts = fallback)
defaults   = {"theme": "light", "language": "en", "timeout": 30}
user_prefs = {"theme": "dark"}
config = ChainMap(user_prefs, defaults)   # user_prefs takes priority
print(config["theme"])               # → "dark"   (from user_prefs)
print(config["language"])            # → "en"     (from defaults)
config["timeout"] = 60               # writes ALWAYS go to the FIRST map
print(user_prefs)                    # → {'theme': 'dark', 'timeout': 60}
```

### `itertools` — lazy, memory-efficient iteration

```python
import itertools

# chain — flatten multiple iterables into one without building a list
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print(combined)                  # → [1, 2, 3, 4, 5]

# islice — take a slice from any iterator (works on generators, infinite sequences)
gen = (x**2 for x in itertools.count(1))   # infinite: 1, 4, 9, 16 ...
print(list(itertools.islice(gen, 5)))       # → [1, 4, 9, 16, 25]

# groupby — group consecutive elements by a key (input MUST be sorted by key first)
data = [
    {"dept": "eng",  "name": "Alice"},
    {"dept": "eng",  "name": "Carol"},
    {"dept": "mkt",  "name": "Bob"},
]
data.sort(key=lambda r: r["dept"])      # MUST sort before groupby
for dept, members in itertools.groupby(data, key=lambda r: r["dept"]):
    print(dept, [m["name"] for m in members])
# → eng ['Alice', 'Carol']
# → mkt ['Bob']

# combinations and permutations
print(list(itertools.combinations("ABC", 2)))
# → [('A', 'B'), ('A', 'C'), ('B', 'C')]
print(list(itertools.permutations("AB", 2)))
# → [('A', 'B'), ('B', 'A')]

# product — cartesian product (equivalent to nested for loops)
print(list(itertools.product([0, 1], repeat=3)))
# → [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)]
```

### `functools` — senior-level tools

```python
import functools

# lru_cache — memoization with size limit
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(50))               # → 12586269025 (instant, no exponential recursion)
print(fibonacci.cache_info())      # → CacheInfo(hits=48, misses=51, maxsize=128, currsize=51)
fibonacci.cache_clear()            # reset the cache


# partial — freeze some arguments of a function (currying-like)
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube   = functools.partial(power, exponent=3)
print(square(5))                   # → 25
print(cube(3))                     # → 27

# Works great for callbacks and map():
print(list(map(functools.partial(power, exponent=2), [1, 2, 3, 4])))
# → [1, 4, 9, 16]


# reduce — fold a sequence into a single value
from functools import reduce
product = reduce(lambda acc, x: acc * x, [1, 2, 3, 4, 5])
print(product)                     # → 120


# total_ordering — define only __eq__ + ONE comparison, get the rest for free
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)

v1 = Version(1, 5)
v2 = Version(2, 0)
print(v1 < v2)   # → True
print(v1 >= v2)  # → False  (auto-generated from __lt__ and __eq__)
```

### `pathlib` — modern file path handling

```python
from pathlib import Path

# Object-oriented paths — replaces os.path string manipulation
p = Path("/home/sumanth/projects")
data_file = p / "data" / "records.csv"   # / operator joins paths cleanly

print(data_file.name)          # → records.csv
print(data_file.stem)          # → records
print(data_file.suffix)        # → .csv
print(data_file.parent)        # → /home/sumanth/projects/data
print(data_file.exists())      # → True/False

# Glob — find files matching a pattern
for py_file in Path(".").glob("**/*.py"):   # recursive glob
    print(py_file)

# Reading/writing without explicit open()
config = Path("config.json")
config.write_text('{"key": "value"}')
print(config.read_text())      # → {"key": "value"}

# Create directories
Path("output/reports").mkdir(parents=True, exist_ok=True)
# parents=True → creates intermediate dirs; exist_ok=True → no error if exists
```

### `logging` — production-grade logging

```python
import logging

# Basic setup — always do this instead of print() in production code
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)   # always use __name__ for logger hierarchy

logger.debug("Detailed diagnostic info")
logger.info("Normal operation")
logger.warning("Something unexpected but non-fatal")
logger.error("Error occurred, operation failed")
logger.critical("System-level failure")

# Logging exceptions with full traceback
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Caught an error")   # → logs ERROR + full traceback automatically
```

### `enum` — safe named constants

```python
from enum import Enum, auto

class OrderStatus(Enum):
    PENDING   = auto()    # auto() assigns sequential int values
    CONFIRMED = auto()
    SHIPPED   = auto()
    DELIVERED = auto()
    CANCELLED = auto()

status = OrderStatus.PENDING
print(status)             # → OrderStatus.PENDING
print(status.value)       # → 1
print(status.name)        # → "PENDING"
print(status == OrderStatus.PENDING)    # → True

# Enums are iterable
for s in OrderStatus:
    print(s.name, s.value)

# Lookup by value — useful for deserializing from DB/API
status_from_db = OrderStatus(2)
print(status_from_db)     # → OrderStatus.CONFIRMED
```

---

## 4. Internals / how it works

- **`defaultdict`** is a subclass of `dict` that overrides `__missing__(key)` — when a key isn't found, instead of raising `KeyError`, it calls `self.default_factory()`, stores the result under the key, and returns it. The `default_factory` is just a callable stored as an instance attribute.
- **`Counter`** subclasses `dict` with `__missing__` returning `0` and arithmetic operators (`+`, `-`, `&`, `|`) defined to work element-wise. `most_common(n)` uses `heapq.nlargest` internally for efficiency.
- **`deque`** is implemented in C as a **doubly-linked list of fixed-size blocks** (not a circular array) — this gives true O(1) appendleft/popleft regardless of size, whereas `list.insert(0, x)` is O(n) because it shifts every element.
- **`lru_cache`** uses a dict (for O(1) lookup) combined with a doubly-linked list to maintain LRU order. Cache hits move the entry to the front; when `maxsize` is reached, the least-recently-used entry (at the back) is evicted. This is the classic LRU cache data structure — knowing this is a common interview question itself.
- **`itertools`** functions are implemented in C and return iterator objects — they produce values lazily, one at a time. Chaining them together creates a **pipeline of C-level iterators** with essentially no Python overhead per step, which is why they're dramatically faster than equivalent Python loops for large datasets.
- **`pathlib.Path`** uses `os.fspath()` under the hood, making `Path` objects acceptable anywhere a string path was previously expected (since Python 3.6, the `__fspath__` protocol). `Path` objects are immutable value-objects — `Path("/a") / "b"` creates a new `Path` object, it doesn't mutate.
- **`logging`** uses a **hierarchy of loggers** by name (`"app"` is parent of `"app.db"`) — log records propagate up to parent loggers unless `propagate=False`. Each logger has a level threshold, handlers (where output goes: file, stream, network), and formatters. This tree structure is why `logging.getLogger(__name__)` is the standard pattern — it automatically creates the right hierarchy matching your module structure.

---

## 5. Interview questions

**Q1: When would you use `defaultdict` vs `dict.get(key, default)` vs `dict.setdefault(key, default)`?**
A: `dict.get(key, default)` — read-only fallback; doesn't modify the dict; best for simple lookups where you don't want to store the default. `dict.setdefault(key, default)` — inserts the default if the key is missing AND returns it; useful for one-off initialization inside a function. `defaultdict(factory)` — auto-inserts on every access; best when you're building up a structure (grouping, counting) and every key-access should initialize it. Key trap: `defaultdict` creates entries on read (`d["missing"]` modifies `d`), which can bloat the dict unexpectedly when you just want a fallback without insertion.

**Q2: What's the complexity difference between `list` and `deque` for left-side operations, and why does it matter?**
A: `list.insert(0, x)` and `list.pop(0)` are **O(n)** because Python lists are dynamic arrays — inserting at the front requires shifting every element right. `deque.appendleft(x)` and `deque.popleft()` are **O(1)** because deque is a doubly-linked list of blocks. This matters for queues, sliding windows, and BFS implementations. However, `deque` random access (`dq[i]`) is **O(n)** while `list[i]` is O(1), so deque is specialized for front/back operations, not random access.

**Q3: What's the difference between `itertools.groupby` and a SQL `GROUP BY`, and what's the most common bug with it?**
A: SQL `GROUP BY` aggregates all matching rows regardless of their position. `itertools.groupby` groups **consecutive** elements — it only starts a new group when the key changes. If your data isn't sorted by the grouping key first, you'll get multiple groups for the same key value scattered through the output. The most common bug: forgetting to `sort(key=...)` before `groupby(key=...)` — `groupby` just compares adjacent elements, it doesn't scan the whole sequence.

**Q4: Why should production code use `logging` instead of `print()`?**
A: `print()` always goes to stdout with no level, no timestamp, no caller context, and can't be selectively enabled/disabled. `logging` provides: severity levels (filter debug in prod, enable in dev), structured output with timestamps and module names, multiple handlers (file + stream simultaneously), log rotation via `RotatingFileHandler`, propagation through a logger hierarchy, and zero-cost disabled-level calls (a `logger.debug()` call below the threshold doesn't even format the string). Senior-level code also uses `logger.exception()` inside `except` blocks to automatically capture the full traceback — `print(e)` loses it.

**Q5: What does `functools.partial` do, and how is it different from a lambda that does the same thing?**
A: Both create a callable with pre-filled arguments. `partial(pow, exponent=2)` is preferable because: it's introspectable (`partial_func.func`, `partial_func.keywords`), it preserves the original function's identity (useful for debugging), and it's implemented in C (faster). A lambda `lambda x: pow(x, exponent=2)` creates a new function object with its own scope lookup overhead and shows up in tracebacks as `<lambda>` with no context. `partial` is also composable — you can `partial` an already-`partial`'d function. Rule of thumb: `partial` for pre-filling arguments on existing functions; lambda for combining logic from multiple calls.

---

## 6. Practice problems

**Beginner:**
Given a list of words, use `collections.Counter` to find the top 3 most frequent words and print them with their counts. Then use `itertools.chain` to merge two word lists before counting. Finally, use `pathlib.Path` to write the results to `output/word_counts.txt`, creating the directory if it doesn't exist.
- Suggested filename: `stdlib_prac01_word_counter.py`
- Input: `["apple", "banana", "apple"]` + `["cherry", "apple", "banana", "banana"]`
- Output (file content): `apple: 3`, `banana: 3`, `cherry: 1`

**Senior:**
Build a **log file analyzer** using only the standard library:

1. Use `pathlib.Path` to read a multi-line log file where each line is: `"2024-01-15 10:23:45 [ERROR] auth: Invalid token"`.
2. Parse each line using `re` (covered later — for now use `.split()` with maxsplit) into a `namedtuple` or `dataclass` with fields: `timestamp (datetime)`, `level`, `module`, `message`.
3. Use `collections.defaultdict` to group log entries by `level`.
4. Use `itertools.groupby` (with correct pre-sorting) to group `ERROR` entries by `module`, and for each module print the count of errors and the most recent one.
5. Use `Counter` to find which module has the most errors overall.
6. Use `functools.reduce` to build a single summary string from all `CRITICAL` messages.
7. Write the full summary report to `output/log_report.txt` using `pathlib`, and log each step of your analysis using `logging` at appropriate levels.

- Suggested filename: `stdlib_prac02_log_analyzer.py`
- Provide a sample 10-line log file in the script itself (as a multiline string written to a temp file) to make it self-contained.

---

## 7. Common mistakes & senior traps

- **Using `dict` where `defaultdict` would eliminate `if key not in d` boilerplate** — juniors write `if word not in counts: counts[word] = 0; counts[word] += 1`; seniors write `defaultdict(int)` with just `counts[word] += 1`.

- **Accessing a `defaultdict` key just to check if it exists** — this inserts the default, silently growing your dict.
  ```python
  d = defaultdict(list)
  # WRONG — creates d["missing"] = [] as a side effect
  if d["missing"]:
      process(d["missing"])

  # RIGHT
  if "missing" in d:
      process(d["missing"])
  ```

- **Forgetting to sort before `itertools.groupby`** — the most common groupby bug, silently giving wrong results with no error (covered in Q3).

- **Using `list` as a queue** — `list.pop(0)` in a loop is O(n²) total. Use `deque` or `queue.Queue`.
  ```python
  # WRONG — O(n²) for n dequeues
  queue = [1, 2, 3, 4]
  while queue:
      item = queue.pop(0)    # O(n) each time!

  # RIGHT — O(n) total
  from collections import deque
  queue = deque([1, 2, 3, 4])
  while queue:
      item = queue.popleft()  # O(1)
  ```

- **Using `print()` in production code** instead of `logging` — interviewers specifically look for this as a seniority signal. Any code that ships should use `logging`.

- **Comparing `Enum` members by value instead of identity** — `OrderStatus.PENDING == 1` is `False` for regular `Enum` (use `IntEnum` if you need integer comparison), and using `==` instead of `is` for enum comparison can cause subtle bugs.
  ```python
  class Color(Enum):
      RED = 1

  Color.RED == 1        # → False  (Enum, not IntEnum)
  Color.RED == Color.RED  # → True
  Color.RED is Color.RED  # → True  (enums are singletons — `is` is preferred)
  ```

- **Misusing `lru_cache` on methods** — as discussed in the decorators topic, `self` becomes part of the cache key, keeping instances alive through the cache and causing memory leaks in long-lived objects. Use `functools.cached_property` for instance-level memoization instead.

- **Using `os.path` string operations when `pathlib` exists** — `os.path.join(base, "data", "file.csv")` is valid but harder to read and compose than `base / "data" / "file.csv"`. Mixing both styles in a codebase is a code-quality red flag.

---

Say **"next"** when you're ready for **Virtual Environments**, or ask for more practice problems on the standard library first.