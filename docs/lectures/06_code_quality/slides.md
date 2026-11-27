---
orphan: true
---

# Code quality
Linting, formatting, and type hints

## What can we check *before* running the code?

| Check | What does it check? | Tool |
|---|---|---|
| Formatting | Is the layout consistent? | Ruff |
| Linting | Are there likely mistakes, such as undefined names? | Ruff |
| Type checking | Do the types match what the code expects? | ty |

## Why do we do this?

Benefits:

- consistent style makes the code easier to read and changes easier to review,
- linters and type checkers can catch mistakes in code that the tests don’t exercise,
- type hints help readers see what a function expects and what it returns,
- removes friction from developing and using your software

## Live demo

Let's demo this using the `sequence` package

````{only} revealjs
```{raw} html
<a href="../../../lectures/06_testing/walkthrough.html">Walkthrough</a>
```
````

```{only} html and not revealjs
[Walkthrough](walkthrough.md)
```

## Project Requirements

- Add type hints to function and method signatures throughout your codebase. Annotate
  parameters and return values.
- Use Ruff to format and lint your code. Before submitting, run `ruff format --check`
  and `ruff check` from the repository root.
- (*) Use `ty` to type-check your package.

## Coding agents

- AI coding agents have transformed software devlopment
- Company / Chatbot / Coding agent:
  - Anthropic / Claude / Claude Code
  - OpenAi / ChatGPT / Codex
  - Google / Gemini / Antigravity
- quick demo + discussion