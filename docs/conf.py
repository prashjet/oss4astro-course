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
revealjs_static_path = ["_static"]
revealjs_css_files = ["revealjs-custom.css"]
revealjs_script_conf = {
    # top-align content instead of vertically centering it, so any
    # overflow (see revealjs-custom.css) extends predictably downward
    # into the scroll area rather than clipping above the fold too.
    "center": False,
}
