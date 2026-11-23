---
orphan: true
---

# Walkthrough: Testing Python software

This walkthrough follows the live demo using [sequence](https://github.com/prashjet/sequence). Run shell commands from the repository root. Text at a Python prompt (`>>>`) is Python, not a shell command. The goal is to test a specified behaviour, then ask how strong those tests are.

## 1. Set up

Continue from the lecture 4 checkout:

```bash
git clone https://github.com/prashjet/sequence.git
cd sequence
git switch -c lecture-05-testing 0d838a5
uv sync --locked
```

We'll install each testing tool as we introduce it.

Create a `tests/` directory, then install pytest:

```bash
uv add --dev pytest
```

This updates `pyproject.toml`, `uv.lock`, and the local environment. We use `--dev` because pytest is needed to develop and test the package, but not to use it.

`uv run` runs commands in the project's environment.

## 2. Specify and implement Fibonacci

A function's **contract** describes what callers can expect: which inputs it accepts, what it returns, and what errors it raises.

**Contract:** `fibonacci(n)` returns a Python list containing the first `n` Fibonacci numbers, starting `0, 1`; subsequent terms are the sum of the previous two. `n` must be a non-negative Python `int`; reject `bool` despite it being an `int` subclass. Return `[]` for zero. Raise `TypeError` for other types and `ValueError` for negative integers.

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

We chose to reject `True` even though `bool` is a subclass of `int`. In the next section, we'll write a test that makes sure `fibonacci` honours that choice.

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

Pytest discovers `test_*.py` files and `test_` functions. The report should show one passed test.

Temporarily change the expected last value to `8`, rerun and inspect pytest's comparison. Restore `5` and rerun.

A failure is useful information: check whether the implementation or the expectation is wrong before changing either.

### Test multiple inputs with parametrization

Often we want to test the same behaviour for several different inputs. Rather than writing a separate test function for each case, pytest lets us **parametrize** a test.

Add this test below the first one:

```python
@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, []), (1, [0]), (2, [0, 1])],
)
def test_boundaries(n, expected):
    assert fibonacci(n) == expected
```

The `@pytest.mark.parametrize` decorator tells pytest to run `test_boundaries` three times, once for each `(n, expected)` pair. Each run is collected and reported as a separate test case, so we can see exactly which input fails.

Run pytest again:

```bash
uv run pytest -v
```

Notice that pytest reports three separate cases for `test_boundaries`, even though we've written only one test function.

### Test invalid inputs

We should also check that the function rejects inputs that violate its specification. Pytest provides `pytest.raises` to verify that a particular exception is raised.

Add this test:

```python
@pytest.mark.parametrize("n", [1.5, "3", True, None])
def test_non_integer_n_is_rejected(n):
    with pytest.raises(TypeError, match="integer"):
        fibonacci(n)
```

Here, `pytest.raises` checks the exception type, while `match` checks that its message contains the specified text. The test uses parametrization again, this time with just one parameter, `n`.

Notice that `True` is included: Python treats booleans as integers, so we need to explicitly reject them if our function is intended to accept integers but not booleans.

Run pytest again. It should now collect eight test cases in total.

## 4. Test examples in docstrings

In the previous lecture, we included examples in our docstrings using the `>>>` syntax. These examples illustrate how to use a function, but they aren't automatically tested when we build the documentation.

Pytest can execute these examples and check that their outputs match what we've documented:

```bash
uv run pytest -v --doctest-modules src/sequence
```

The `--doctest-modules` option tells pytest to look for `>>>` examples in Python docstrings. Each docstring containing examples is collected as a test, and pytest compares the actual output with the expected output.

Try deliberately introducing an error: in the Fibonacci docstring, change the expected final value from `5` to `8`. Run the command again and inspect the failure message.

Restore the correct value and verify that the test passes.

**A limitation:** Doctest compares displayed output, which can make tests sensitive to formatting and floating-point precision. For more sophisticated numerical tests, use ordinary pytest assertions with `pytest.approx` or NumPy's testing utilities.

Finally, run our regular tests and docstring examples together:

```bash
uv run pytest -v --doctest-modules src/sequence tests
```

## 5. Measure test coverage

So far, we've checked whether our tests pass. But how much of our code are we actually testing?

We can measure this using **coverage**, which records which lines of code are executed during our tests.

First, install the pytest coverage plugin:

```bash
uv add --dev pytest-cov
```

Then run:

```bash
uv run pytest --doctest-modules src/sequence tests --cov=sequence --cov-report=term-missing
```

The report shows the percentage of lines executed in each module, along with any lines that weren't reached.

We can also measure **branch coverage**, which checks whether different paths through conditional statements have been exercised:

```bash
uv run pytest --doctest-modules src/sequence tests --cov=sequence --cov-branch --cov-report=term-missing
```

Inspect the coverage report. We haven't yet tested what happens when `n` is a negative integer, so the branch that raises `ValueError` should be missing.

Add the missing test to `tests/test_fibonacci.py`:

```python
def test_negative_n_is_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        fibonacci(-1)
```

Run the coverage command again.

The negative-input branch should now be covered. We may have exercised every branch in `fibonacci()`, but the reported coverage percentage applies to the measured package, which may contain other functions or modules.

The regular test suite now has nine cases.

**But does exercising every branch mean our function is correct?** Could we introduce a bug that our tests wouldn't detect, without changing the coverage at all?

We'll return to that question in the slides, where we'll discuss what makes a **good test**, rather than simply a test that executes some code.

## 6. Property-based testing with Hypothesis

We've seen how tests can check general properties, rather than just particular input-output pairs. **Hypothesis** lets us test those properties across many automatically generated inputs.

Let's use our Fibonacci function to demonstrate.

The Fibonacci sequence satisfies the **recurrence relation**

\[
F_n = F_{n-1} + F_{n-2}, \qquad n \geq 2
\]

In other words, each number is the sum of the previous two.

Rather than checking this for a few values of `n` that we choose ourselves, we can ask Hypothesis to generate many values and check the relationship for each one.

First, install Hypothesis:

```bash
uv add --dev hypothesis
```

Create a new test file, `tests/test_properties.py`:

```python
from hypothesis import given, strategies as st

from sequence import fibonacci


@given(st.integers(min_value=2, max_value=100))
def test_fibonacci_recurrence(n):
    seq = fibonacci(n + 1)
    assert seq[n] == seq[n - 1] + seq[n - 2]
```

The `@given` decorator tells Hypothesis to supply values of `n` to our test. `st.integers(min_value=2, max_value=100)` describes the allowed inputs.

Run:

```bash
uv run pytest -v tests/test_properties.py
```

Pytest reports one passing test, but Hypothesis has checked the property for many different values of `n`.

### How does Hypothesis choose its inputs?

**Is it just choosing random numbers?**

Not quite. Hypothesis uses generated inputs, including pseudorandom exploration, but also deliberately explores interesting cases such as boundary values. It uses feedback from test execution to guide its search.

For our integer strategy, values near the ends of the range, such as `2` and `100`, are among the interesting cases it may explore.

**What does it do that parametrization doesn't?**

With pytest parametrization, we explicitly provide every case:

```python
@pytest.mark.parametrize("n", [2, 3, 10, 100])
def test_fibonacci_recurrence(n):
    ...
```

With Hypothesis, we describe the allowed inputs and let the library generate examples:

```python
@given(st.integers(min_value=2, max_value=100))
def test_fibonacci_recurrence(n):
    ...
```

Hypothesis can explore combinations we might not have thought to include manually. This is especially useful when a function accepts several inputs, arrays, strings or more complicated data structures.

It doesn't guarantee that every possible input is tested, and it doesn't replace carefully chosen examples with known expected results.

### See a failing property

Temporarily change the assertion to:

```python
assert seq[n] == seq[n - 1] + seq[n - 2] + 1
```

Run the test again:

```bash
uv run pytest -v tests/test_properties.py
```

Hypothesis reports a failing input. Since the assertion is now wrong for every valid `n`, the test fails regardless of which value is chosen.

Restore the original assertion and rerun.

**The key distinction:** We specify the property and the allowed inputs; Hypothesis chooses examples to test it.

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
| `--cov=sequence --cov-report=term-missing` | Measure line coverage and identify untested lines. |
| `--cov-branch` | Also measure branch coverage. |
| `--cov-fail-under=75` | Fail the test run if total coverage is below 75%. |
| `uv add --dev hypothesis` | Add Hypothesis for property-based testing. |
| `@given(...)` and `st.integers(...)` | Describe allowed inputs and test a property using generated examples. |

### Key ideas

- **Tests** check expected behaviour, including boundary cases and invalid inputs.
- **Coverage** reveals which code has been exercised, but doesn't establish correctness.
- **Parametrization** runs cases we explicitly choose.
- **Property-based testing** explores generated inputs, complementing tests of specific examples.