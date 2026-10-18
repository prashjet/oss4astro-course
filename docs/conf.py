# Minimal Sphinx scaffold. Extended as the site is built out.

project = "Open Source Software Development for Astronomy"

extensions = [
    "myst_parser",  # markdown support
    "sphinx_revealjs",  # build slides.md as reveal.js decks via `-b revealjs`
]

source_suffix = {
    ".md": "markdown",
}

exclude_patterns = ["_build"]

revealjs_style_theme = "white"
