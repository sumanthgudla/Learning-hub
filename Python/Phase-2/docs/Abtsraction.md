# Python OOP: Abstraction — From Basics to Senior-Level Interviews

Abstraction is one of the four main pillars of Object-Oriented Programming (OOP), along with Encapsulation, Inheritance, and Polymorphism.

Abstraction means hiding implementation details and exposing only what the user needs to interact with.

Think about driving a car. You press the accelerator to increase speed, but you don't need to understand how fuel injection, combustion, and the engine work internally.

- What you use: Accelerator, brake, steering.
- What is hidden: Internal engine mechanics.

That's abstraction!

## 1. Basic Example — Without Abstraction

Imagine you are building a payment application.

```
class Payment:    def pay(self):        print("Connecting to bank...")        print("Validating account...")        print("Processing payment...")        print("Payment successful!")payment = Payment()payment.pay()
```

The user calls `pay()` and gets the payment processed. However, this class doesn't enforce any particular implementation contract. The method also exposes internal steps in its code.

Now let's understand how abstraction helps us design this better.

## 2. Abstraction Using Python's `abc` Module

Python provides the `abc` module to implement formal abstraction using Abstract Base Classes (ABCs).

```
from abc import ABC, abstractmethodclass Payment(ABC):    @abstractmethod    def pay(self, amount):        pass
```

Let's understand every line.

- `ABC`: Makes `Payment` an abstract base class.
- `@abstractmethod`: Declares a method that subclasses must implement.
- `pass`: A placeholder; the actual payment logic is supplied by a subclass.

The important part is that `Payment` defines what a payment class must provide, not how every payment must work.

## 3. Implementing the Abstraction

Suppose we support credit card payments and UPI payments.

Payment (Abstract Class)

Defines the contract: `pay(amount)`

CreditCardPayment

Card-specific logic

UPIPayment

UPI-specific logic

```
from abc import ABC, abstractmethodclass Payment(ABC):    @abstractmethod    def pay(self, amount):        passclass CreditCardPayment(Payment):    def pay(self, amount):        print(f"Charging ₹{amount} to credit card")class UPIPayment(Payment):    def pay(self, amount):        print(f"Processing ₹{amount} through UPI")card = CreditCardPayment()upi = UPIPayment()card.pay(1000)upi.pay(500)
```

Output:

```
Charging ₹1000 to credit card
Processing ₹500 through UPI
```

Notice what happened:

1. `Payment` defined the required method.
2. Each subclass implemented its own logic.
3. The calling code uses the same method name, `pay()`.
4. The implementation differs depending on the payment type.

This is abstraction in action.

## 4. What Happens If We Don't Implement the Abstract Method?

Consider this example:

```
class CreditCardPayment(Payment):    passcard = CreditCardPayment()
```

Python raises an error similar to:

```
TypeError: Can't instantiate abstract class
CreditCardPayment with abstract method pay
```

Why?

Because `CreditCardPayment` inherited the requirement to implement `pay()`, but did not fulfill it.

Interview point: An abstract class cannot be instantiated directly, and a subclass with unimplemented abstract methods cannot be instantiated either.

## 5. Real-World Example — AI Engineer Application

Imagine your AI application supports OpenAI, Anthropic Claude, and Gemini.

You want your application to call any model using the same interface.

```
from abc import ABC, abstractmethodclass LLMProvider(ABC):    @abstractmethod    def generate(self, prompt):        passclass OpenAIProvider(LLMProvider):    def generate(self, prompt):        return "Response from OpenAI"class ClaudeProvider(LLMProvider):    def generate(self, prompt):        return "Response from Claude"def get_response(provider, prompt):    return provider.generate(prompt)openai = OpenAIProvider()claude = ClaudeProvider()print(get_response(openai, "Explain RAG"))print(get_response(claude, "Explain RAG"))
```

Output:

```
Response from OpenAI
Response from Claude
```

The application doesn't need to know the internal API calls, authentication, or request format of each provider. It only needs to know that the provider implements `generate()`.

In production, each provider would contain its own API integration, error handling, retries, and configuration.

Why this is useful: You can add another LLM provider without rewriting the application's calling logic, provided the new provider follows the same contract.

## 6. Abstract Class vs Normal Class

| Feature                                          | Normal class                        | Abstract class           |
| ------------------------------------------------ | ----------------------------------- | ------------------------ |
| Create an object directly                        | Yes                                 | No                       |
| Define regular methods                           | Yes                                 | Yes                      |
| Define abstract methods                          | Not enforced as abstract            | Yes                      |
| Require subclasses to implement specific methods | Not automatically                   | Yes                      |
| Typical purpose                                  | Create objects and provide behavior | Define a common contract |

An abstract class can also contain regular methods and shared state.

```
from abc import ABC, abstractmethodclass LLMProvider(ABC):    def __init__(self, model_name):        self.model_name = model_name    def get_model_name(self):        return self.model_name    @abstractmethod    def generate(self, prompt):        pass
```

Here, `get_model_name()` is shared functionality, while `generate()` must be implemented by concrete subclasses.

## 7. Abstraction vs Encapsulation

This is a very common interview question.

| Abstraction                              | Encapsulation                                                   |
| ---------------------------------------- | --------------------------------------------------------------- |
| Hides implementation complexity          | Bundles data and behavior together and controls access to state |
| Focuses on what an object does           | Focuses on how its state is managed and protected               |
| Uses ABCs and abstract methods in Python | Uses classes, properties, and access conventions                |
| Example: `payment.pay(1000)`             | Example: controlling access to a payment's internal balance     |

A useful way to remember it:

- Abstraction: You can use the payment method without knowing how it works internally.
- Encapsulation: You control how the payment object's internal data is accessed or changed.

These concepts can work together in the same class.

## 8. Important Interview Traps

Q1. Can an abstract class have a constructor?

Yes. Its constructor can initialize common state, and a subclass can call it using `super().__init__()`.

Q2. Can an abstract class contain implemented methods?

Yes. Only methods marked `@abstractmethod` impose an implementation requirement on concrete subclasses.

Q3. Does Python have interfaces?

Python does not have a separate `interface` keyword like Java. Abstract base classes can provide interface-like contracts. Python also supports structural interfaces through `typing.Protocol`.

Q4. Does `@abstractmethod` hide the implementation?

No. Its primary purpose is to require subclasses to implement a method. Hiding implementation complexity is the broader design principle of abstraction.

Q5. Can we create an object of an abstract class?

Not while it still has unimplemented abstract methods. Once all abstract methods are implemented, a concrete subclass can be instantiated.

Q6. Is abstraction possible without `ABC`?

Yes. You can design simple interfaces through conventions or use `Protocol` for structural typing. However, `ABC` is useful when you want Python to enforce abstract method requirements at instantiation time.

## 9. Practice Problems

## Beginner — Abstract class behavior

What happens when this code runs?

```
from abc import ABC, abstractmethodclass Animal(ABC):    @abstractmethod    def sound(self):        passclass Dog(Animal):    passdog = Dog()
```

It creates a Dog object successfully.

It raises a TypeError.

It prints `None`.

Check answer

## Senior-level — Design question

You are building an AI application that supports OpenAI and Claude. Both providers have different APIs, but the application should call them through `generate(prompt)`.

What is the best design?

Write all provider-specific logic in one giant function.

Define an abstract `LLMProvider` with `generate()` and implement it separately for each provider.

Create two unrelated classes with different method names.

Check answer

Remember this for interviews:

> Abstraction is an OOP principle that exposes essential functionality while hiding implementation complexity. In Python, abstract base classes and abstract methods help define contracts that subclasses must implement.