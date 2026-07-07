API rate limits mean the provider only allows a certain number of requests per minute (or tokens per minute). If you exceed that, you’ll get errors like 429 Too Many Requests.
In LangChain, the safest approach is to retry with backoff, and also control concurrency so you don’t spam the API.
A common pattern is:
Catch rate limit errors
Wait a bit (backoff)
Retry a few times
If it still fails, return a graceful error or fallback model
Here’s a simple retry approach using tenacity (very common in Python):


from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# Replace with the provider's rate limit exception if available
class RateLimitError(Exception):
    pass

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=20),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(RateLimitError),
)
def safe_invoke(chain_or_llm, inp):
    return chain_or_llm.invoke(inp)

What this does:
If a rate limit error happens, it retries.
It waits longer each time (1s → 2s → 4s … up to 20s).
It stops after 5 attempts.
You also reduce rate limit issues by:
Using smaller max_tokens
Batching calls (if supported)
Limiting parallel requests (for example, don’t run 200 calls at once

No material available!

The