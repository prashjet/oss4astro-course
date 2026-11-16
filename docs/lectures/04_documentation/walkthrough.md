---
orphan: true
---

# Walkthrough: Documentation

This walkthrough follows the live demo using [sequence](https://github.com/prashjet/sequence).
Run terminal commands from the **sequence repository root**, unless stated otherwise.
We build a site in stages: a written page, a new theme, generated API reference,
and an executable example, then discuss hosting options.

## 1. Recap: where we left off

Open your lecture 3 checkout. To start from the same revision as the demo:

```sh
git clone https://github.com/prashjet/sequence.git
cd sequence
git switch -c lecture-04-documentation 0d838a5
```

An existing checkout does not need cloning again. Use your usual feature-branch workflow.
Inspect `README.md`, `pyproject.toml`, `.python-version`, `uv.lock`, and
`src/sequence/__init__.py`. There is no documentation directory yet.

- The README explains installation, use, and editable development.
- `even(n)` lives in `src/sequence/__init__.py`; `hello()` is a starter function we leave alone.
- NumPy is a runtime dependency; Sphinx is already under `[dependency-groups].dev`.
- Python is pinned to 3.13, consistent with `requires-python = ">=3.13"`.
- The lockfile records resolved dependencies; `.venv` is the disposable local environment.

Let's ensure our environment is up to date (`uv sync --locked`) then open an interactive python session in that enviroment

```sh
uv run python
```

At the Python prompt (`>>>`), enter the statements below without typing the
prompt characters. `exit()` returns to the shell. Start a fresh Python session
after editing the package so imports pick up the changed source.

```pycon
>>> import sequence
>>> print(sequence.__file__)
>>> from sequence import even
>>> print(even(5))
[0. 2. 4. 6. 8.]
>>> exit()
```

The import path should end in `src/sequence/__init__.py`; the output is
`[0. 2. 4. 6. 8.]`. The implementation multiplies by `2.`, so it returns floats.
`uv sync --locked` installs the package in editable mode and includes dev tools.
If your own checkout has no Sphinx dev dependency, run `uv add --dev sphinx` first;
this updates `pyproject.toml`, `uv.lock`, and the environment. Do not reinitialize the project.

## 2. Docstrings

First open [Napoleon's Google vs NumPy examples](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#google-vs-numpy)
and compare the two versions of the same function. Google style uses headings
such as `Args:` followed by indented entries; NumPy style uses underlined
headings such as `Parameters`. Both communicate similar information.
I prefer **Google style** stylistically. The important point is to stay consistent across your project. We will explain Napoleon's role when we enable it in the website later.

### Adding a docstring for `even`

Inspect `src/sequence/__init__.py`: `even(n)` returns `2.*np.arange(n)`.
It starts at zero and returns a NumPy array of floats, with no input validation.
Add the following docstring:

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

This short docstring explains the purpose, intended input, and return value. We can now read the docstring directly from Python:

```sh
uv run python
```

```pycon
>>> from sequence import even
>>> help(even)
>>> exit()
```

You should see `even(n)` and the new text. If a pager opens, press `q` to exit.
Docstrings are useful even without a website.

Note: in lecture 6 on **Code quality**, we will add type hints to our functions.
These can also appear in the generated API reference, reducing the need
to repeat types in docstrings.

### A richer example: `geometric` sequence

To illustrate defaults, validation, exceptions, and examples, append the following
function to **`src/sequence/__init__.py`**, alongside the existing functions:

```python
def geometric(n, start=1.0, ratio=2.0):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer.")
    if n < 0:
        raise ValueError("n must be non-negative.")

    return [start * ratio**k for k in range(n)]
```

This package defines functions directly in `__init__.py`, so adding the function
there makes `from sequence import geometric` work. No separate module or export
list is needed. The first term uses exponent zero: `start * ratio**0` is `start`.
Each subsequent term multiplies by `ratio`. Zero terms produces an empty list.

Now insert this Google-style docstring immediately after the
`def geometric(n, start=1.0, ratio=2.0):` line, leaving the implementation below it:

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

`Args` records defaults and the restriction on `n`. `Raises` describes the actual
checks: non-`int` input and booleans cause `TypeError`; negative integers cause
`ValueError`. The function does not validate `start` or `ratio`; the descriptions
show the intended numeric inputs. Integer arguments can produce integer terms,
so `Returns` deliberately describes a list without promising float elements.

Inspect the documentation and try both examples:

```sh
uv run python
```

```pycon
>>> from sequence import geometric
>>> help(geometric)
>>> geometric(4)
[1.0, 2.0, 4.0, 8.0]
>>> geometric(4, start=3.0, ratio=0.5)
[3.0, 1.5, 0.75, 0.375]
>>> exit()
```

Note that the example code in the docstring is not executed when calling
`help()` or building API documentation with `autodoc` (see below).
We can run these examples and check their expected output using Python’s
[doctest](https://docs.python.org/3/library/doctest.html) module,
which we will cover in the next lecture on **Testing**.

## 3. Create and preview a basic Sphinx site

[Sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html) translates
source documents into HTML. Use its quickstart command to generate the initial setup:

```sh
uv run sphinx-quickstart docs
```

Answer the prompts as follows (substitute your own name for your own project):

| Prompt | Answer |
|---|---|
| Separate source and build directories | `n` |
| Project name | `sequence` |
| Author name(s) | `Prashin Jethwa` |
| Project release | `0.1.0` |
| Project language | `en` |

Choosing `n` keeps source files directly in `docs/` and generated output under
`docs/_build/`, matching all the commands below. Quickstart creates `docs/conf.py`
(configuration), `docs/index.rst` (landing page), and `docs/Makefile` and
`docs/make.bat` (build helpers). We will use `uv run sphinx-build` directly so the
same command works across platforms and uses the project environment.

Open the generated `docs/conf.py`: note the project metadata, empty `extensions`
list, `exclude_patterns` containing `_build`, and default `alabaster` theme.
Keep this generated configuration for now.

Replace the generated `docs/index.rst` with the following
(reStructuredText, Sphinx's native markup):

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

Build from the repository root:

```sh
uv run sphinx-build docs docs/_build/html
```

`docs/` contains the sources we edit; `docs/_build/html/` contains generated HTML.
Add `docs/_build/` to `.gitignore` if it is not already ignored. Keep source files
in Git, not the generated site. HTML is the default output format.

Open `docs/_build/html/index.html` directly in your browser, for example by
double-clicking it in your file manager. No local web server is needed for this
demo. After editing a source file, run the build command again and refresh the
browser to see the changes.

## 4. Change the presentation with a theme

Browse [Sphinx Themes](https://sphinx-themes.org/) to see different ways to present
your documentation. We will use Furo for this demo.

Install [Furo](https://pradyunsg.me/furo/quickstart/) as another development dependency:

```sh
uv add --dev furo
```

In `docs/conf.py`, replace `html_theme = "alabaster"` with `html_theme = "furo"`.
Run the same build command and refresh the browser. The content is unchanged;
the theme controls presentation and navigation styling.

## 5. Add functionality with extensions

Extensions add capabilities to Sphinx documentation. Two extensions which ship with Sphinx are:

- [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html): imports Python objects and includes their docstrings.
- [Napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html): lets Sphinx interpret the structured Google-style sections we wrote earlier.

Replace `extensions = []` in `docs/conf.py` with:

```python
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
napoleon_google_docstring = True
napoleon_numpy_docstring = False
```

Create `docs/api.rst`:

```rst
API reference
=============

.. autofunction:: sequence.even
```

Append this directive to `docs/api.rst` to include the docstring for
`geometric` too:

```rst
.. autofunction:: sequence.geometric
```

Alternatively, you can document all public functions in the module using
`automodule` with the `:members:` option:

```rst
.. automodule:: sequence
   :members:
```

Use this **instead of** the individual `autofunction` directives to avoid
duplicate entries. By default, only members with docstrings are included.
Add `:undoc-members:` if you also want to list undocumented functions.

Append this table of contents to `docs/index.rst`:

```rst
.. toctree::
   :maxdepth: 2

   api
```

Rebuild and open **API reference**. You should see `sequence.even(n)`, its parameters
and return value. `sequence.geometric` also shows defaults, exceptions,
and examples.

Because we run Sphinx with uv run, it can import the installed sequence package and read its docstrings. Edit a docstring, rebuild the documentation, and refresh the browser to see the API reference update.

## 6. Compute a worked example with MyST-NB

So far, all the examples in our documentation have been written in by hand. What if we wanted these to be actual code, which is executed to produce output when the documentation builds?

MyST is a Markdown dialect with Sphinx directives and roles. MyST-NB builds on
its parser to read and execute notebook pages. It also reads ordinary Markdown. Enable `myst_nb` without also adding
`myst_parser` to `extensions`: MyST-NB already supplies the Markdown parser.

Install the MyST-NB extension and the Python kernel:

```sh
uv add --dev myst-nb ipykernel
```

We tell the documentation examples to use this project’s Python environment.

```sh
uv run python -m ipykernel install --sys-prefix --name sequence-docs
```

Repeat this registration after recreating `.venv`. If the build reports that
`sequence-docs` cannot be found, rerun the kernel registration command.

We can edit `docs/conf.py` to include the `myst_nb` extension, along with two new settings:

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_nb",
]
nb_execution_mode = "force"
nb_execution_raise_on_error = True
```

`nb_execution_mode = "force"` runs the examples whenever their page is built.
`nb_execution_raise_on_error = True` fails the build if an example fails.
Keep the other settings already in `conf.py`. See the MyST-NB documentation for
more [execution](https://myst-nb.readthedocs.io/en/latest/computation/execute.html)
and [configuration](https://myst-nb.readthedocs.io/en/latest/configuration.html) options.

We can now write a Markdown documentation page containing executable code. Create `docs/example.md` with the following complete contents. The YAML metadata
marks this Markdown file as a notebook and selects the kernel we registered
([text notebook format](https://myst-nb.readthedocs.io/en/latest/authoring/text-notebooks.html)):

````markdown
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

Replace the table of contents at the bottom of `docs/index.rst` with:

```rst
.. toctree::
   :maxdepth: 2

   api
   example
```

Build and open **Generate even numbers**. The code cell should display the computed
output `[0. 2. 4. 6. 8.]`. A normal fenced Python block displays code but does not execute;
the `{code-cell}` directive requests execution.

Change `n = 5` to `n = 8` in `docs/example.md`, and update “five values” to “eight values”.
Rebuild and refresh: the output should now be `[ 0.  2.  4.  6.  8. 10. 12. 14.]`.
The output is computed from the code, not copied into the page.

To see what happens when an example stops working, temporarily change the import
in `docs/example.md` to `from sequence import missing_function`, then rebuild.
The build should fail because that function does not exist. Restore
`from sequence import even` and rebuild successfully. This helps catch examples
that become outdated as the package changes.

## 7. Sharing your documentation online

We have built the HTML documentation and opened the local
`index.html` in a browser.

To make it accessible to other people, we need to host it online.
Options include:

- **GitHub Pages:** hosts the HTML generated by Sphinx. In the
  **Continuous integration** lecture, we will set up a workflow
  to build and publish the documentation automatically.

- **Read the Docs:** builds and hosts documentation, with support
  for multiple versions corresponding to branches and releases.
  We will explore this in **Publishing and citing a release**,
  so users can find documentation matching their installed version.

For now, keep the documentation source and dependencies in your
repository. The generated HTML can be rebuilt from them.

### Further possibilities

| Functionality | What could you use it for? |
|---|---|
| Mathematical notation | Explain algorithms and scientific assumptions using equations. |
| Cross-references | Link to functions, sections, equations, and figures elsewhere in your docs. |
| Intersphinx | Link directly to API documentation in other projects, such as NumPy. |
| Plot outputs | Generate figures from executable examples using e.g. MyST-NB and Matplotlib |
| Execution caching | Reuse computed outputs to avoid rerunning expensive examples unnecessarily. |
| `doctest` | Check that examples written with `>>>` produce their expected output. |
| `autosummary` | Generate API summary tables and individual reference pages. |
| Additional builders | Produce formats such as EPUB or PDF through LaTeX. |
| Automated hosting | Build and publish with GitHub Pages in the **Continuous integration** lecture. |
| Versioned documentation | Publish documentation matching software releases with Read the Docs in **Publishing and citing a release**. |