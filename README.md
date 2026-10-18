# Open Source Software Development for Astronomy — course site

Source for the course site, built with Sphinx and deployed to GitHub Pages:
**https://prashjet.github.io/oss4astro-course/**

Each lecture page renders two ways from the same source: a normal scrolling
docs page, and (under `/present/...`) an actual reveal.js slideshow.

## Structure

```
docs/
├── conf.py                   Sphinx config
├── index.md                  site landing page
├── _static/
│   └── revealjs-custom.css   global overrides for the slide deck (see
│                              comments in the file for what each rule
│                              fixes and why)
├── examples/                 placeholder for the evolving example package
│                              used in later lectures' live demos (not
│                              wired up yet)
└── lectures/
    └── NN_topic/
        ├── slides.md         the lecture's slide deck (one file, ## per
        │                      slide; see "Authoring slides" below)
        ├── walkthrough.md    student-facing demo write-up, if the
        │                      lecture has a hands-on demo
        ├── demo_script.md    instructor's own terse command script for
        │                      the live demo - not linked from the site nav
        └── figs/             images for that lecture
```

Lecture order (`01_motivation` … `10_community_building`) reflects the
restructured 2026 syllabus: documentation comes right after environment
setup and before testing/code quality, so the example package already has
docstrings by the time students start testing it. Only `01_motivation` has
been migrated from the old slide decks so far; the rest are empty
scaffolding.

## Building locally

```bash
pip install -r requirements-docs.txt

sphinx-build -b html docs docs/_build/html          # docs pages
sphinx-build -b revealjs docs docs/_build/revealjs  # slide decks
cp -r docs/_build/revealjs docs/_build/html/present # merge the two
```

Open `docs/_build/html/index.html`, or a specific lecture's
`docs/_build/html/present/lectures/NN_topic/slides.html` for its deck.

## Deployment

`.github/workflows/deploy-docs.yml` runs both builds and publishes to
GitHub Pages automatically on every push to `main`. No manual deploy step.

## Authoring slides

- One `##` heading per slide (sphinx-revealjs slices on heading depth, not
  on `---`/thematic breaks - those render as a stray `<hr>` if you add
  them, they don't create a slide break).
- For side-by-side content (a figure beside text, a table split across
  columns), wrap in raw HTML using reveal.js's built-in `r-hstack`:

  ```html
  <div class="r-hstack">
  <div>

  - bullet content

  </div>
  <div>

  ![alt](figs/image.jpeg)

  </div>
  </div>
  ```

  MyST passes raw HTML through natively, and `revealjs-custom.css` handles
  sizing/alignment for anything placed this way.
- A slide that overflows the canvas isn't silently scrolled or clipped -
  there's no fallback for that by design. If a slide is too dense, split
  it (another `##`) or lay it out with `r-hstack` rather than shrinking
  text to fit.
