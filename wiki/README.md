# `wiki/` — source for the GitHub Wiki

These Markdown files are the **source** of the project's GitHub Wiki, kept in the main
repo so they're versioned and reviewable in pull requests. The GitHub Wiki itself lives
in a *separate* git repository (`<repo>.wiki.git`); the files here are published to it.

## Pages
- `Home.md` — landing page (what the tutorial is, how to run, the notebook map)
- `Setup-help.md` — install Python/conda, open Jupyter, fix common errors
- `ML-glossary.md` — every term in one sentence + a nanoindentation example
- `Datasets.md` — the shipped data and its licences (with an overview image)
- `FAQ.md` — kernel restarts, shape errors, the Colab clone note, etc.
- `From-notebook-to-your-own-data.md` — plug your own maps/curves into the helpers
- `Going-further.md` — advanced/optional directions and references
- `_Sidebar.md` — the wiki navigation sidebar
- `images/` — figures embedded by the pages

## Publishing to the GitHub Wiki

The wiki repo exists once the Wiki has been enabled and initialised on GitHub
(create any page once via the web UI, or just push to it if wikis are enabled).
Then, from the repo root:

```bash
# 1. Clone the wiki repo next to this one
git clone https://github.com/edrossi93/mecanano-ml-nanomechanics.wiki.git

# 2. Copy the pages and images across (everything except this README)
cp wiki/*.md                mecanano-ml-nanomechanics.wiki/
mkdir -p                    mecanano-ml-nanomechanics.wiki/images
cp wiki/images/*            mecanano-ml-nanomechanics.wiki/images/
rm -f                       mecanano-ml-nanomechanics.wiki/README.md   # this file isn't a wiki page

# 3. Commit and push
cd mecanano-ml-nanomechanics.wiki
git add .
git commit -m "Update tutorial wiki"
git push
```

> Keep the same rules as the repo: **no private paths, no proprietary data** in any
> wiki page.
