## 1. Temperature and Top-p

These are **generation parameters** that control how an LLM chooses the next token.

The easiest way to remember:

> **Temperature controls how random the model is.**
> **Top-p controls how many likely tokens the model is allowed to consider.**

---

### 1. Temperature

The model doesn't simply say:

> "This is definitely the next token."

Instead, it produces probabilities.

Suppose the model sees:

> "The sky is..."

It might produce:

| Token       | Probability |
| ----------- | ----------: |
| `blue`      |         70% |
| `clear`     |         15% |
| `cloudy`    |         10% |
| `beautiful` |          5% |

**Temperature changes how strongly these probabilities are concentrated.**

#### Low temperature

Example:

```text
temperature = 0.1
```

The model strongly prefers the most probable token.

```text
"The sky is blue."
"The sky is blue."
"The sky is blue."
```

More **deterministic and predictable**.

Good for:

* RAG question answering
* Data extraction
* Classification
* SQL generation
* Structured JSON
* Business applications where consistency matters

#### High temperature

Example:

```text
temperature = 1.0 or 1.5
```

The probability distribution becomes flatter, allowing less-probable tokens to be selected more often.

You may get:

```text
"The sky is blue."
"The sky is painted with brilliant azure."
"The sky is a vast ocean of light."
```

More **creative and varied**.

Good for:

* Creative writing
* Brainstorming
* Story generation
* Marketing ideas

---

## 2. Top-p

Top-p is also called **nucleus sampling**.

Instead of considering every possible token, the model selects the **smallest group of tokens whose combined probability reaches p**.

Suppose:

| Token     | Probability |
| --------- | ----------: |
| blue      |        0.60 |
| clear     |        0.20 |
| cloudy    |        0.10 |
| beautiful |        0.05 |
| dark      |        0.03 |
| orange    |        0.02 |

If:

```text
top_p = 0.90
```

The model considers:

```text
blue   → 60%
clear  → 20%
cloudy → 10%
----------------
Total  → 90%
```

The remaining tokens are excluded.

So the model chooses from the **smallest probability set adding up to 90%**.

---

## Temperature vs Top-p

This is the important interview distinction:

| Parameter       | Controls                                 |
| --------------- | ---------------------------------------- |
| **Temperature** | How randomly probabilities are sampled   |
| **Top-p**       | How many candidate tokens are considered |

Think of it like this:

```text
Temperature
     ↓
"How adventurous should I be?"

Top-p
     ↓
"How many options should I consider?"
```

---

### Example

Imagine you're asking:

> "Give me a name for an AI startup."

**Low temperature + high top-p:**

```text
NeuraTech
```

Likely to give predictable answers.

**High temperature + high top-p:**

```text
Synaptica
Cognivault
NeuralForge
MindMesh
```

More creative.

---

## Should we change both?

Usually, **you don't need to aggressively tune both at the same time**.

For a production application, you might start with something like:

```text
temperature = 0.2
top_p = 0.9
```

and evaluate the actual behavior.

The exact useful values depend on the model/provider.

### Interview answer

If the interviewer asks:

> **"What is temperature and top-p?"**

Say:

> **"Temperature and top-p are sampling parameters that control how an LLM generates text. Temperature controls the randomness of the probability distribution—lower values make the output more deterministic, while higher values make it more diverse. Top-p, or nucleus sampling, limits the model's choices to the smallest set of tokens whose cumulative probability reaches a specified threshold. In production, I would use lower randomness for tasks like RAG and structured extraction, and higher randomness for creative tasks."**

### One-line memory trick

**Temperature = randomness**

**Top-p = candidate pool**

Next, a very important interview topic is **Transformers and Attention — how an LLM actually understands relationships between tokens.**
