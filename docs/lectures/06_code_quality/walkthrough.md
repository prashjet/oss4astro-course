---
orphan: true
---

# Walkthrough: Code quality

This walkthrough follows the live demo using
[sequence](https://github.com/prashjet/sequence). Run shell commands from the repository
root.

## 1. Set up

Let's start `sequence` from the last commit after last lecture:

```bash
git clone https://github.com/prashjet/sequence.git
cd sequence
git switch -c lecture-06-code-quality fdbe0ac
uv sync --locked
```

If you already have a checkout, run `git fetch origin` from the repository root, then
run the branch and sync commands above.

Let's run the existing tests to check everything is order

```bash
uv run pytest
```

before moving on to changing the code.

## 2. Formatting and Linting with Ruff

[Ruff](https://docs.astral.sh/ruff/) is a Python formatter and linter. It serves two
main purposes:

- **Formatting** (`ruff format`) applies a consistent style to the code, including
  spacing, indentation, and line wrapping.
- **Linting** (`ruff check`) flags code that matches an enabled lint rule, such as an
  unused import or an undefined name.

To see this in action, let's add Ruff as a development dependency:

```bash
uv add --dev ruff
```

### Formatting

`ruff format` is the basic command to reformat your code.

Let's first check the changes `ruff format` would make:

```bash
uv run ruff format --check
```

This identifies formatting errors in several places e.g.
- enclose strings with double quotes (`'sequence'` → `"sequence"`),
- add trailing 0's to typed floats (`2.` → `2.0`)
- uniform spacing between function definitions.

The [Ruff Formatter Style Guide](https://docs.astral.sh/ruff/formatter/#style-guide)
describes Ruff's default formatting rules. These defaults are a good starting point -
stick with them unless you have a strong reason not to e.g. some pre-existing formatting
conventions.

The defaults locations Ruff checks include:
- any `*.py` files e.g. `src/*.py`, `tests/*.py ` and `docs/conf.py`
- specifically named `*.toml` files e.g. `pyproject.toml` and `ruff.toml`
- any notebooks `*.ipynb`

You can limit the scope by passing a specific location e.g. to only check the `src/`
directory:

```bash
uv run ruff format --check src
```

Now let Ruff apply the formatting corrections

```bash
uv run ruff format
```

We can view the applied changes in VSCode's Source Control view.

### Linting

Linting flags potential bugs and style issues not covered by formatting.

Let's run the linter (`ruff check`) to see what it finds:

```bash
uv run ruff check
```

The linter picks out
- an unused import (`import math`)
- grouped imports (`import math`)

These imports are valid Python, but Ruff flags them to keep import blocks consistent and
easy to scan. Other lint rules catch likely bugs, such as references to undefined names.
Ruff's [default lint rules](https://docs.astral.sh/ruff/default-rules/) are a good
starting place

To apply the lint corrections:

```bash
uv run ruff check --fix
```

Note the checking vs. applying fixes looks different for formatting and linting:

| Goal | Linter | Formatter |
|---|---|---|
| Check without editing | `ruff check` | `ruff format --check` |
| Apply changes | `ruff check --fix` | `ruff format` |

### Configuring ruff

Ruff's default formatting and linting rules are probably fine. If for any reason you
need to alter these there are several options for
[configuring Ruff](https://docs.astral.sh/ruff/configuration/).

## 2. Type hints and type checking

**Statically typed** languages, the compiler checks types before the program runs. 
In C, for example, this means that a typical variable declaration must include its 
type:

```c
int n = 6;
double ratio = 2.0;
```

Python, in contrast, is **dynamically typed**. Values have types, and a name can 
refer to values of different types over the course of a program. You can write the 
same assignments without declaring types:

```python
n = 6
ratio = 2.0
```

This keeps simple code concise and makes it easy to write functions that work with
different kinds of inputs. Nevertheless, as a project grows, it helps to spell out 
what kinds of values its functions expect and return.

**Type hints** let you express those expectations in the code. They help readers
understand how to call a function, and a type checker such as `ty` can use them 
to flag mistakes before you run it.

Let's add `ty` as a development dependency:

```bash
uv add --dev ty
```

### Basic type hints and type checking

In `src/sequence/__init__.py`, change the signature of `fibonacci` and keep its body as
it is.

```python
def fibonacci(n: int) -> list[int]:
```

The signature says that callers should pass an integer and can expect a list of integers
in return.

Create a temporary file called `typing_demo.py` in the repository root.

```python
from sequence import fibonacci

print(fibonacci(6))
print(fibonacci("6"))
print(fibonacci(-1))
```

Ask ty to check the package and the demo file.

```bash
uv run ty check src typing_demo.py
```

Which call does ty flag? `"6"` is a string, so ty reports a type error. `-1` is an
integer, so it satisfies the annotation, even though if 

```bash
uv run python -c 'from sequence import fibonacci; fibonacci(-1)'
```

The type hint describes the kind of value the function expects. The docstring says the
integer must be non-negative, the function enforces that rule, and the tests verify it.

### Other types of types: `typing` and classes

Alongside built-in types such as `int`, use annotation:
- constructs from Python’s `typing` module,
- constructs from Python’s `collections.abc` module,
- classes you define yourself or import from a dependency.

To demo these, let's write a function plot our sequences. Lets add `matplotlib`
as a dependency (`uv add matplotlib`) then add our plotting function in a new file
 `src/sequence/analysis.py`:

```python
from collections.abc import Callable
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_sequence(
    sequence: Callable[[int], list[int]],
    n: int,
    order: Literal["forward", "reverse"] = "forward",
) -> Figure:
    values = sequence(n)
    if order == "reverse":
        values = list(reversed(values))

    fig, ax = plt.subplots()
    ax.plot(values)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title(f"Order = {order}")
    return fig
```

We've used types:
- `Callable[[int], list[int]]`: a function which takes int and returns a list of
ints
- `Literal["forward", "reverse"] = "forward"` either of two specified options
(`"forward"` or `"reverse"`), with a set default
- `Figure`: a class defined in `matplotlib.figure` 

Let's add an example usage to `typing_demo.py`

```python
from sequence import fibonacci
import matplotlib.pyplot as plt
from sequence.plotter import plot_sequence

fig = plot_sequence(even, 10, "forward")
plt.show()
```

check it passes the type checker

```bash
uv run ty check typing_demo.py
```

and finally run the example

```bash
uv run python typing_demo.py
```

### Composing types
 
In a type annotation the operator | combines types into their union. For example, let’s write a 
function that returns the last element of a sequence of integers. If the sequence 
is empty, it should returns `None`. The return annotation will describe both possibilities.

Add the following example to `src/sequences/analysis.py` 

```python
from collections.abc import Sequence


def last_term(terms: Sequence[int]) -> int | None:
    return terms[-1] if terms else None
```

then add an example using this to `typing_demo.py`, and check it passes the type checker and runs.

Other examples of composing types:

| Annotation | Meaning | Example |
|---|---|---|
| `list[int] \| None` | The whole sequence may be missing. If present, every term is an integer. | `[0, 1, 1, 2]` or `None` |
| `list[int \| None]` | The sequence is present, but individual terms may be missing. | `[0, None, 1, 2]` |
| `tuple[int, float]` | A pair with an integer first and a float second, such as an index and the corresponding term. | `(3, 8.0)` |

- Which annotation would accept `[0, 1, 1, 2]`?
- Which annotation would accept `(1.0, 3)`?

### Annotation reference

A non-exhaustive list of useful types you may need:

| Type Annotation | Meaning |
|---|---|
| **Built-in** | |
| `list[int]` | A list of integers |
| `tuple[int, float]` | A pair with an integer first and a float second |
| `dict[str, float]` | A dictionary with string keys and floating-point values |
| `int \| None` | An integer or `None` |
| **`from typing`** | |
| `Literal["forward", "reverse"]` | One of these two exact values |
| `Any` | Any value, with most static checks on its use skipped |
| `Self` | The type of the current class |
| **`from collections.abc`** | |
| `Iterable[int]` | Something you can iterate over to get integers |
| `Sequence[int]` | A sequence of integers with a length and indexed access |
| `Callable[[int], list[int]]` | A callable that takes an integer and returns a list of integers |

### Update docstrings for annotated code

Now we've added some type hints, do we need argument/return types in docstrings?
Let's see how the documentation looks now we've added type hints,

```bash
uv run sphinx-build -b html docs docs/_build/html
open docs/_build/html/index.html
```

The API type hints render the type hints as expected. This means we can simplify our
docstring for `fibonacci`, currently

```text
    Args:
        n (int): Number of terms; a non-negative Python integer, excluding bool.

    Returns:
        list: The first n terms, or an empty list when n is zero.
```

by removing `type` and `list` description. This helps a lot when we write the 
docstring for `plot_sequence`. It can now be something as simple as:

```text
    Args:
        sequence: Function that generates terms given a requested count.
        n: Number of terms to request.
        order: Whether to plot the terms in generated or reverse order.

    Returns:
        A figure showing each term's value against its zero-based position
        in the chosen order.
```

leaving the type hint to specify the exact signature of the `sequence` function.
To see this render add 

```rst
.. automodule:: sequence.analysis
   :members:
```

to `docs/api.rst` before re-building the docs. To make the output a little more readable
we can give each argument a new line in the API docs by adding a limit on the 
signature line length in `docs/conf.py`

```python
maximum_signature_line_length = 80
```

## 3. AI Coding Agent

A brief demo using Codex. To start working with Codex on this project, my first
prompt would be

```text
Look over this project and add and AGENTS.md file. Note that we're using uv for
project management - all tests, docs, formatting, linting should be run via uv 
```

Now let's use it to add our missing docstrings and type hints.

## 4. Putting it altogether

We now have a number of checks you should run periodically. Before opening/updating
every pull request: 1. format your code 2. run the linter, 3. run the type checker, 
4. run the full test suite 5. build the documentation.

```bash
uv run ruff format
uv run ruff check
uv run ty check src
uv run pytest --doctest-modules src/sequence tests
uv run sphinx-build -b html docs docs/_build/html
```

If you're using an AI coding agent, you can add this to your AGENTS.md.

In the next lecture, we’ll automate these checks with continuous integration.