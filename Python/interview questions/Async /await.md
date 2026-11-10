In Python, `await` is used inside an `async` function to wait for an asynchronous operation to complete without blocking the entire thread.

Let's understand this from the basics.

## 1. First, understand `async`

When you define a function using `async def`, Python treats it as a coroutine function.

```
async def get_data():    print("Fetching data")    return "Data received"
```

Now, if you call it:

```
result = get_data()print(result)
```

Output:

```
<coroutine object get_data at ...>
```

Why?

Because calling an async function does not execute its body immediately. It creates a coroutine object.

## 2. What does `await` do?

`await` tells Python:

Wait for this asynchronous operation to finish before continuing with the next statement in this coroutine.

```
import asyncioasync def get_data():    print("Fetching data")    await asyncio.sleep(2)    print("Data received")    return "Success"async def main():    result = await get_data()    print(result)asyncio.run(main())
```

Output:

```
Fetching data
(wait 2 seconds)
Data received
Success
```

Here:

- `async` makes a function asynchronous.
- `await` waits for the coroutine to complete.
- `asyncio.sleep(2)` simulates a 2-second asynchronous operation.

## 3. The most important concept: Does await block execution?

This is where many interview candidates get confused.

Consider this:

```
import asyncioasync def task1():    print("Task 1 started")    await asyncio.sleep(3)    print("Task 1 completed")async def task2():    print("Task 2 started")    await asyncio.sleep(1)    print("Task 2 completed")async def main():    await task1()    await task2()asyncio.run(main())
```

Output:

```
Task 1 started
(wait 3 seconds)
Task 1 completed
Task 2 started
(wait 1 second)
Task 2 completed
```

Total time = 4 seconds.

Why? Because we awaited task1 before starting task2.

Now let's change it.

```
async def main():    await asyncio.gather(task1(), task2())asyncio.run(main())
```

Output:

```
Task 1 started
Task 2 started
(wait approximately 3 seconds)
Task 2 completed
Task 1 completed
```

Total time = 3 seconds.



Important

&#x20;Both tasks can make progress concurrently because `gather()` schedules them together.



## 4. Visual understanding

Imagine you are downloading two files.

Sequential execution

One operation finishes before the next starts.

Download A — 3 seconds

Download B — 1 second

# 4 seconds

Concurrent execution

Both operations make progress during overlapping periods.

Download A — 3 seconds

Download B — 1 second

# 3 seconds

## 5. What happens internally when Python encounters `await`?

Suppose:

```
async def fetch_data():    print("Start")    await asyncio.sleep(3)    print("End")
```

The sequence is:

1. Coroutine starts executing.
2. Python encounters `await`.
3. It suspends the current coroutine.
4. Control returns to the event loop.
5. The event loop can execute other ready coroutines.
6. After the awaited operation completes, the event loop resumes the suspended coroutine.
7. Execution continues after `await`.

Important: `await` doesn't necessarily block the thread. It suspends the current coroutine and gives the event loop an opportunity to run other work.

## 6. Important interview questions

| Question                                    | Answer                                              |
| ------------------------------------------- | --------------------------------------------------- |
| Can we use await outside async?             | Generally, no                                       |
| Can async function exist without await?     | Yes                                                 |
| Does await create a thread?                 | No                                                  |
| Does await execute tasks in parallel?       | No                                                  |
| Does await block the entire thread?         | Not when awaiting a properly asynchronous operation |
| Can we await multiple coroutines?           | Yes, using gather or TaskGroup                      |
| What happens if we don't await a coroutine? | It may never execute                                |

## 7. Test your understanding

Let's see whether you've understood the concept.

What will be the output and total execution time?

```
import asyncioasync def task1():    print("A")    await asyncio.sleep(2)    print("B")async def task2():    print("C")    await asyncio.sleep(1)    print("D")async def main():    task1_coro = task1()    task2_coro = task2()    await task1_coro    await task2_coroasyncio.run(main())
```

What is the total execution time?

1 second

3 seconds

2 seconds

They execute in parallel

Check answer

This distinction between `await`, coroutine creation, and task scheduling is fundamental to understanding Python asyncio and is commonly tested in Python interviews.