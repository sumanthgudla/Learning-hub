# Topic 4: Output Parsers

---

## 1. What Is It?

Output Parsers transform raw LLM text responses into structured Python objects — strings, lists, dicts, or Pydantic models. At senior level, what matters is understanding **why parsing fails in production** (LLMs don't always follow instructions), **which parser to use for which job**, how to build **retry/fix logic** when the model returns malformed output, and how parsers plug into LCEL chains via the `format_instructions` pattern — because unstructured LLM output is unusable in real applications.

---

## 2. Core Concepts Table

| Parser | Input From LLM | Output Type | Best For |
|---|---|---|---|
| `StrOutputParser` | Any text | `str` | Simple text, most common |
| `CommaSeparatedListOutputParser` | `"a, b, c"` | `List[str]` | Quick lists, simple extraction |
| `JsonOutputParser` | JSON string | `dict` | Flexible structured data |
| `PydanticOutputParser` | JSON string | Pydantic model instance | Validated, typed structured output |
| `OutputFixingParser` | Malformed output | Fixed parsed result | Wrap any parser with auto-repair |
| `RetryOutputParser` | Failed parse | Retry with new LLM call | Re-ask model on parse failure |
| `.get_format_instructions()` | — | `str` (instructions for LLM) | Tells LLM exactly what format to produce |

---

## 3. Syntax & Code Examples

### Basic — `StrOutputParser`

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

chain = (
    ChatPromptTemplate.from_template("Explain {topic} in one sentence.")
    | ChatOpenAI(model="gpt-4o-mini")
    | StrOutputParser()   # extracts .content from AIMessage → plain str
)

result = chain.invoke({"topic": "recursion"})
print(result)        # → "Recursion is a function calling itself..."
print(type(result))  # → <class 'str'>
```

---

### `CommaSeparatedListOutputParser`

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()

# Always inject format instructions into the prompt
instructions = parser.get_format_instructions()
print(instructions)
# → "Your response should be a list of comma separated values,
#    eg: `foo, bar, baz`"

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "List 5 Python built-in functions.\n\n{format_instructions}")
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | parser

result = chain.invoke({"format_instructions": instructions})
print(result)        # → ['len', 'range', 'print', 'type', 'enumerate']
print(type(result))  # → <class 'list'>
```

---

### Real-World Pattern — `JsonOutputParser`

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Return only valid JSON. No explanation."),
    ("human", "Give me info about the Python language.\n\n{format_instructions}")
])

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | parser

result = chain.invoke({"format_instructions": parser.get_format_instructions()})
print(result)
# → {"name": "Python", "year": 1991, "creator": "Guido van Rossum", ...}
print(type(result))  # → <class 'dict'>
```

---

### Senior-Level — `PydanticOutputParser` with Validation

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# Step 1: Define your data shape with Pydantic
class CodeReview(BaseModel):
    summary: str          = Field(description="One sentence summary of the code")
    issues:  List[str]    = Field(description="List of issues found")
    score:   int          = Field(description="Quality score from 1 to 10")
    approved: bool        = Field(description="Whether the code is approved")

# Step 2: Create parser from the model
parser = PydanticOutputParser(pydantic_object=CodeReview)

# Step 3: Inject format instructions — this tells the LLM exactly what JSON to produce
print(parser.get_format_instructions())
# → "The output should be formatted as a JSON instance that conforms to the
#    JSON schema below..."  (includes full schema)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior code reviewer."),
    ("human",  "Review this code:\n{code}\n\n{format_instructions}")
])

chain = prompt | ChatOpenAI(model="gpt-4o", temperature=0) | parser

result = chain.invoke({
    "code": "def add(a, b): return a+b",
    "format_instructions": parser.get_format_instructions()
})

print(result)              # → CodeReview(summary='...', issues=[...], score=8, approved=True)
print(type(result))        # → <class '__main__.CodeReview'>
print(result.score)        # → 8        ← typed attribute access
print(result.approved)     # → True
print(result.issues)       # → ['No type hints', 'No docstring']
```

```
PydanticOutputParser Flow:
──────────────────────────────────────────────────────
  LLM Response (raw string):
  '{"summary": "Simple add function", "issues": [...],
    "score": 8, "approved": true}'
          │
          ▼
  Step 1: json.loads()  → Python dict
          │
          ▼
  Step 2: CodeReview(**dict)  → Pydantic validates types
          │           ┌─ score must be int ✓
          │           ├─ approved must be bool ✓
          │           └─ issues must be List[str] ✓
          ▼
  CodeReview instance (fully typed, validated)
──────────────────────────────────────────────────────
```

---

### Senior-Level — `OutputFixingParser` (Auto-Repair)

```python
from langchain.output_parsers import OutputFixingParser
from langchain_openai import ChatOpenAI

# Base parser that might fail on malformed output
base_parser = PydanticOutputParser(pydantic_object=CodeReview)

# Wrap it — on parse failure, sends the bad output + error back to LLM
# and asks it to fix the JSON
fixing_parser = OutputFixingParser.from_llm(
    parser=base_parser,
    llm=ChatOpenAI(model="gpt-4o-mini")  # can be a cheaper model
)

# Simulate malformed LLM output
bad_output = '{"summary": "good code", "issues": "no issues", "score": "8", "approved": "yes"}'
# issues should be List[str] not str
# score should be int not str
# approved should be bool not str

result = fixing_parser.parse(bad_output)
# Internally: tries base_parser → fails → sends to LLM with error message
# LLM returns corrected JSON → base_parser succeeds
print(result)       # → CodeReview(summary='good code', issues=['no issues'], score=8, approved=True)
```

```
OutputFixingParser Flow:
──────────────────────────────────────────────────────
  bad_output (malformed JSON string)
        │
        ▼
  base_parser.parse()  ──── success? ──→  return result
        │ ValidationError / JSONDecodeError
        ▼
  Send to LLM:
  "This output was supposed to match this schema.
   Here's the error: [error]. Fix it: [bad_output]"
        │
        ▼
  LLM returns corrected JSON string
        │
        ▼
  base_parser.parse()  ──── success? ──→  return result
        │ still fails?
        ▼
  raise final exception
──────────────────────────────────────────────────────
```

---

### Senior-Level — Streaming with `JsonOutputParser`

```python
# JsonOutputParser supports partial streaming — unique among parsers
chain = (
    ChatPromptTemplate.from_template(
        "Return a JSON object with keys: name, capital, population for {country}"
    )
    | ChatOpenAI(model="gpt-4o-mini", streaming=True)
    | JsonOutputParser()
)

# Yields partial dicts as tokens arrive — not just the final result
for partial in chain.stream({"country": "Japan"}):
    print(partial)
# → {}
# → {"name": ""}
# → {"name": "Japan"}
# → {"name": "Japan", "capital": ""}
# → {"name": "Japan", "capital": "Tokyo"}
# → {"name": "Japan", "capital": "Tokyo", "population": 125700000}
```

> This is powerful for UI — you can render partial results as they arrive rather than waiting for the full response.

---

## 4. Internals / How It Works

### The Parser Interface

Every parser implements `BaseOutputParser` with two key methods:

```
BaseOutputParser
├── .parse(text: str) → T          # core method — string in, typed object out
├── .get_format_instructions() → str  # what to inject into the prompt
└── .parse_with_prompt(text, prompt)  # used by RetryOutputParser
```

### How `PydanticOutputParser` Works Internally

```
.parse(text) called with LLM's raw string output
    │
    ▼
Step 1: Strip markdown fences if present
        (LLM often wraps JSON in ```json ... ```)
    │
    ▼
Step 2: json.loads(text)  → Python dict
        Raises: json.JSONDecodeError if malformed
    │
    ▼
Step 3: pydantic_object(**dict)
        Raises: pydantic.ValidationError if types wrong
    │
    ▼
Step 4: Return validated Pydantic instance
```

### Why `get_format_instructions()` Matters

Parsers are only as good as the prompt tells the LLM to be. Without injecting format instructions, the LLM returns whatever format it feels like:

```
Without instructions:  "The score is 8 out of 10 and it looks good."
With instructions:     '{"score": 8, "approved": true, "issues": [...]}'
```

`get_format_instructions()` generates a detailed schema description from your Pydantic model and injects it as part of the prompt — this is what makes structured output reliable.

---

## 5. Interview Questions

**Q1: When would you use `PydanticOutputParser` over `JsonOutputParser`?**

> Use `JsonOutputParser` when you want a flexible dict and don't need type validation — fast and simple. Use `PydanticOutputParser` when you need **guaranteed types and field validation** — the Pydantic model enforces that `score` is an `int`, not `"8"`, and that required fields are present. In production APIs where downstream code depends on types, always use `PydanticOutputParser`.

**Q2: What does `get_format_instructions()` do and why must you inject it into the prompt?**

> `get_format_instructions()` generates a string describing the exact JSON schema the LLM must produce — field names, types, and descriptions. Without injecting it, the LLM has no idea what format you expect and returns free text. It's the bridge between your parser's schema and the LLM's output.

**Q3: What's the difference between `OutputFixingParser` and `RetryOutputParser`?**

> `OutputFixingParser` takes the **bad output** and asks the LLM to fix it — one extra LLM call. `RetryOutputParser` discards the bad output entirely and **re-runs the original prompt** with a note that the previous attempt failed — it's a full retry. Use `OutputFixingParser` when the output is close but malformed; use `RetryOutputParser` when the output is completely wrong structurally.

**Q4: How does `JsonOutputParser` support partial streaming but `PydanticOutputParser` doesn't?**

> `JsonOutputParser` uses an incremental JSON parser that builds a partial dict as tokens arrive. `PydanticOutputParser` calls `pydantic_object(**dict)` which requires the complete JSON — a partial JSON string fails validation. For streaming + structured output, parse to dict first with `JsonOutputParser`, then validate the final result with Pydantic manually.

**Q5: What are the most common reasons output parsing fails in production?**

> Three main reasons: (1) **LLM adds markdown fences** — wraps JSON in ` ```json ``` ` which breaks `json.loads()`. (2) **LLM adds explanation text** before/after the JSON — `"Here is the result: {...}"`. (3) **Type mismatches** — LLM returns `"true"` as a string instead of `true` as a boolean. Solutions: use `OutputFixingParser` as a safety net, set `temperature=0` for structured tasks, and always include strong format instructions.

---

## 6. Practice Problems

### Beginner — `outputparsers_prac01_pydantic_extractor.py`

**Task:** Define a Pydantic model `MovieInfo` with fields:
- `title: str`
- `year: int`
- `genre: str`
- `rating: float`

Build an LCEL chain that takes `{"description": "..."}` and extracts structured movie info using `PydanticOutputParser`. Test with:
```
"The Dark Knight is a 2008 crime thriller directed by Nolan, rated 9.0 on IMDb"
```

**Expected:**
```python
MovieInfo(title='The Dark Knight', year=2008, genre='crime thriller', rating=9.0)
```

---

### Senior — `outputparsers_prac02_robust_pipeline.py`

**Task:** Build a robust code analysis pipeline that:
1. Defines a Pydantic model `CodeAnalysis` with:
   - `language: str`
   - `complexity: Literal["low", "medium", "high"]`
   - `bugs: List[str]`
   - `suggestions: List[str]`
   - `refactored_snippet: str`
2. Uses `PydanticOutputParser` wrapped in `OutputFixingParser`
3. Takes a code snippet as input and returns full analysis
4. After parsing, programmatically checks: if `complexity == "high"` or `len(bugs) > 2`, print a warning: `"⚠️ This code needs immediate attention"`
5. Test with a deliberately messy Python function

**Expected:**
```python
CodeAnalysis(language='Python', complexity='high', bugs=['...', '...', '...'],
             suggestions=[...], refactored_snippet='...')
⚠️ This code needs immediate attention
```

---

## 7. Common Mistakes & Senior Traps

- **Not injecting `format_instructions` into the prompt** — the single most common mistake. The parser has a schema; the LLM doesn't know about it unless you tell it.

```python
# WRONG — LLM returns free text, parser fails
prompt = ChatPromptTemplate.from_template("Review this code: {code}")
chain = prompt | model | PydanticOutputParser(pydantic_object=CodeReview)

# RIGHT — LLM knows exactly what to produce
prompt = ChatPromptTemplate.from_template(
    "Review this code: {code}\n\n{format_instructions}"
)
chain = prompt | model | parser
result = chain.invoke({
    "code": "...",
    "format_instructions": parser.get_format_instructions()
})
```

- **LLM wraps JSON in markdown fences** — `json.loads('```json\n{...}\n```')` raises `JSONDecodeError`. Modern LangChain parsers strip these automatically, but older versions don't. Always test with `temperature=0` and verify raw output.

- **Using `StrOutputParser` and parsing manually** — tempting but fragile. If the LLM adds a preamble, your manual `json.loads()` breaks. Use `JsonOutputParser` instead which handles this more robustly.

- **Pydantic v1 vs v2 mismatch** — LangChain supports both but the import paths differ. Using `from pydantic import BaseModel` when your env has Pydantic v2 but LangChain expects v1 causes subtle errors.

```python
# If you see Pydantic v2 warnings in LangChain, use:
from langchain_core.pydantic_v1 import BaseModel, Field
# instead of:
from pydantic import BaseModel, Field
```

- **Streaming with `PydanticOutputParser`** — it doesn't support partial streaming. Using `.stream()` with a Pydantic parser gives you the complete object in one chunk at the end — it won't yield partial results.

- **`OutputFixingParser` costs double** — every parse failure triggers a second LLM call. In high-volume production, this doubles your latency and cost on bad outputs. Always log fix attempts so you can improve your prompt and reduce failures over time.

---

## 🎉 All 4 Topics Complete!

Here's your full summary:

| # | Topic | Key Takeaway |
|---|---|---|
| 1 | Architecture Overview | Everything is a `Runnable`; LCEL `\|` composes them |
| 2 | Prompt Templates | `ChatPromptTemplate` + `MessagesPlaceholder` + `partial()` |
| 3 | LLM & Chat Model Integration | Swap models freely; use `with_fallbacks()` in prod |
| 4 | Output Parsers | `PydanticOutputParser` + `get_format_instructions()` + `OutputFixingParser` |

Let me know what you'd like to do next — more topics, practice problem help, or a combined project that uses all 4!