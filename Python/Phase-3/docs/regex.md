# Regex (Senior/Interview Level)

## 1. What is it

Regular expressions are a **mini-language for describing text patterns** — used for searching, validating, extracting, and transforming strings. Python's `re` module implements Perl-compatible regex (PCRE-lite). At senior level this isn't just "write a pattern that works" — it's understanding **how the regex engine works internally (backtracking, greedy vs lazy quantifiers), when regex is the wrong tool, compiled patterns vs inline calls, capturing groups vs non-capturing groups, lookaheads/lookbehinds, catastrophic backtracking, and the difference between `re.match`, `re.search`, `re.fullmatch`**. Interviewers use regex to test whether you understand both the power and the dangers of the tool.

---

## 2. Core concepts table

| Concept | Description |
|---|---|
| `re.compile(pattern)` | Pre-compile a pattern into a `Pattern` object — reuse for performance |
| `re.match(p, s)` | Match only at the **start** of the string |
| `re.search(p, s)` | Search **anywhere** in the string — first match |
| `re.fullmatch(p, s)` | Match must cover the **entire** string |
| `re.findall(p, s)` | Return list of all non-overlapping matches (strings) |
| `re.finditer(p, s)` | Return iterator of `Match` objects — lazy, memory efficient |
| `re.sub(p, r, s)` | Replace all matches with replacement string or callable |
| `re.split(p, s)` | Split string by pattern |
| `re.IGNORECASE` / `re.I` | Case-insensitive matching |
| `re.MULTILINE` / `re.M` | `^`/`$` match start/end of each LINE, not just whole string |
| `re.DOTALL` / `re.S` | `.` matches newlines too (by default `.` doesn't) |
| `re.VERBOSE` / `re.X` | Allow whitespace and `#` comments inside pattern for readability |
| `.` | Any character except newline (unless `DOTALL`) |
| `^` / `$` | Start / end of string (or line with `MULTILINE`) |
| `*` / `+` / `?` | Greedy: 0+, 1+, 0 or 1 matches |
| `*?` / `+?` / `??` | Lazy (non-greedy): match as few as possible |
| `{n,m}` | Between n and m repetitions |
| `[abc]` / `[^abc]` | Character class / negated class |
| `\d` / `\w` / `\s` | Digit / word char / whitespace (and `\D`, `\W`, `\S` = negated) |
| `\b` | Word boundary — zero-width assertion |
| `(...)` | Capturing group — accessible via `.group(n)` |
| `(?:...)` | Non-capturing group — groups without capturing |
| `(?P<name>...)` | Named capturing group — accessible via `.group("name")` |
| `(?=...)` | Positive lookahead — assert what follows, without consuming |
| `(?!...)` | Negative lookahead |
| `(?<=...)` | Positive lookbehind — assert what precedes |
| `(?<!...)` | Negative lookbehind |
| `\1` / `(?P=name)` | Backreference to captured group |
| `re.escape(s)` | Escape all special regex chars in a literal string |

---

## 3. Syntax & code examples

### Basic usage — match vs search vs fullmatch

```python
import re

text = "The price is $42.99 today"

# re.match — only matches at the START of the string
m = re.match(r"price", text)
print(m)              # → None  ("The" comes first, not "price")

m = re.match(r"The", text)
print(m.group())      # → "The"

# re.search — finds FIRST match ANYWHERE in string
m = re.search(r"\$[\d.]+", text)   # \$ escapes the literal dollar sign
print(m.group())      # → "$42.99"
print(m.start())      # → 13  (index where match starts)
print(m.end())        # → 19  (index after match ends)
print(m.span())       # → (13, 19)

# re.fullmatch — entire string must match the pattern
m = re.fullmatch(r"\d{4}-\d{2}-\d{2}", "2024-01-15")
print(m.group())      # → "2024-01-15"

m = re.fullmatch(r"\d{4}-\d{2}-\d{2}", "2024-01-15 extra")
print(m)              # → None  (extra content at end fails fullmatch)

# findall — returns list of match strings
prices = re.findall(r"\$[\d.]+", "Pay $10.99 or $5.00 today")
print(prices)         # → ['$10.99', '$5.00']

# finditer — lazy iterator of Match objects (better for large strings)
for m in re.finditer(r"\$[\d.]+", "Pay $10.99 or $5.00"):
    print(f"Found {m.group()} at position {m.start()}")
# → Found $10.99 at position 4
# → Found $5.00 at position 14
```

### Capturing groups — the most used feature in real code

```python
import re

# Numbered capturing groups — accessed by position
log_line = "2024-01-15 10:23:45 ERROR auth: Invalid token for user@example.com"

pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (\w+): (.+)"
m = re.match(pattern, log_line)

if m:
    print(m.group(0))   # → entire match (same as m.group())
    print(m.group(1))   # → "2024-01-15"    (first group)
    print(m.group(2))   # → "10:23:45"      (second group)
    print(m.group(3))   # → "ERROR"
    print(m.groups())   # → ('2024-01-15', '10:23:45', 'ERROR', 'auth', 'Invalid...')


# Named capturing groups — (?P<name>...) — far more readable and maintainable
pattern = r"""
    (?P<date>\d{4}-\d{2}-\d{2})   # date field
    \s+
    (?P<time>\d{2}:\d{2}:\d{2})   # time field
    \s+
    (?P<level>\w+)                 # log level
    \s+
    (?P<module>\w+):               # module name
    \s+
    (?P<message>.+)                # rest of message
"""

m = re.match(pattern, log_line, re.VERBOSE)
if m:
    print(m.group("date"))     # → "2024-01-15"
    print(m.group("level"))    # → "ERROR"
    print(m.groupdict())
    # → {'date': '2024-01-15', 'time': '10:23:45', 'level': 'ERROR',
    #    'module': 'auth', 'message': 'Invalid token for user@example.com'}


# Non-capturing groups (?:...) — group without capturing
# Use when you need to group for alternation/quantifier but don't need the value
pattern = r"(?:https?|ftp)://[\w./]+"    # group "https?" and "ftp" for alternation
                                          # but don't capture the protocol separately
urls = re.findall(pattern, "Visit https://example.com or ftp://files.example.com")
print(urls)  # → ['https://example.com', 'ftp://files.example.com']


# re.sub with capturing groups — powerful transformation tool
# \1 refers to first captured group in replacement string
result = re.sub(
    r"(\w+)@(\w+)\.(\w+)",         # capture: user, domain, tld
    r"\1 [at] \2 [dot] \3",        # rearrange in replacement
    "Contact me: alice@example.com"
)
print(result)   # → "Contact me: alice [at] example [dot] com"

# re.sub with a CALLABLE replacement — even more powerful
def mask_email(m):
    user = m.group(1)
    domain = m.group(2)
    tld = m.group(3)
    return f"{user[0]}***@{domain}.{tld}"   # mask everything after first char

result = re.sub(r"(\w+)@(\w+)\.(\w+)", mask_email, "alice@example.com")
print(result)   # → "a***@example.com"
```

### Senior-level / non-obvious usage: lookaheads, lookbehinds, compiled patterns, flags

```python
import re

# ── LOOKAHEADS & LOOKBEHINDS ────────────────────────────────────────────────
# These are ZERO-WIDTH assertions — they check context without consuming characters

# Positive lookahead (?=...) — match X only if followed by Y
text = "100USD 200GBP 300EUR"
amounts = re.findall(r"\d+(?=USD)", text)    # digits followed by USD
print(amounts)    # → ['100']  (only the USD amount)

# Negative lookahead (?!...) — match X only if NOT followed by Y
amounts = re.findall(r"\d+(?!USD|GBP|EUR)", text)
# → ['10', '20', '30']  ← WRONG! Matches partial numbers
amounts = re.findall(r"\d+(?!\d)(?!USD|GBP|EUR)", text)
# tricky — lookaheads take care with word boundaries

# Positive lookbehind (?<=...) — match X only if preceded by Y
prices = re.findall(r"(?<=\$)\d+\.?\d*", "Costs $42.99 and $100")
print(prices)     # → ['42.99', '100']  (numbers after $, not including $)

# Negative lookbehind (?<!...) — match X only if NOT preceded by Y
# Find standalone numbers not preceded by $ 
nums = re.findall(r"(?<!\$)\b\d+\b", "Total: $42 items: 10 cost: $5")
print(nums)       # → ['10']  (only '10' is not preceded by $)


# ── COMPILED PATTERNS — always compile when reusing ────────────────────────
# re.compile() returns a Pattern object — same methods, but pattern compiled once
EMAIL_RE = re.compile(
    r"""
    (?P<user>[a-zA-Z0-9._%+-]+)   # username part
    @                              # literal @
    (?P<domain>[a-zA-Z0-9.-]+)    # domain
    \.                             # literal dot
    (?P<tld>[a-zA-Z]{2,})         # TLD: 2+ letters
    """,
    re.VERBOSE | re.IGNORECASE    # combine flags with |
)

# Now use it as a method on the pattern object
m = EMAIL_RE.fullmatch("Alice@Example.COM")
print(m.groupdict())
# → {'user': 'Alice', 'domain': 'Example', 'tld': 'COM'}

emails = EMAIL_RE.findall("contact alice@ex.com or bob@test.org please")
# NOTE: findall with groups returns LIST OF TUPLES of groups, not full matches!
print(emails)   # → [('alice', 'ex', 'com'), ('bob', 'test', 'org')]
# → to get full matches use finditer instead:
for m in EMAIL_RE.finditer("contact alice@ex.com or bob@test.org please"):
    print(m.group())    # → alice@ex.com, bob@test.org


# ── MULTILINE AND DOTALL FLAGS ──────────────────────────────────────────────
text = """ERROR: disk full
WARNING: low memory
ERROR: connection refused"""

# Without MULTILINE: ^ only matches start of ENTIRE string
errors = re.findall(r"^ERROR: .+", text)
print(errors)   # → ['ERROR: disk full']  (only first line!)

# With MULTILINE: ^ matches start of EACH LINE
errors = re.findall(r"^ERROR: .+", text, re.MULTILINE)
print(errors)   # → ['ERROR: disk full', 'ERROR: connection refused']

# DOTALL: . matches newlines too
html = "<div>\n  <p>Hello</p>\n</div>"
m = re.search(r"<div>(.+)</div>", html, re.DOTALL)
print(m.group(1) if m else None)
# → "\n  <p>Hello</p>\n"  (. matched newlines)


# ── GREEDY VS LAZY ──────────────────────────────────────────────────────────
html = "<b>bold</b> and <b>more bold</b>"

# Greedy — .+ matches as MUCH as possible, then backtracks
m = re.search(r"<b>.+</b>", html)
print(m.group())    # → "<b>bold</b> and <b>more bold</b>"  (too much!)

# Lazy — .+? matches as LITTLE as possible
m = re.search(r"<b>.+?</b>", html)
print(m.group())    # → "<b>bold</b>"  (stops at first </b>)

# Find ALL bold sections:
print(re.findall(r"<b>.+?</b>", html))
# → ['<b>bold</b>', '<b>more bold</b>']


# ── re.split ────────────────────────────────────────────────────────────────
# Split on multiple delimiters at once
parts = re.split(r"[,;\s]+", "alice, bob;carol   dave")
print(parts)    # → ['alice', 'bob', 'carol', 'dave']

# re.escape — safely use literal strings as regex patterns
user_input = "Hello (world) $100"   # contains regex special chars
safe = re.escape(user_input)        # → "Hello\ \(world\)\ \$100"
m = re.search(safe, "Say Hello (world) $100 today")
print(m.group() if m else None)     # → "Hello (world) $100"
```

**ASCII view — greedy vs lazy backtracking:**

```
Input:  "<b>bold</b> and <b>more</b>"
        0123456789...

Greedy pattern: <b>.+</b>
  Engine tries .+ → matches EVERYTHING to end of string
  Then backtracks char by char looking for </b>
  Finds last </b> → returns longest possible match:
  "<b>bold</b> and <b>more</b>"
         ↑ starts here            ↑ ends here (last </b>)

Lazy pattern: <b>.+?</b>
  Engine tries .+ → matches ONE char ("b")
  Then checks: is next </b>? No → expand one more char
  Keeps expanding until </b> found
  Stops at FIRST </b>:
  "<b>bold</b>"
         ↑    ↑ stops at first </b>

Backtracking flow (greedy):
<b>.+</b> on "<b>X</b>Y</b>"
  .+ grabs: "X</b>Y</b>"   → look for </b> at end? No, backtrack
  .+ grabs: "X</b>Y</b"    → look for </b>? No, backtrack
  ...
  .+ grabs: "X"             → look for </b>? YES → match: <b>X</b>Y</b>
  (greedy matched LAST </b>, lazy would stop at FIRST)
```

---

## 4. Internals / how it works

- Python's `re` module uses a **backtracking NFA (Non-deterministic Finite Automaton)** engine. The engine tries to match the pattern against the input left-to-right, and when it has a choice (from `*`, `+`, `|`, etc.), it makes a **greedy** choice first (or lazy if `?` suffix), then **backtracks** to try alternatives if the greedy choice doesn't lead to an overall match. This backtracking is the key to both regex's power and its performance pitfalls.
- **Catastrophic backtracking** occurs when a poorly-written pattern causes exponential backtracking. The classic example: `(a+)+` on input `"aaaaaab"` — the engine tries every possible way to split the `a`s between the inner and outer `+`, which is exponential in the number of `a`s. This is a real **ReDoS (Regular Expression Denial of Service)** vulnerability in production systems that accept user-provided input.
- `re.compile()` converts the pattern string into a compiled `Pattern` object (a state machine) once. Without `compile()`, calling `re.search(pattern, string)` recompiles the pattern every call (though CPython caches the last ~512 compiled patterns in an internal LRU cache, so the practical difference is smaller than you'd expect for repeated identical patterns — but compile explicitly for large-scale processing or when you want the pattern object's methods).
- Named groups `(?P<name>...)` are stored in the match object's internal dict and accessible via `m.group("name")` or `m.groupdict()`. The `(?P=name)` syntax creates a **backreference** to a named group — useful for matching repeated tokens like `<div>...</div>` with `(?P<tag>\w+)>.*?</(?P=tag)>`.
- **Lookaheads and lookbehinds are zero-width assertions** — they don't consume characters or move the engine's position in the string. They assert a condition about the surroundings without including those surroundings in the match. Lookbehinds in Python must be **fixed-width** — `(?<=\d{2,3})` is not allowed because the engine needs to know exactly how far back to look. Use `(?<=\d\d)` or `(?<=\d\d\d)` instead.
- The `re.VERBOSE` flag (`re.X`) strips **unescaped whitespace and `#`-to-end-of-line comments** from the pattern before compiling. This lets you write readable, documented patterns across multiple lines — one of the most underused features of the `re` module.

---

## 5. Interview questions

**Q1: What is the difference between `re.match()`, `re.search()`, and `re.fullmatch()`? What's the most common mistake with `re.match()`?**
A: `re.match()` only checks for a match at the **beginning** of the string — it's equivalent to anchoring the pattern with `^`. `re.search()` scans through the string and returns the first match found **anywhere**. `re.fullmatch()` requires the **entire string** to match the pattern — equivalent to anchoring with both `^` and `$`. The most common mistake: using `re.match(r"\d+", "abc123")` and expecting it to find `123` — it returns `None` because `match` only checks the start. Another common mistake: assuming `re.match(r"\d+", "123abc")` means the entire string is digits — it matches `123` at the start but ignores `abc` at the end. Use `fullmatch` for validation.

**Q2: What is greedy vs lazy matching, and when does the distinction matter?**
A: A **greedy** quantifier (`*`, `+`, `?`, `{n,m}`) matches **as many characters as possible**, then backtracks if needed. A **lazy** quantifier (add `?`: `*?`, `+?`, `??`) matches **as few characters as possible**, expanding only if needed. The distinction matters when the pattern could match multiple sub-strings of different lengths. Classic example: parsing HTML tags — `<.+>` greedily matches `<b>text</b>` all the way to the last `>`, while `<.+?>` lazily stops at the first `>`. In practice: use lazy quantifiers when extracting content between delimiters, use greedy when you want the longest possible match. Always consider whether the input is well-structured enough for regex — HTML/XML parsing should generally use a proper parser (`BeautifulSoup`, `lxml`), not regex.

**Q3: What is catastrophic backtracking and how do you avoid it?**
A: Catastrophic backtracking (ReDoS) happens when a regex pattern causes the engine to try an **exponential number of paths** through the input before failing. The canonical example: `(a+)+b` on `"aaaaaac"` — for n `a`s, there are 2^(n-1) ways to partition them among the nested groups, all of which fail when `b` isn't found. The engine tries every partition before giving up — this is O(2^n). Prevention: (1) Avoid **nested quantifiers** like `(x+)+` or `(x*)*`; (2) Use **possessive quantifiers** or **atomic groups** when available (Python's `re` doesn't support them, but `regex` module does); (3) Use **character classes** instead of `.+` when you know what characters to expect (`[^<]+` instead of `.+` for "non-angle-bracket characters"); (4) Set a timeout on regex operations for user-supplied patterns; (5) Use the `regex` module which supports atomic groups and possessive quantifiers.

**Q4: What's the difference between a capturing group `(...)` and a non-capturing group `(?:...)`? When should you use each?**
A: Both group sub-patterns for quantifiers or alternation. **Capturing groups** additionally store their matched text in the match object, accessible via `.group(n)` and included in `findall()` results. **Non-capturing groups** `(?:...)` purely control parsing/grouping without storing the match — they're slightly faster and don't pollute the group numbering. Use capturing groups when you need the matched text later; use non-capturing when you only need the grouping for a quantifier or alternation (`(?:https?|ftp)://`). A key gotcha: `re.findall()` with capturing groups returns **a list of tuples of group strings** instead of a list of full match strings — this surprises developers who add a capturing group for readability and suddenly get a different return type.

**Q5: When should you NOT use regex, and what should you use instead?**
A: Regex is wrong when: (1) **Parsing structured formats** — HTML/XML should use `BeautifulSoup`/`lxml` (regex can't handle nesting); JSON should use `json.loads()`; CSV should use `csv.DictReader` (quoted fields with embedded commas defeat regex). (2) **Simple string operations are enough** — `"ERROR" in line`, `line.startswith("2024")`, `line.split(",")` are faster, more readable, and less error-prone than equivalent regex for simple cases. (3) **You need to maintain the pattern** — a regex for a complex validation rule becomes unmaintainable; write a function with explicit conditionals instead. Rule of thumb: reach for regex when you need **pattern matching with wildcards/quantifiers** on text you don't control the structure of; reach for string methods for anything that can be expressed simply as splits, starts/endswith, or `in` checks.

---

## 6. Practice problems

**Beginner:**
Write a function `parse_log_line(line)` that uses a **named-group regex** to parse log lines in the format:
`"2024-01-15 10:23:45 [ERROR] auth.service: Login failed for user: alice@example.com"`

Return a dict with keys: `date`, `time`, `level`, `module`, `message`. Handle lines that don't match by returning `None`. Test with at least 3 valid lines and 1 invalid line. Compile the pattern outside the function (at module level).

- Suggested filename: `regex_prac01_log_parser.py`
- Input: `"2024-01-15 10:23:45 [ERROR] auth.service: Login failed"`
- Output: `{'date': '2024-01-15', 'time': '10:23:45', 'level': 'ERROR', 'module': 'auth.service', 'message': 'Login failed'}`

**Senior:**
Build a **text sanitization and extraction pipeline** that processes a block of raw user-submitted text and performs the following operations using regex (each as a separate compiled pattern + function):

1. `extract_emails(text)` → list of unique emails, case-normalized to lowercase, validated against a proper email regex (handle dots, plus signs, subdomains; reject obvious invalids like `@.com`)
2. `extract_urls(text)` → list of URLs (http/https/ftp), handling URLs with query strings and fragments, excluding trailing punctuation (`.`, `,`, `)`) that's likely not part of the URL
3. `mask_phone_numbers(text)` → return text with all phone numbers replaced by `[PHONE]`; handle formats: `+91-98765-43210`, `(123) 456-7890`, `123-456-7890`, `1234567890` (10+ digits)
4. `normalize_whitespace(text)` → collapse all runs of whitespace (spaces, tabs, newlines) into a single space; strip leading/trailing
5. `extract_key_value_pairs(text)` → extract `key=value` or `key: value` pairs from text (keys are `\w+`, values run until next pair or end of line); return a dict
6. Chain all of them in a `sanitize(text)` function that: extracts emails + URLs first (before masking), masks phones, normalizes whitespace, and returns `{"emails": [...], "urls": [...], "cleaned_text": "..."}`
7. Write tests for each function including edge cases: email with `+` sign, URL with query string, phone with country code, empty input, text with no matches

- Suggested filename: `regex_prac02_text_sanitizer.py`
- Test input: a realistic paragraph containing emails, URLs, phone numbers, and messy whitespace

---

## 7. Common mistakes & senior traps

- **Using `re.match` when you meant `re.search`** — `match` only checks the start, which trips up developers expecting it to find a pattern anywhere in the string.
  ```python
  # WRONG assumption
  m = re.match(r"\d+", "abc 123")
  print(m)         # → None  ("abc" is at the start, not digits)

  # RIGHT
  m = re.search(r"\d+", "abc 123")
  print(m.group()) # → "123"
  ```

- **Using `re.findall` with capturing groups and getting unexpected tuple results:**
  ```python
  # WRONG — developer expects list of full matches
  results = re.findall(r"(\d+)-(\w+)", "42-hello 99-world")
  print(results)   # → [('42', 'hello'), ('99', 'world')]  ← tuples, not strings!

  # RIGHT — use non-capturing group if you don't need the parts separately
  results = re.findall(r"\d+-\w+", "42-hello 99-world")
  print(results)   # → ['42-hello', '99-world']

  # OR use finditer to get full match + access groups
  for m in re.finditer(r"(\d+)-(\w+)", "42-hello 99-world"):
      print(m.group(), m.group(1), m.group(2))
  ```

- **Not escaping user input before using it in a pattern** — if a user provides a search string that contains regex special chars (`(`, `.`, `*`, `+`), it will be interpreted as regex syntax.
  ```python
  user_query = "hello (world)"

  # WRONG — ( is unmatched, raises re.error
  re.search(user_query, text)

  # RIGHT — always escape literal strings from external input
  re.search(re.escape(user_query), text)
  ```

- **Using `.` when you mean "any character" in HTML/multiline content** — `.` doesn't match newlines by default, silently failing on multi-line content.
  ```python
  html = "<div>\nContent\n</div>"

  # WRONG — . doesn't cross newlines
  m = re.search(r"<div>(.+)</div>", html)
  print(m)    # → None

  # RIGHT — use re.DOTALL
  m = re.search(r"<div>(.+)</div>", html, re.DOTALL)
  print(m.group(1))   # → "\nContent\n"
  ```

- **Catastrophic backtracking with nested quantifiers on user input** — a real security risk in production.
  ```python
  # DANGEROUS — nested quantifier on unconstrained input
  pattern = re.compile(r"(a+)+b")
  # pattern.search("a" * 30 + "c")  # hangs for seconds!

  # SAFER — restrict character class, avoid nesting
  pattern = re.compile(r"a+b")
  ```

- **Forgetting `re.MULTILINE` when matching line-by-line patterns** — `^` and `$` match the start/end of the ENTIRE string by default.
  ```python
  text = "start\nmiddle\nend"

  re.findall(r"^\w+", text)               # → ['start']  (only first line)
  re.findall(r"^\w+", text, re.MULTILINE) # → ['start', 'middle', 'end']
  ```

- **Using regex for JSON, HTML, CSV, or URL parsing** — these are structured formats with parsers specifically designed for their edge cases. Regex will handle 90% of cases and silently fail on the other 10%.
  ```python
  # WRONG — regex for HTML parsing
  emails = re.findall(r"<a href='(.+?)'>", html)   # breaks on double quotes, spaces

  # RIGHT — use a proper parser
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html, "html.parser")
  emails = [a["href"] for a in soup.find_all("a")]
  ```

- **Not compiling patterns used in loops** — even with CPython's internal cache, explicitly compiling patterns used in hot loops is cleaner and guaranteed to avoid re-compilation overhead.
  ```python
  # WRONG — technically re-compiles if cache is evicted
  for line in millions_of_lines:
      m = re.search(r"\d{4}-\d{2}-\d{2}", line)

  # RIGHT — compile once outside the loop
  DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
  for line in millions_of_lines:
      m = DATE_RE.search(line)
  ```

---

Say **"next"** when you're ready for **Unittest**, or ask for more practice problems on regex first.