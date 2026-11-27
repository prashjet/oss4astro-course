---
orphan: true
---

# Walkthrough: Testing Python software

This walkthrough follows the live demo using
[sequence](https://github.com/prashjet/sequence). Run shell commands from the repository
root. The goal is to test specified behaviour, then ask how strong those tests are.

## 1. Set up

Let's start from the commit at the end of lecture 4:

```bash
git clone https://github.com/prashjet/sequence.git
cd sequence
git switch -c lecture-05-testing 48a47b7
uv sync --locked
```

We'll install each testing tool as we introduce it.

Create a `tests/` directory and install pytest:

```bash
mkdir -p tests
uv add --dev pytest
```

This updates `pyproject.toml`, `uv.lock`, and the local environment. We use `--dev`
because pytest is needed to develop and test the package, but not to use it.

`uv run` runs commands in the project's environment.

## 2. Specify and implement Fibonacci

A function's **contract** describes what callers can expect: which inputs it accepts,
what it returns, and what errors it raises.

**Contract:** `fibonacci(n)` returns a Python list containing the first `n` Fibonacci
numbers, starting `0, 1`; subsequent terms are the sum of the previous two. `n` must be
a non-negative Python `int`; reject `bool` despite it being an `int` subclass. Return
`[]` for zero. Raise `TypeError` for other types and `ValueError` for negative integers.

Append this function to `src/sequence/__init__.py`; keep existing imports and functions:

```python
def fibonacci(n):
    """Return the first n Fibonacci numbers, starting with 0 and 1.

    Args:
        n (int): Number of terms; a non-negative Python integer, excluding bool.

    Returns:
        list: The first n terms, or an empty list when n is zero.

    Raises:
        TypeError: If n is not a Python int or is a bool.
        ValueError: If n is negative.

    Examples:
        >>> fibonacci(6)
        [0, 1, 1, 2, 3, 5]
        >>> fibonacci(0)
        []
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    values = []
    a, b = 0, 1
    for _ in range(n):
        values.append(a)
        a, b = b, a + b
    return values
```

We chose to reject `True` even though `bool` is a subclass of `int`. In the next
section, we'll write a test that makes sure `fibonacci` honours that choice.

## 3. Write and run tests with pytest

Create `tests/test_fibonacci.py`:

```python
import pytest

from sequence import fibonacci


def test_first_six_terms():
    assert fibonacci(6) == [0, 1, 1, 2, 3, 5]
```

Run:

```bash
uv run pytest -v tests/test_fibonacci.py
```

Pytest discovers `test_*.py` files and `test_` functions. The report should show one
passed test.

Temporarily change the expected last value to `8`, rerun and inspect pytest's
comparison. Restore `5` and rerun.

A failure is useful information: check whether the implementation or the expectation is
wrong before changing either.

### Test multiple inputs with parametrization

Often we want to test the same behaviour for several different inputs. Rather than
writing a separate test function for each case, pytest lets us **parametrize** a test.

Add this test below the first one:

```python
@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, []), (1, [0]), (2, [0, 1])],
)
def test_boundaries(n, expected):
    assert fibonacci(n) == expected
```

The `@pytest.mark.parametrize` decorator tells pytest to run `test_boundaries` three
times, once for each `(n, expected)` pair. Each run is collected and reported as a
separate test case, so we can see exactly which input fails.

Run pytest again:

```bash
uv run pytest -v
```

Notice that pytest reports three separate cases for `test_boundaries`, even though we've
written only one test function.

### Test invalid inputs

We should also check that the function rejects inputs that violate its specification.
Pytest provides `pytest.raises` to verify that a particular exception is raised.

Add this test:

```python
@pytest.mark.parametrize("n", [1.5, "3", True, None])
def test_non_integer_n_is_rejected(n):
    with pytest.raises(TypeError, match="integer"):
        fibonacci(n)
```

Here, `pytest.raises` checks the exception type, while `match` checks that its message
contains the specified text. The test uses parametrization again, this time with just
one parameter, `n`.

Notice that `True` is included: Python treats booleans as integers, so we need to
explicitly reject them if our function is intended to accept integers but not booleans.

Run pytest again. It should now collect eight test cases in total.

## 4. Test examples in docstrings

In the previous lecture, we included examples in our docstrings using the `>>>` syntax.
These examples illustrate how to use a function, but they aren't automatically tested
when we build the documentation.

Pytest can execute these examples and check that their outputs match what we've
documented:

```bash
uv run pytest -v --doctest-modules src/sequence
```

The `--doctest-modules` option tells pytest to look for `>>>` examples in Python
docstrings. Each docstring containing examples is collected as a test, and pytest
compares the actual output with the expected output.

Try deliberately introducing an error: in the Fibonacci docstring, change the expected
final value from `5` to `8`. Run the command again and inspect the failure message.

Restore the correct value and verify that the test passes.

**A limitation:** Doctest compares displayed output, which can make tests sensitive to
formatting and floating-point precision. For more sophisticated numerical tests, use
ordinary pytest assertions with `pytest.approx` or NumPy's testing utilities.

Finally, run our regular tests and docstring examples together:

```bash
uv run pytest -v --doctest-modules src/sequence tests
```

## 5. Measure test coverage

So far, we've checked whether our tests pass. But how much of our code are we actually
testing?

We can measure this using **coverage**, which records which lines of code are executed
during our tests.

First, install the pytest coverage plugin:

```bash
uv add --dev pytest-cov
```

Run:

```bash
uv run pytest --doctest-modules src/sequence tests --cov=sequence --cov-report=term-missing
```

The report shows the percentage of executable lines covered by our tests, along with any
lines that weren't reached.

For a more detailed view, generate an **HTML coverage report**:

```bash
uv run pytest --doctest-modules src/sequence tests --cov=sequence --cov-report=html
```

Open `htmlcov/index.html` in your browser. You can inspect individual source files and
see which lines were executed and which were missed.

Notice that we haven't tested what happens when `n` is a negative integer. Find the
corresponding uncovered line in `fibonacci()`.

Add the missing test to `tests/test_fibonacci.py`:

```python
def test_negative_n_is_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        fibonacci(-1)
```

Generate the HTML report again. The previously uncovered line should now be marked as
covered.

The overall coverage percentage may still be below 100%, because we're measuring the
entire `sequence` package, which contains other functions.

### Enforcing a minimum coverage threshold

For your course project, you'll need at least **75% line coverage**. You can check this
automatically:

```bash
uv run pytest --cov=sequence --cov-report=term-missing --cov-fail-under=75
```

Replace `sequence` with your own package name. The command fails if the measured
coverage is below 75%.

**But does executing every line mean our function is correct?** Could we introduce a bug
that our tests wouldn't detect, without changing the coverage?

We'll return to that question in the slides.

## 6. Property-based testing with Hypothesis

So far, we've tested specific inputs and expected outputs. But some functions also
satisfy **general properties** that we can test across many inputs.

For Fibonacci, each number after the first two is the sum of its predecessors:

```{math}
F_n = F_{n-1} + F_{n-2}, \qquad n \geq 2
```

Rather than choosing a few values of `n` ourselves, we can use **Hypothesis** to
generate inputs and check this relationship.

First, install Hypothesis:

```bash
uv add --dev hypothesis
```

Create `tests/test_properties.py`:

```python
from hypothesis import given, strategies as st

from sequence import fibonacci


@given(st.integers(min_value=2, max_value=100))
def test_fibonacci_recurrence(n):
    seq = fibonacci(n + 1)
    assert seq[n] == seq[n - 1] + seq[n - 2]
```

Run the test:

```bash
uv run pytest -v tests/test_properties.py
```

Pytest reports one passing test, but Hypothesis has checked the property for many
generated values of `n`.

### How does Hypothesis choose its inputs?

Hypothesis isn't simply choosing uniformly random numbers.

It generates inputs within the constraints we specify, using a combination of
pseudorandom exploration and deliberately interesting examples, including boundary
values.

For our integer strategy, `2` and `100` are examples of boundary values it can explore.

Hypothesis doesn't guarantee that every possible input will be tested. It explores a
selection of inputs, including edge cases, within the constraints we specify.

### How is this different from parametrization?

With pytest parametrization, **we explicitly choose the inputs**:

```python
@pytest.mark.parametrize("n", [2, 3, 10, 100])
def test_fibonacci_recurrence(n):
    ...
```

With Hypothesis, **we describe the allowed inputs**, and it generates examples:

```python
@given(st.integers(min_value=2, max_value=100))
def test_fibonacci_recurrence(n):
    ...
```

The distinction becomes particularly useful for functions accepting several parameters,
arrays, strings, or more complicated data structures, where there may be many possible
combinations to explore.

### See a failing property

Temporarily change the assertion to:

```python
assert seq[n] == seq[n - 1] + seq[n - 2] + 1
```

Run the test again:

```bash
uv run pytest -v tests/test_properties.py
```

Hypothesis reports a failing example. In this case, the assertion is wrong for every
valid input, so any generated value of `n` will reveal the failure.

Restore the original assertion and rerun the test.

**The key idea:** We specify the property and the allowed inputs; Hypothesis explores
examples that might violate it.

Property-based testing complements, rather than replaces, tests with specific known
results.

## 7. Summary: testing commands and concepts

| Command / concept | Purpose |
|---|---|
| `uv add --dev pytest` | Add pytest as a development dependency. |
| `uv run pytest` | Discover and run tests. |
| `uv run pytest -v` | Run tests with more detailed output. |
| `assert` | Check that a result matches an expectation. |
| `@pytest.mark.parametrize` | Run the same test with several specified inputs. |
| `pytest.raises(...)` | Check that invalid inputs raise the expected exception. |
| `uv run pytest --doctest-modules` | Also test `>>>` examples in Python docstrings. |
| `uv add --dev pytest-cov` | Add the coverage plugin for pytest. |
| `--cov=sequence --cov-report=term-missing` | Measure line coverage and list unexecuted lines. |
| `--cov-report=html` | Generate an HTML report showing covered and missed lines. |
| `--cov-fail-under=75` | Fail the test run if coverage is below 75%. |
| `uv add --dev hypothesis` | Add Hypothesis for property-based testing. |
| `@given(...)` and `st.integers(...)` | Describe allowed inputs and test a property using generated examples. |

### Key ideas

- **Tests** check expected behaviour, including boundary cases and invalid inputs.
- **Coverage** reveals which code has been exercised, but doesn't establish correctness.
- **Parametrization** runs cases we explicitly choose.
- **Property-based testing** explores generated inputs, complementing tests of specific
  examples.
