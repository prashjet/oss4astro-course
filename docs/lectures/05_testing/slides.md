---
orphan: true
---

# Testing Python software

Prashin Jethwa

23/11/26

## When can you trust a result?

Your code runs without errors and produces a plausible plot.

**But how do you know the result is correct?**

- Compare against a result you already know.
- Check how the code handles boundary cases and invalid inputs.
- Make sure changes to the code don't break existing behaviour.

**Automated tests let us make these checks repeatedly.**

## What is a test?

1. **Arrange** an input and the conditions.
2. **Act:** call the code.
3. **Assert** an independently expected result.

```python
from sequence import fibonacci

def test_first_six_terms():
    assert fibonacci(6) == [0, 1, 1, 2, 3, 5]
```

The expected result comes from the sequence definition, not from running the implementation once.

## Which cases should we check?

- Typical inputs and known results
- Boundaries: zero terms, one term, two terms
- Invalid inputs and useful error messages
- Scientific assumptions: units, shapes, tolerances and limiting cases

A few carefully chosen cases can reveal more than many similar ones.

## Tools for today

- **pytest** discovers tests and reports failures.
- **doctest** checks Python examples in docstrings against their displayed output.
- **pytest-cov** reports which code was executed.
- **Hypothesis** generates inputs to check properties.

These tools help us ask different questions about the same code.

## Live demo

We will add a Fibonacci sequence to our `sequence` package, test it, and examine our tests.

````{only} revealjs
```{raw} html
<a href="../../../lectures/05_testing/walkthrough.html">Walkthrough</a>
```
````

```{only} html and not revealjs
[Walkthrough](walkthrough.md)
```

## What does coverage tell us?

Coverage asks: **which lines or branches ran?**

It does not ask whether an assertion was meaningful, whether all inputs were tried, or whether the science is right.

A test can execute every line and still fail to notice a wrong result.

Use coverage to identify gaps in your tests, **not as a certificate of correctness**.

## What makes a good test?

A good test checks **behaviour**, not just whether code runs.

- **Specific:** It checks a clearly defined expectation.
- **Sensitive:** It fails when the behaviour is meaningfully wrong.
- **Independent:** It doesn't simply reproduce the implementation's logic.
- **Reproducible:** It gives the same result under the same conditions.

Ask yourself: **What plausible mistake would this test catch?**

## Exercise: design a test suite

Consider a function with the following docstring:

```python
def normalize(x):
    """
    Normalize a sequence of non-negative numbers.

    Parameters
    ----------
    x : array-like
        A one-dimensional sequence of non-negative
        numbers with a positive sum.

    Returns
    -------
    numpy.ndarray
        An array of the same length, whose elements
        sum to one.

    Raises
    ------
    ValueError
        If the input is empty, contains negative
        values, or has a sum of zero.
    """
```

**Working in pairs (10 minutes):**

Design a set of tests for this function, using only its docstring as a specification.

- What inputs would you choose?
- What assertions would you make?
- Are there general properties you could test?
- What plausible bugs would your tests detect?

## Discuss

- Which tests did you come up with?
- Would checking that the output sums to one be sufficient?
- What would happen if the function always returned a uniform distribution?
- How would you choose an appropriate numerical tolerance?
- Which tests check particular examples, and which check general properties?

**Is the specification itself sufficiently precise?**

## Property-based testing

Instead of manually choosing every test input, we can check **general properties** across many automatically generated inputs.

[Hypothesis](https://hypothesis.readthedocs.io/) is a Python library that:

- Generates inputs satisfying constraints we specify.
- Explores both generated values and interesting edge cases.
- Checks the same property across many inputs.

**How is this different from `pytest.mark.parametrize`?**

With parametrization, **we choose the test cases**. With Hypothesis, **we describe the allowed inputs**, and the library generates examples.

For our `normalize` function, we might want to test whether multiplying every input by a positive constant leaves the result unchanged.

But first, we'd need to establish that this behaviour is part of the intended specification.

## Takeaways

- **Tests check behaviour**, not just successful execution.
- **Coverage reveals untested code**, but doesn't measure correctness.
- **Good tests start from the specification**, not the implementation.
- **Examples, boundaries, errors and properties complement each other.**
- **Property-based testing** helps explore inputs we might not think to test manually.

Good tests give us confidence to change our code without inadvertently changing its behaviour.

## Further reading

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [Python doctest](https://docs.python.org/3/library/doctest.html)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/)

## Project Requirements

- Write automated tests for your Python code using **pytest** (or an equivalent testing framework).
- Achieve **at least 75% line coverage** across your package, measured using `pytest-cov` (or an equivalent coverage tool).
- In your **final presentation**, present one representative test from your test suite. Explain what behaviour it checks, why you chose it, and what kind of bug it would catch.
- (*) Include executable examples in your docstrings and test them using `pytest --doctest-modules`.
- (*) Use **Hypothesis** (or an equivalent tool) for property-based testing.