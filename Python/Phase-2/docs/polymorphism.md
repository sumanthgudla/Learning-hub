# Python OOP: Polymorphism — From Basics to Senior-Level Interviews

Polymorphism is one of the four main pillars of Object-Oriented Programming (OOP), along with Abstraction, Encapsulation, and Inheritance.

Polymorphism means “one interface, many forms.” The same method name or operation can behave differently depending on the object or the data it receives.

Think about a `pay()` method in a payment application:

- Credit card → charges the card.
- UPI → processes a UPI payment.
- PayPal → processes a PayPal payment.

You call the same method, `pay()`, but the behavior changes.

## 1. Basic Example — Same Method, Different Behavior

```
class Dog:    def sound(self):        print("Bark")class Cat:    def sound(self):        print("Meow")dog = Dog()cat = Cat()dog.sound()cat.sound()
```

Output:

```
Bark
Meow
```

What happened?

1. Both classes have a method called `sound()`.
2. The `Dog` object produces a bark.
3. The `Cat` object produces a meow.
4. The same method call behaves differently for different objects.

This is polymorphism.

Notice that we didn't need inheritance here. Python supports polymorphism through a concept called duck typing, which we'll cover below.

## 2. Polymorphism Through Inheritance and Method Overriding

Suppose we have a common parent class called `Payment`.

```
class Payment:    def pay(self, amount):        print(f"Paying ₹{amount}")class CreditCardPayment(Payment):    def pay(self, amount):        print(f"Charging ₹{amount} to credit card")class UPIPayment(Payment):    def pay(self, amount):        print(f"Paying ₹{amount} using UPI")card = CreditCardPayment()upi = UPIPayment()card.pay(1000)upi.pay(500)
```

Output:

```
Charging ₹1000 to credit card
Paying ₹500 using UPI
```

Here, both child classes override the parent's `pay()` method.

The important concept is method overriding: a child class provides its own implementation of a method inherited from a parent class.

### How Python decides which method to call

`card.pay(1000)`

Python checks the object's class first

`CreditCardPayment.pay()`

Found → execute this method

Python uses the object's class and its method resolution order (MRO) to determine which implementation to execute.

Interview point: Method overriding enables runtime polymorphism because the behavior depends on the actual object.

## 3. Polymorphism Without Inheritance — Duck Typing

This is especially important in Python interviews.

Python often cares more about what an object can do than which class it belongs to.

```
class OpenAIProvider:    def generate(self):        print("Generating response using OpenAI")class ClaudeProvider:    def generate(self):        print("Generating response using Claude")class GeminiProvider:    def generate(self):        print("Generating response using Gemini")def get_response(provider):    provider.generate()get_response(OpenAIProvider())get_response(ClaudeProvider())get_response(GeminiProvider())
```

Output:

```
Generating response using OpenAI
Generating response using Claude
Generating response using Gemini
```

Notice something important: these classes do not inherit from a common parent class.

Yet `get_response()` works with all three.

Why?

Because each object supports the required method, `generate()`.

This is duck typing.

> If an object behaves like the thing we need, Python can use it without requiring it to belong to a specific class hierarchy.

### Why this matters for AI engineers

Imagine your LangGraph application can use OpenAI, Claude, or Gemini. If each provider implements `generate()`, your application can call the same interface without hardcoding provider-specific logic into every part of the application.

In production, you would also handle different API parameters, authentication, errors, retries, and response formats inside provider-specific implementations.

## 4. Polymorphism With a Common Function

A useful design pattern is to write a function that works with different objects.

```
class PDFReport:    def export(self):        print("Exporting PDF report")class ExcelReport:    def export(self):        print("Exporting Excel report")class CSVReport:    def export(self):        print("Exporting CSV report")def export_report(report):    report.export()reports = [PDFReport(), ExcelReport(), CSVReport()]for report in reports:    export_report(report)
```

Output:

```
Exporting PDF report
Exporting Excel report
Exporting CSV report
```

The function doesn't need separate conditions such as:

```
if report_type == "PDF":    ...elif report_type == "Excel":    ...
```

Each object knows how to export itself.

Benefit: You can add a new report type without changing `export_report()`, as long as the new object implements `export()`.

## 5. Operator Overloading — Another Form of Polymorphism

Have you noticed that `+` behaves differently depending on the data type?

```
print(10 + 20)print("Hello " + "World")print([1, 2] + [3, 4])
```

Output:

```
30
Hello World
[1, 2, 3, 4]
```

The same operator performs different operations:

- Integers → addition.
- Strings → concatenation.
- Lists → concatenation.

Python classes can define their own operator behavior using special methods, also called dunder methods.

For example, `__add__()` controls the behavior of `+` for a custom class.

```
class Money:    def __init__(self, amount):        self.amount = amount    def __add__(self, other):        return Money(self.amount + other.amount)m1 = Money(100)m2 = Money(200)result = m1 + m2print(result.amount)
```

Output:

```
300
```

Here, `m1 + m2` invokes the custom `__add__()` implementation.

## 6. Method Overloading in Python — Common Interview Trap

In languages such as Java, you can define multiple methods with the same name but different parameter lists.

For example, Java can support:

```
add(int a, int b)
add(int a, int b, int c)
```

Python does not support traditional method overloading by defining multiple methods with the same name.

Consider:

```
class Calculator:    def add(self, a, b):        return a + b    def add(self, a, b, c):        return a + b + ccalculator = Calculator()print(calculator.add(2, 3))
```

This raises a `TypeError` because the second definition replaces the first. Python does not preserve both definitions as separate overloads.

### How do we handle different numbers of arguments?

Use default parameters or `*args`.

```
class Calculator:    def add(self, *numbers):        return sum(numbers)calculator = Calculator()print(calculator.add(2, 3))print(calculator.add(2, 3, 4))
```

Output:

```
5
9
```

This is a practical way to support varying argument counts, but it isn't traditional signature-based method overloading.

Python also supports `functools.singledispatch` for function dispatch based on the type of the first argument.

## 7. Polymorphism vs Overriding vs Overloading

| Concept              | Meaning                                       | Python example                               |
| -------------------- | --------------------------------------------- | -------------------------------------------- |
| Polymorphism         | Same interface, different behavior            | Different providers implement `generate()`   |
| Method overriding    | Child class replaces inherited behavior       | `UPIPayment.pay()` overrides `Payment.pay()` |
| Method overloading   | Same name with different parameter signatures | Not natively supported as in Java            |
| Operator overloading | Customize an operator for your class          | Implement `__add__()`                        |
| Duck typing          | Use an object based on its supported behavior | Any object with `generate()` can be used     |

Remember: overriding is one way to achieve polymorphism, but polymorphism in Python is broader than inheritance and overriding.

## 8. Senior-Level Example — Extensible Payment System

Let's combine these ideas into a practical design.

```
from abc import ABC, abstractmethodclass Payment(ABC):    @abstractmethod    def pay(self, amount):        passclass UPI(Payment):    def pay(self, amount):        return f"UPI payment: ₹{amount}"class Card(Payment):    def pay(self, amount):        return f"Card payment: ₹{amount}"class PaymentService:    def process(self, payment, amount):        return payment.pay(amount)service = PaymentService()print(service.process(UPI(), 500))print(service.process(Card(), 1000))
```

Output:

```
UPI payment: ₹500
Card payment: ₹1000
```

Why is this a good design?

- Common contract: `Payment` requires `pay()`.
- Separate implementations: Each payment type handles its own behavior.
- Flexible service: `PaymentService` works with different payment methods.
- Easy extension: A new payment class can be added without changing the service.

This example combines abstraction and polymorphism:

- Abstraction defines the contract.
- Polymorphism lets different implementations respond differently through that contract.

## 9. Common Interview Questions

Q1. What is polymorphism?

The ability to use the same interface for different underlying implementations or behaviors.

Q2. Is inheritance mandatory for polymorphism in Python?

No. Duck typing allows unrelated classes to work with the same function if they support the required operations.

Q3. What happens when a child class overrides a parent method?

When that method is called on a child object, Python normally selects the child's implementation first, according to the method resolution order.

Q4. What is runtime polymorphism?

When the method implementation selected for execution depends on the actual object at runtime, such as calling an overridden method on a subclass instance.

Q5. What is the difference between abstraction and polymorphism?

Abstraction defines what functionality is exposed. Polymorphism allows different objects to provide different behavior through a common interface.

Q6. Can static methods be overridden?

A subclass can define a static method with the same name, but static methods do not receive `self` or `cls` automatically. Their behavior differs from ordinary instance-method overriding.

Q7. Why is polymorphism useful in production applications?

It reduces type-specific branching, improves extensibility, and lets calling code work with multiple implementations through a consistent interface.

## 10. Practice Problems

## Beginner — Predict the output

```
class A:    def show(self):        print("A")class B(A):    def show(self):        print("B")obj = B()obj.show()
```

What is printed?

A

B

A then B

Check answer

## Senior-level — Design thinking

You are building an application that supports OpenAI, Claude, and Gemini. You want to add a new provider without modifying your main response-generation function.

Which approach best supports polymorphism?

Write a separate `if/elif` branch for every provider.

Require each provider to implement `generate()` and call that method through a common interface.

Put all provider logic into one class.

Check answer

One-line interview answer to remember:

> Polymorphism in Python allows different objects to respond to the same method or operation in different ways. It can be achieved through method overriding, duck typing, and operator overloading.