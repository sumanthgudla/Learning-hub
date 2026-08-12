# HTTP Requests (Senior/Interview Level)

## 1. What is it

HTTP requests in Python means making your code **talk to the outside world** — calling REST APIs, webhooks, external services, and microservices. The standard tool is the third-party `requests` library (so dominant it's practically stdlib), with `httpx` as the modern async-capable alternative. At senior level this isn't just "call `requests.get(url)`" — it's understanding **connection pooling, sessions, timeouts (the most commonly forgotten production necessity), retry strategies with backoff, authentication patterns, streaming large responses, mocking in tests, and the difference between sync and async HTTP**. Interviewers use this topic to probe whether you think about **network reliability and production robustness**, not just happy-path API calls.

---

## 2. Core concepts table

| Concept | Description |
|---|---|
| `requests.get/post/put/patch/delete` | One-shot HTTP methods — creates a new connection each call |
| `requests.Session` | Reuses connections (connection pooling), persists headers/cookies/auth across requests |
| `response.json()` | Parse response body as JSON — raises `JSONDecodeError` if body isn't valid JSON |
| `response.text` | Response body as a string (decoded by detected charset) |
| `response.content` | Response body as raw bytes |
| `response.raise_for_status()` | Raises `HTTPError` for 4xx/5xx responses — always call this |
| `timeout=` | Tuple `(connect_timeout, read_timeout)` — ALWAYS set this |
| `params=` | Dict of query string parameters — auto-encoded |
| `json=` | Pass a dict — auto-serializes to JSON + sets `Content-Type: application/json` |
| `data=` | Form-encoded body (`application/x-www-form-urlencoded`) |
| `headers=` | Dict of request headers |
| `auth=` | Auth handler: `(user, pass)` for Basic, or custom `AuthBase` subclass |
| `stream=True` | Stream response body — don't load into memory all at once |
| `verify=` | SSL certificate verification — never set `False` in production |
| `HTTPAdapter` | Customize connection pooling, retry behavior, SSL settings per session |
| `urllib3.Retry` | Retry policy with backoff — attach via `HTTPAdapter` |
| `httpx` | Modern alternative: sync + async, HTTP/2, type hints, better API |
| `responses` / `httpretty` | Libraries for mocking HTTP calls in tests |
| `unittest.mock.patch` | Mock `requests` at the module level in tests |
| Status codes | 2xx success, 3xx redirect, 4xx client error, 5xx server error |
| Connection pooling | Reusing TCP connections across requests — massive performance win |

---

## 3. Syntax & code examples

### Basic usage

```python
import requests

# Simple GET request
response = requests.get("https://api.github.com/users/torvalds")

print(response.status_code)          # → 200
print(response.headers["Content-Type"])  # → application/json; charset=utf-8
print(response.url)                  # → final URL after any redirects

# Parse JSON response
data = response.json()
print(data["name"])                  # → Linus Torvalds
print(data["public_repos"])          # → 6 (or however many he has)

# ALWAYS check for HTTP errors — status_code 200 is not guaranteed
response.raise_for_status()          # raises requests.HTTPError for 4xx/5xx
# Without this, a 404 or 500 silently returns a response object — a common bug

# Query parameters — pass as dict, requests handles encoding
params = {"q": "python requests", "sort": "stars", "order": "desc"}
response = requests.get(
    "https://api.github.com/search/repositories",
    params=params
)
print(response.url)
# → https://api.github.com/search/repositories?q=python+requests&sort=stars&order=desc

# POST with JSON body
payload = {"name": "test-repo", "private": True, "description": "Test"}
response = requests.post(
    "https://api.github.com/user/repos",
    json=payload,                    # auto-serializes dict + sets Content-Type header
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
response.raise_for_status()
print(response.status_code)          # → 201 Created
```

### Always set timeouts — the #1 production oversight

```python
import requests

# WRONG — no timeout = your program can hang forever waiting for a response
response = requests.get("https://slow-api.example.com/data")

# RIGHT — always pass timeout
# timeout=(connect_seconds, read_seconds)
# connect: how long to wait to establish TCP connection
# read:    how long to wait between bytes once connected
response = requests.get(
    "https://api.example.com/data",
    timeout=(3.05, 10)    # 3.05s to connect, 10s to read
    # 3.05 is intentionally slightly above 3 — avoids race with TCP's 3s retry
)

# Or a single float = SAME timeout for both connect and read
response = requests.get("https://api.example.com/data", timeout=5)

# Handle timeout exceptions
from requests.exceptions import Timeout, ConnectionError, HTTPError

try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()
    data = response.json()
except Timeout:
    print("Request timed out — service may be slow or down")
except ConnectionError:
    print("Could not reach the server — check network/DNS")
except HTTPError as e:
    print(f"HTTP error: {e.response.status_code} — {e.response.text[:200]}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Common real-world pattern: `Session` with auth, headers, and connection pooling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def build_api_session(base_url: str, api_key: str) -> requests.Session:
    """
    Build a production-ready session with:
    - Persistent auth headers (no need to repeat per request)
    - Connection pooling (reuses TCP connections — huge perf win for many requests)
    - Automatic retry with exponential backoff for transient failures
    """
    session = requests.Session()

    # Persistent headers applied to every request in this session
    session.headers.update({
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "MyApp/1.0",
        "X-Request-ID": "auto",      # could generate UUIDs per-request too
    })

    # Retry policy: retry on 429 (rate limit), 500, 502, 503, 504
    retry_strategy = Retry(
        total=3,                      # max 3 retries
        backoff_factor=1,             # waits: 1s, 2s, 4s between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],   # also retry POSTs (careful — idempotency!)
        raise_on_status=False         # don't raise on retry-able status — let Retry handle
    )

    # Mount the adapter for both http and https
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,          # number of connection pools
        pool_maxsize=20,              # connections per pool
    )
    session.mount("https://", adapter)
    session.mount("http://",  adapter)

    return session


# Usage — session reuses connections across all requests
session = build_api_session("https://api.example.com", api_key="sk-abc123")

# All requests inherit the session's headers, auth, and retry policy
r1 = session.get("/users", timeout=10)           # GET https://api.example.com/users
r2 = session.post("/orders", json={...}, timeout=10)

# Use as context manager — ensures connection pool is properly closed
with build_api_session("https://api.example.com", "sk-abc") as session:
    response = session.get("/data", timeout=10)
    response.raise_for_status()
```

### Senior-level / non-obvious usage: streaming, pagination, auth classes, httpx async

```python
import requests

# ── STREAMING LARGE RESPONSES ──────────────────────────────────────────────
# stream=True delays downloading body until you consume it
# Use for large files, huge API responses, server-sent events

def download_file(url: str, dest_path: str, chunk_size: int = 8192):
    """Download a file without loading it all into memory."""
    with requests.get(url, stream=True, timeout=(5, None)) as response:
        # timeout=(connect, None) = 5s to connect, no read timeout for streaming
        response.raise_for_status()

        total = int(response.headers.get("Content-Length", 0))
        downloaded = 0

        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:              # filter out keep-alive empty chunks
                    f.write(chunk)
                    downloaded += len(chunk)
                    pct = downloaded / total * 100 if total else 0
                    print(f"\r{pct:.1f}% downloaded", end="")
    print(f"\nSaved to {dest_path}")


# ── AUTOMATIC PAGINATION ────────────────────────────────────────────────────
def paginate(session: requests.Session, url: str, **kwargs):
    """
    Generic paginator that follows GitHub-style Link header pagination.
    Yields one page of results at a time — lazy, memory-efficient.
    """
    while url:
        response = session.get(url, **kwargs)
        response.raise_for_status()
        yield response.json()

        # GitHub puts next page URL in Link header:
        # Link: <https://api.github.com/...?page=2>; rel="next"
        links = response.links               # requests parses Link headers automatically
        url = links.get("next", {}).get("url")   # None when last page reached

with requests.Session() as session:
    session.headers["Authorization"] = "Bearer TOKEN"
    all_repos = []
    for page in paginate(session, "https://api.github.com/user/repos", timeout=10):
        all_repos.extend(page)
        print(f"Fetched {len(all_repos)} repos so far")


# ── CUSTOM AUTH CLASS ───────────────────────────────────────────────────────
from requests.auth import AuthBase

class HMACAuth(AuthBase):
    """Custom auth that signs requests with HMAC — common in payment APIs."""
    def __init__(self, api_key: str, secret: str):
        self.api_key = api_key
        self.secret = secret

    def __call__(self, request):
        import hmac, hashlib, time
        timestamp = str(int(time.time()))
        message = f"{timestamp}{request.method}{request.path_url}"
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        request.headers["X-API-Key"]   = self.api_key
        request.headers["X-Timestamp"] = timestamp
        request.headers["X-Signature"] = signature
        return request                 # MUST return the request

session.auth = HMACAuth("key123", "supersecret")
response = session.get("https://payment-api.example.com/charges", timeout=5)


# ── ASYNC HTTP WITH httpx ───────────────────────────────────────────────────
import httpx
import asyncio

async def fetch_all(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs CONCURRENTLY — much faster than sequential requests."""
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)  # fires all requests simultaneously
        results = []
        for r in responses:
            r.raise_for_status()
            results.append(r.json())
        return results

urls = [
    "https://api.github.com/users/torvalds",
    "https://api.github.com/users/gvanrossum",
    "https://api.github.com/users/kennethreitz",
]
results = asyncio.run(fetch_all(urls))
# Fetches all 3 in ~parallel — total time ≈ slowest single request, not sum of all 3
```

### Mocking HTTP in tests — the right way

```python
# The two main approaches: `responses` library and `unittest.mock`

# ── Approach 1: `responses` library (cleanest for requests) ─────────────────
# pip install responses
import responses as responses_mock
import requests

@responses_mock.activate
def test_get_user_success():
    # Register a fake response BEFORE making the request
    responses_mock.add(
        method=responses_mock.GET,
        url="https://api.example.com/users/1",
        json={"id": 1, "name": "Alice"},
        status=200
    )

    response = requests.get("https://api.example.com/users/1", timeout=5)
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"
    assert len(responses_mock.calls) == 1  # verify exactly one call was made


@responses_mock.activate
def test_get_user_not_found():
    responses_mock.add(
        method=responses_mock.GET,
        url="https://api.example.com/users/999",
        json={"error": "Not found"},
        status=404
    )
    response = requests.get("https://api.example.com/users/999", timeout=5)
    assert response.status_code == 404


# ── Approach 2: unittest.mock.patch (no extra dependency) ──────────────────
from unittest.mock import patch, MagicMock

def get_user(user_id: int) -> dict:
    response = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)
    response.raise_for_status()
    return response.json()

def test_get_user_mocked():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    mock_response.raise_for_status.return_value = None   # don't raise

    with patch("requests.get", return_value=mock_response) as mock_get:
        result = get_user(1)
        mock_get.assert_called_once_with(
            "https://api.example.com/users/1",
            timeout=5
        )
        assert result["name"] == "Alice"
```

**ASCII view — Session connection pooling vs one-shot requests:**

```
WITHOUT Session (one-shot requests.get calls):
  Request 1: DNS lookup → TCP handshake → TLS handshake → send → receive → CLOSE
  Request 2: DNS lookup → TCP handshake → TLS handshake → send → receive → CLOSE
  Request 3: DNS lookup → TCP handshake → TLS handshake → send → receive → CLOSE
             ↑ expensive setup/teardown repeated every single time

WITH Session (connection pooling):
  Request 1: DNS lookup → TCP handshake → TLS handshake → send → receive → KEEP OPEN
                                                                               ↓
  Request 2:                                                   send → receive → KEEP OPEN
                                                                               ↓
  Request 3:                                                   send → receive → CLOSE
             ↑ setup cost paid ONCE — subsequent requests reuse the TCP/TLS connection
             ↑ especially significant for HTTPS (TLS handshake is expensive)

Retry flow with backoff_factor=1:
  Attempt 1 → 503 → wait 0s
  Attempt 2 → 503 → wait 2s   (backoff_factor * 2^(retry-1) = 1 * 2^1)
  Attempt 3 → 503 → wait 4s   (1 * 2^2)
  Attempt 4 → success OR raises MaxRetryError
```

---

## 4. Internals / how it works

- `requests` is built on top of `urllib3`, which handles the actual TCP connection management, connection pooling, SSL/TLS, and HTTP/1.1 keep-alive. `requests` adds the ergonomic API on top: automatic JSON encoding/decoding, authentication handlers, session/cookie management, and the `PreparedRequest` model.
- A `requests.Session` maintains a `urllib3.PoolManager` internally — a dict of connection pools keyed by `(scheme, host, port)`. Each pool holds up to `pool_maxsize` open TCP connections. When you make a request, `urllib3` checks the pool for an existing open connection to that host before opening a new one — this is the "connection reuse" that makes `Session` so much faster for multiple requests to the same host.
- `response.raise_for_status()` checks `response.status_code` and raises `requests.exceptions.HTTPError` if it's 4xx or 5xx. Critically, it does **nothing** for 3xx redirects — `requests` follows redirects automatically by default (up to 30). You can disable this with `allow_redirects=False`.
- `timeout` is **not** a total request timeout — it's per network operation. `timeout=(3, 10)` means: wait 3s for the TCP connection to be established, then wait up to 10s for each chunk of data to arrive. A very slow server that sends 1 byte every 9 seconds will never trigger the read timeout. For a true end-to-end timeout, you need to implement it yourself (e.g., using `threading.Timer` or `asyncio.wait_for`).
- `urllib3.Retry` implements exponential backoff as `{backoff_factor} * (2 ** (retry_number - 1))` seconds — so `backoff_factor=1` gives waits of 0, 2, 4, 8 seconds. The first retry has 0 wait (`2^0 = 1` but capped by `backoff_max`). It also respects `Retry-After` headers sent by rate-limiting APIs.
- `httpx` was built as a ground-up replacement for `requests` with first-class `async`/`await` support, HTTP/2, and a cleaner type-annotated API. Internally it uses `h11` (for HTTP/1.1) and `h2` (for HTTP/2) as protocol parsers instead of `urllib3`. The key difference: `httpx.AsyncClient` uses Python's event loop to multiplex many requests over fewer connections, whereas `requests` (being synchronous) blocks on each network operation.
- SSL certificate verification (`verify=True` by default) uses the `certifi` package's certificate bundle to verify the server's TLS certificate chain. Setting `verify=False` disables this entirely — NEVER do this in production as it opens you to man-in-the-middle attacks. If you have a custom CA, pass `verify="/path/to/ca-bundle.pem"` instead.

---

## 5. Interview questions

**Q1: Why should you always use a `requests.Session` when making multiple requests to the same API, instead of calling `requests.get()` directly each time?**
A: Three reasons: (1) **Connection pooling** — a `Session` reuses TCP and TLS connections across requests to the same host via `urllib3`'s connection pool. Each `requests.get()` call opens a fresh connection (DNS lookup + TCP handshake + TLS handshake), which is expensive — especially TLS which requires 2 round-trips. A `Session` pays this cost once. (2) **Shared state** — headers, cookies, auth, and base settings are set once and applied to every request, eliminating repetition and ensuring consistency. (3) **Retry/adapter configuration** — `HTTPAdapter` with retry logic can only be mounted on a `Session`, not on one-shot calls. For a loop making 100 API calls, a `Session` can be 3–5x faster than bare `requests.get()`.

**Q2: What does `timeout=(3.05, 10)` actually mean, and why is it NOT a total request timeout?**
A: The tuple is `(connect_timeout, read_timeout)`. `3.05` is the maximum time to wait for the TCP connection to be established (SYN/ACK handshake). `10` is the maximum time to wait between bytes arriving once connected — it resets on each chunk received, not on the entire response. A server that streams data very slowly (1 byte every 9 seconds) will never trigger the read timeout. This means a request could theoretically run for hours despite a 10-second timeout. For a true end-to-end timeout you need an external mechanism like `asyncio.wait_for()` (for async code) or a `threading.Timer` that calls `response.close()`. The `3.05` value is intentionally slightly above a round number to avoid a race condition with TCP's own 3-second retransmission timer.

**Q3: What is `response.raise_for_status()` and why should it be called on every response?**
A: `raise_for_status()` raises `requests.exceptions.HTTPError` if the status code is 4xx or 5xx. Without it, `requests` returns the response object silently regardless of status code — a `404 Not Found` or `500 Internal Server Error` response is returned just like a `200 OK`. This leads to a very common bug: code that calls `response.json()` on a 404 response (which might contain an HTML error page) and gets a confusing `JSONDecodeError` instead of a clear HTTP error. Always call `raise_for_status()` immediately after the request, then parse the body — this makes the error obvious and the code self-documenting about its expectations.

**Q4: How would you implement retry with exponential backoff for a flaky API, and what's the difference between retrying at the `urllib3` level vs at the application level?**
A: **`urllib3` level** (via `HTTPAdapter` + `Retry`): retries happen inside the HTTP layer, transparent to your calling code — best for transient network errors and specific HTTP status codes (429, 503). Limitation: can't easily implement application-specific logic (e.g., parsing a `Retry-After` header value to wait exactly that long, or checking the response body for a specific error code). **Application level** (manual `for attempt in range(max_retries)` loop with `time.sleep(backoff_factor * 2**attempt)`): full control over retry conditions, wait times, and logging — but more boilerplate. Senior practice: use `urllib3.Retry` for infrastructure-level retries (network failures, 5xx), then add application-level retry logic for API-specific behavior (rate limit headers, partial success responses).

**Q5: What's the difference between `requests` and `httpx`, and when would you choose `httpx`?**
A: `requests` is synchronous only — each call blocks the thread until the response arrives. `httpx` supports both sync (`httpx.Client`) and async (`httpx.AsyncClient`) interfaces. Choose `httpx` when: (1) you're writing async code (FastAPI, asyncio) and need non-blocking HTTP calls — `requests` in async code blocks the event loop; (2) you need HTTP/2 (multiplexing multiple requests over one connection — significant for APIs with many small requests); (3) you want a more modern API with better type hints and a stricter interface (e.g., `httpx` requires `timeout` to be set explicitly or it raises a warning, preventing the "forgot timeout" bug). For sync scripts and standard REST API clients, `requests` is still the simpler choice. `httpx`'s API is intentionally compatible with `requests` for easy migration.

---

## 6. Practice problems

**Beginner:**
Write a `GitHubClient` class that wraps a `requests.Session` and provides:
1. `__init__(token)` — sets up the session with auth header, base URL `https://api.github.com`, default timeout `(3.05, 10)`, and `Accept: application/vnd.github.v3+json` header
2. `get_user(username)` → dict — fetches user profile, calls `raise_for_status()`
3. `list_repos(username, sort="stars")` → list — fetches repos, handles pagination via `Link` header (stop after 3 pages max to avoid rate limits in testing)
4. Proper exception handling: `Timeout` → log warning and return `None`; `HTTPError` with 404 → return `None`; other `HTTPError` → re-raise
5. A `__enter__`/`__exit__` so it can be used as a context manager (closing the session on exit)

- Suggested filename: `http_prac01_github_client.py`
- Test: fetch your own GitHub profile and first 2 pages of repos with the client

**Senior:**
Build a **production-ready HTTP client base class** for internal microservice communication:

1. `MicroserviceClient(base_url, service_name, api_key)` — base class using `requests.Session`
2. Retry policy: 3 retries, exponential backoff, retry on 429/500/502/503/504
3. Every request automatically gets: `X-Request-ID` (UUID4), `X-Service-Name`, `X-Timestamp` headers
4. Automatic rate limit handling: if response is 429 with `Retry-After` header, sleep exactly that many seconds before retrying (override the default backoff)
5. Circuit breaker pattern: after 5 consecutive failures, `_open_circuit()` raises `CircuitOpenError` immediately without making requests, for 30 seconds — then `_half_open()` allows one test request through
6. Metrics hook: a `record_metric(method, url, status_code, duration_ms)` method that subclasses can override (default: `logging`)
7. `OrderServiceClient(MicroserviceClient)` — concrete subclass with `get_order(id)`, `create_order(payload)`, `cancel_order(id)` methods
8. Full test suite using the `responses` library covering: success, retry on 503, circuit breaking after 5 failures, rate limit with `Retry-After`, metrics recorded correctly

- Suggested filename: `http_prac02_microservice_client.py`
- This tests whether you can design a robust HTTP layer for a real distributed system

---

## 7. Common mistakes & senior traps

- **Forgetting `timeout=`** — the single most common production mistake. Without it, a hung server will hang your thread/process indefinitely, taking down your application.
  ```python
  # WRONG — hangs forever if server doesn't respond
  response = requests.get("https://api.example.com/data")

  # RIGHT — always set timeout
  response = requests.get("https://api.example.com/data", timeout=(3.05, 10))
  ```

- **Not calling `raise_for_status()`** — silently processing error responses as success.
  ```python
  # WRONG — 404 body might not be valid JSON, causing confusing JSONDecodeError
  response = requests.get("https://api.example.com/user/999", timeout=5)
  user = response.json()   # might raise JSONDecodeError on HTML error page

  # RIGHT — fail fast with a clear error
  response = requests.get("https://api.example.com/user/999", timeout=5)
  response.raise_for_status()   # raises HTTPError clearly if 404/500
  user = response.json()        # only reached if response was 2xx
  ```

- **Using one-shot `requests.get()` in a loop** instead of a `Session` — causes a new TCP+TLS handshake on every iteration.
  ```python
  # WRONG — N connections for N requests
  for user_id in user_ids:
      r = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)

  # RIGHT — one connection pool, reused across all requests
  with requests.Session() as session:
      for user_id in user_ids:
          r = session.get(f"https://api.example.com/users/{user_id}", timeout=5)
  ```

- **Setting `verify=False`** to get past SSL errors instead of fixing the certificate problem — disables all certificate validation, opening the connection to MITM attacks.
  ```python
  # WRONG — never in production
  requests.get("https://internal-api.com", verify=False)

  # RIGHT — provide the CA bundle if using internal/self-signed certs
  requests.get("https://internal-api.com", verify="/etc/ssl/certs/internal-ca.pem")
  ```

- **Loading entire large responses into memory** — `response.json()` / `response.text` / `response.content` all buffer the full body. For large files or data exports, use `stream=True` with `iter_content()`.

- **Hardcoding API keys in source code** — always load from environment variables or a secrets manager:
  ```python
  # WRONG
  API_KEY = "sk-abc123hardcoded"

  # RIGHT
  import os
  API_KEY = os.environ["MY_API_KEY"]   # raises KeyError if not set → fails fast
  # or: API_KEY = os.getenv("MY_API_KEY", "default")  # but "default" for secrets is bad
  ```

- **Not closing sessions** — open sessions hold TCP connections and file descriptors. Always use `Session` as a context manager (`with requests.Session() as s:`) or call `session.close()` explicitly.

- **Assuming `response.json()` always works** — if the server returns a non-JSON body (e.g., an HTML error page, a plain-text 503 message), `response.json()` raises `json.JSONDecodeError`. Always call `raise_for_status()` first, and consider wrapping `response.json()` in a try/except for truly defensive code against misbehaving APIs.

- **Blocking `asyncio` event loop with `requests`** — if you're in an async context (FastAPI route, asyncio task), calling `requests.get()` blocks the entire event loop during the network wait, defeating the purpose of async. Use `httpx.AsyncClient` or run the blocking call in a thread pool with `asyncio.to_thread(requests.get, url)`.

---

Say **"next"** when you're ready for **Regex**, or ask for more practice problems on HTTP requests first.