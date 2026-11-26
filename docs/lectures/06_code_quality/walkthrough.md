---
orphan: true
---

# Walkthrough: Code quality

This walkthrough follows the live demo using [sequence](https://github.com/prashjet/sequence). Run shell commands from the repository root.

## 1. Set up

Start from the commit at the end of Lecture 5, which includes the Fibonacci implementation and tests.

```bash
git clone https://github.com/prashjet/sequence.git
cd sequence
git switch -c lecture-06-code-quality 0d1a625
uv sync --locked
```

If you already have a checkout, run `git fetch origin` from the repository root, then run the branch and sync commands above.
