---
orphan: true
---

# Demo: Documentation — cue sheet

## Before class

- Start from `sequence` commit `0d838a5` (lecture 3 library + README); use a working
  feature branch.
- All commands below run at the **sequence repository root**.
- Follow [walkthrough](walkthrough.md); all seven steps below match it.
- Existing checkout: use feature branch; fresh demo setup

```sh
git clone https://github.com/prashjet/sequence.git
cd sequence
git switch -c lecture-04-documentation 0d838a5
```

- set VSCode autoDocstring docstring format to numpy so we later change it to Google

## 1. Recap lecture 3

- Open README, `pyproject.toml`, `.python-version`, `uv.lock`,
  `src/sequence/__init__.py`.
- `src/` library, installed editable; NumPy runtime; **Sphinx already in dev**.
- Python 3.13; `.venv` disposable; lockfile shared. No docs directory yet.
- Sphinx missing? `uv add --dev sphinx` first → metadata, lockfile, environment updated;
  no reinitialization.

```sh
uv sync --locked
uv run python
```

- Python prompt: omit `>>>` when typing; `exit()` → shell; restart after source edits.

```pycon
>>> import sequence
>>> print(sequence.__file__)
>>> from sequence import even
>>> print(even(5))
[0. 2. 4. 6. 8.]
>>> exit()
```

- Expected: import from `src/sequence/__init__.py`; `[0. 2. 4. 6. 8.]`.
- Actual code uses `2.` → floats. Keep behavior; no packaging changes.

## 2. Styles → docstring → help()

- Open
  [Napoleon's Google vs NumPy examples](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#google-vs-numpy).
- Google: `Args:` and indented entries. NumPy: underlined `Parameters` headings.
- Recommend **Google style** for this course; keep one style throughout a project.
- Inspect actual `even(n)`: `2.*np.arange(n)`. Keep NumPy import and `hello()`.
- Replace only `even` in `src/sequence/__init__.py`:

- demo autocomplete of docstrings: initial default is numpy so we later change it to
  Google

```python
def even(n):
    """Return the first n non-negative even numbers as floats.

    Args:
        n (int): Number of values; use a non-negative integer.
            Input is passed to NumPy without validation.

    Returns:
        numpy.ndarray: One-dimensional float array starting at zero,
        with spacing two. Empty when n is zero.
    """
    return 2.*np.arange(n)
```

```sh
uv run python
```

```pycon
>>> from sequence import even
>>> help(even)
>>> exit()
```

- Simple function: summary, Args, Returns suffice; no need for every section.
- Docstrings work without a website; lecture 6: type hints, also shown in API reference.
- Intended input: non-negative integer; no validation added. `q` exits pager.

### Richer example — geometric

- Append to `src/sequence/__init__.py`, alongside `even` and `hello()`; no separate
  export file:

```python
def geometric(n, start=1.0, ratio=2.0):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer.")
    if n < 0:
        raise ValueError("n must be non-negative.")

    return [start * ratio**k for k in range(n)]
```

- First term: exponent zero → `start`; each next term × `ratio`; `n=0` → `[]`.
- Validation: non-Python-int/bool → TypeError; negative int → ValueError.
- Then insert this docstring immediately after the `def geometric(...)` line; keep the
  implementation below it:

```python
    """Return the first n terms of a geometric sequence.

    Args:
        n (int): Number of terms. Must be non-negative; bool is rejected.
        start (int or float): First term. Defaults to 1.0.
        ratio (int or float): Multiplier between terms. Defaults to 2.0.

    Returns:
        list: First n terms, starting with start at exponent zero.
        Empty when n is zero. Element types depend on start and ratio;
        integer arguments can produce integers.

    Raises:
        TypeError: If n is not a Python int, or is a bool.
        ValueError: If n is negative.

    Examples:
        >>> geometric(4)
        [1.0, 2.0, 4.0, 8.0]
        >>> geometric(4, start=3.0, ratio=0.5)
        [3.0, 1.5, 0.75, 0.375]
    """
```

In an interactive python session,

```pycon
>>> from sequence import geometric
>>> help(geometric)
>>> geometric(4)
[1.0, 2.0, 4.0, 8.0]
>>> geometric(4, start=3.0, ratio=0.5)
[3.0, 1.5, 0.75, 0.375]
>>> exit()
```

- Args: defaults/restrictions; Returns: list; Raises: actual checks; Examples: two
  sequences.
- `start`/`ratio`: numeric intended inputs, no validation.
- `geometric(4, start=1, ratio=2)` → `[1, 2, 4, 8]`; don't promise floats.
- the examples are not exectued - see `doctest` next week

- commit the docstrings!

## 3. Basic Sphinx site

```sh
uv run sphinx-quickstart docs
```

- Prompts: separate source/build directories **n**; project **sequence**; author
  **Prashin Jethwa**; release **0.1.0**; language **en**.
- Inspect generated `docs/conf.py`, `docs/index.rst`, `docs/Makefile`, `docs/make.bat`.
- Sphinx: text sources → HTML (default). No separate source directory.
- `conf.py`: metadata, empty extensions, `_build` excluded, Alabaster theme.
- `index.rst`: landing page, reStructuredText; Makefile/make.bat: optional build
  helpers.

- build the template docs

```sh
uv run sphinx-build docs docs/_build/html
```

- Now replace generated `docs/index.rst` with:

```rst
sequence
========

Generate numerical sequences with a small Python package.

Installation
------------

From a clone, in your own Python environment::

    pip install .

First result
------------

Start with five non-negative even numbers::

    from sequence import even
    print(even(5))

Expected output::

    [0. 2. 4. 6. 8.]

The sequence starts at zero; five is the number of values, not the endpoint.
```
```sh
uv run sphinx-build docs docs/_build/html
```

- Sources: `docs/`; generated HTML: `docs/_build/html/`. Ignore `docs/_build/` in
  `.gitignore`.
- Open `docs/_build/html/index.html` directly in your browser (e.g. double-click it in
  the file manager).
- Rebuild after edits, then refresh the browser.

## 4. Theme = presentation

- Browse [Sphinx Themes](https://sphinx-themes.org/) for examples; use Furo for this
  demo.

```sh
uv add --dev furo
```

- Set `html_theme = "furo"` in `docs/conf.py`; rebuild, refresh. Same content, new
  presentation.

## 5. Extensions = functionality

- Built into Sphinx: autodoc imports code; napoleon lets Sphinx interpret our structured
  Google-style docstrings.
- Replace empty extensions list in `docs/conf.py`:

```python
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
napoleon_google_docstring = True
napoleon_numpy_docstring = False
```

- Create `docs/api.rst`:

```rst
API reference
=============

.. autofunction:: sequence.even
```

- Append to `docs/api.rst`:

```rst
.. autofunction:: sequence.geometric
```

- Append to `docs/index.rst`:

```rst
.. toctree::
   :maxdepth: 2

   api
```

- Rebuild: `even` inputs/return; `geometric` defaults, exceptions, examples.
- Edit docstring; rebuild, refresh → API updates.
- Installed package supplies imports: no `sys.path` workaround.

- Alternative: replace individual directives with all documented public members:

```rst
.. automodule:: sequence
   :members:
```

- Don't combine: duplicate entries. `:undoc-members:` also lists undocumented functions.

## 6. Executable Markdown: MyST-NB

- Handwritten outputs → execute examples during build; catch outdated examples.
- MyST: Markdown + Sphinx directives/roles; MyST-NB adds notebooks/execution.
- Reads ordinary Markdown too; enable `myst_nb`, **not also `myst_parser`**.

```sh
uv add --dev myst-nb ipykernel
uv run python -m ipykernel install --sys-prefix --name sequence-docs
```

- Named kernel → project Python, installed `sequence` + NumPy.
- Re-register after recreating `.venv` or if kernel not found.
- In `docs/conf.py`, update extensions/add execution settings; keep other settings:

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_nb",
]
nb_execution_mode = "force"
nb_execution_raise_on_error = True
```

- `force`: run whenever page is built; execution error → failed build.
- Create `docs/example.md`; metadata marks notebook/selects kernel:

````
---
file_format: mystnb
kernelspec:
  name: sequence-docs
  language: python
---

# Generate even numbers

Our goal is to generate five values, starting at zero.

```{code-cell} ipython3
from sequence import even

n = 5
values = even(n)
print(values)
```

The result contains `n` values, with a spacing of two.
````

- Replace `docs/index.rst` toctree:

```rst
.. toctree::
   :maxdepth: 2

   api
   example
```

```sh
uv run sphinx-build docs docs/_build/html
```

- Open example: computed `[0. 2. 4. 6. 8.]`; ordinary code fences don't execute.
- `n = 5` → `n = 8`; “five values” → “eight values”; rebuild, refresh.
- Output: `[ 0.  2.  4.  6.  8. 10. 12. 14.]`; computed, not pasted.
- Temporarily import `missing_function` instead of `even`; rebuild → failure.
- Restore `from sequence import even`; rebuild → success.

## 7. Sharing online / further possibilities

- Local HTML built; online access needs hosting. No deployment today.
- GitHub Pages: hosts HTML; automatic build/deploy in **Continuous integration**.
- Read the Docs: builds/hosts versions; **Publishing and citing a release**.
- Keep sources + dependency files in Git; regenerate HTML.
- Possibilities: equations; cross-references; Intersphinx → other projects' APIs.
- Computed plots; caching → expensive examples; doctest → check `>>>` outputs.
- Autosummary → API tables/pages; builders → EPUB/PDF via LaTeX.
- Automated hosting; release-matched documentation versions.
- Return to slides: **Writing useful documentation**.
