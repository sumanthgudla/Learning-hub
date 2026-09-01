Actually, Python **can** remember it — that's exactly what a closure is doing.

The confusing part is: **why doesn't the local variable disappear when `outer()` finishes?**

Consider:

```python
def outer():
    x = 10

    def inner():
        print(x)

    return inner

func = outer()
func()
```

### Normally

For a regular local variable:

```python
def outer():
    x = 10
```

After:

```python
outer()
```

there is no way to access `x` anymore, so Python can eventually clean up that local state.

### But with a closure

When Python creates `inner`, it notices:

```python
def inner():
    print(x)
```

`inner` uses `x`, which belongs to `outer`.

So Python keeps a reference to `x` along with the `inner` function.

Conceptually, you can think of:

```text
func
 ├── function code → inner()
 └── remembered x → 10
```

So:

```python
func()
```

can still find `x`.

### Why does Python do this?

Because otherwise this very useful pattern would be impossible:

```python
def multiplier(n):
    def multiply(x):
        return x * n

    return multiply

double = multiplier(2)
triple = multiplier(3)
```

`double` needs to remember `n = 2`, while `triple` needs to remember `n = 3`.

They each keep their **own captured value**.

### Important distinction

The variable isn't necessarily "copied into the function" in the simple sense.

Python's closure mechanism keeps a **reference to the enclosing variable through a closure cell**.

You can actually see it:

```python
def outer():
    x = 10

    def inner():
        return x

    return inner

func = outer()

print(func.__closure__)
print(func.__closure__[0].cell_contents)
```

The cell contains:

```text
10
```

### Interview-friendly explanation

> **When an inner function uses a variable from its enclosing function, Python preserves that variable in a closure so the inner function can access it even after the outer function has returned.**

Think of it as:

**"The function leaves, but the data it still needs travels with it."**
