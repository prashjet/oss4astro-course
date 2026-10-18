# Minimal Sphinx scaffold. Extended as the site is built out.

project = "Open Source Software Development for Astronomy"

extensions = [
    "myst_parser",  # markdown support
    # slide-rendering extension (sphinx-revealjs vs hieroglyph) TBD
]

source_suffix = {
    ".md": "markdown",
}

exclude_patterns = ["_build"]
