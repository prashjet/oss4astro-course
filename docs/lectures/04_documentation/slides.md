---
orphan: true
---

# Documentation

Prashin Jethwa  
16/11/26

## What do you need before using a package?

You find a package that might help with your research.

- What does it do? Is it suitable for your problem?
- How do you install it?
- How do you get a first result?
- What functions and options are available?

Documentation should help you answer these questions.

## Where does documentation live?

- **README:** the front door—purpose, installation, quick start.
- **Tutorials and guides:** worked examples and instructions for specific tasks.
- **API reference:** details of functions, classes, and their parameters.
- **Docstrings:** documentation alongside the code, accessible with `help()`.

A documentation website brings these pieces together.

Let's look at an example: the [Gala](https://gala.adrian.pw/en/latest/index.html) package for galactic dynamics.

## From docstrings to a documentation site

We can combine:

- pages we write ourselves,
- API reference generated from docstrings.

The tools handle building and presenting the documentation.

We still decide what it needs to say.

## Live Demo

Instructions to reproduce can be found [here](https://prashjet.github.io/oss4astro-course/lectures/04_documentation/walkthrough.html).

##  Writing *useful* documentation

We can now build documentation.

But can another astronomer use it?

- Where should they start?
- What will they need to know?
- What will they still have to guess?

## Write for a particular reader

Imagine an astronomer who understands the science,
but has never used your package.

They don't know:

- your terminology and conventions,
- how your code is organised,
- which steps you consider “obvious”.

Your future self may be this reader too.

## Start with the reader's task

Organise a guide around what someone wants to accomplish.

**“Measure a period from a light curve”**

Give them:

1. A clear goal.
2. The inputs they need.
3. Steps they can follow.
4. A result they can recognise and interpret.

## Make examples complete

A useful example includes:

- imports and accessible example data,
- all the steps needed to run it,
- expected output,
- an explanation of what that output means.

Could someone copy your example into a fresh session
and get the result you describe?

## Explain the scientific contract

What must be true for the result to be meaningful?

- **Units:** days or seconds?
- **Shape:** one spectrum or a collection?
- **Conventions:** normalised flux? Which reference frame?
- **Assumptions:** independent errors? Regular sampling?
- **Limits:** when should the result not be trusted?

Code can run successfully and still produce a misleading result.

## Help the reader make decisions

**Too little:**

> `window`: smoothing window size.

**More useful:**

> `window`: number of consecutive samples averaged together.
> Must be a positive odd integer.
> Larger values suppress noise but can wash out short transits.

Explain what a parameter controls,
what values are allowed, and why the choice matters.

## Explain why as well as how

“Set `threshold=5`” tells the reader what to type.

It leaves questions:

- What does the threshold measure?
- Why choose 5?
- When should I change it?
- What happens if I increase it?

Give enough reasoning for the reader to adapt the example
to their own data.

## Put detail where it helps

A first example needs a clear route to success.

An API reference needs precise, easy-to-find details.

A discussion of the method needs assumptions and reasoning.

Link between them:
the reader should be able to find more detail
without needing to read everything first.

## Test your documentation with a reader

Ask someone to complete a small task using only your docs.

Watch where they:

- hesitate,
- search,
- guess,
- ask you a question.

Resist explaining immediately.
The explanation they needed belongs in the documentation.

## Exercise: write a docstring

```python
import numpy as np

def flux_to_magnitude(flux, zero_point=25.0):
    return zero_point - 2.5 * np.log10(flux)
```

Write a docstring that would help another astronomer use this function.

What can you establish from the code?
What would you need to ask the author?

## Project requirements

Your project should include:

- A **README** explaining what the package does, how to install it, and a (optional, if appropriate) quick-start example with expected output
- **Docstrings** for public functions and classes, covering inputs, outputs, units, and relevant assumptions.
- A **published documentation site** containing the usage guide and API reference. Details about publishing covered in later lectures.
- A **worked example** with expected output and an explanation of the result.