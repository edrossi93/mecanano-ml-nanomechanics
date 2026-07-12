# CLAUDE.md — conventions for this repository

Guidance for anyone (people or AI assistants) contributing to the MecaNano
*ML for Nanomechanics* tutorial. Keep changes consistent with what's here.

## What this repo is
A hands-on companion to *Tutorial 1 — Machine learning bases and advanced
applications for nanoindentation data analysis*. Each notebook teaches one method
on real nanoindentation data. **The audience are materials researchers/students who
have never done machine learning and have little Python.** Beginner-friendliness is
the top priority, above cleverness or brevity.

## Layout
```
notebooks/   the tutorials (00–06 core, 01a/02a/03a/04a on-ramps, 10–13 classics)
src/mecanano_ml/   tiny helper package: data loaders + consistent plotting
data/        public datasets only (see data/README.md for licences)
wiki/        source for the GitHub Wiki (Home, glossary, setup, FAQ, …)
.github/     CI that executes every notebook (except 13) on push/PR
```
Notebooks stay focused on the *machine learning*: loading and plotting live in
`src/mecanano_ml/` so each notebook shows only the steps that matter.

## How to run and verify
```bash
pip install -r requirements.txt          # or: conda env create -f environment.yml
jupyter lab                              # open notebooks/00_start_here.ipynb
```
Before committing a notebook change, **run it top-to-bottom on CPU** (Kernel →
Restart & Run All) and make sure it's error-free. CI does this automatically with
`pytest --nbmake` on every push/PR; notebook 13 is optional/heavy and excluded.
Install a **CPU-only** PyTorch (`pip install torch --index-url
https://download.pytorch.org/whl/cpu`) to keep things light.

## The beginner standard (apply to every notebook)
Every notebook must have:
- a **"What you'll learn"** and **"What you need to know first"** header, and a
  **runtime** badge;
- the **first use** of any term (feature, label, PCA, cluster, overfitting, tensor,
  latent space, …) defined in **one plain sentence**, inline;
- a **one-line comment on each non-obvious code line**, and a **"what you should
  see"** note near each cell;
- a **caption in words** under each figure (what to look at and why);
- a **Recap** (3 bullets), a **"Try it yourself"** (2–3 small exercises), and a
  **Common errors** section.
Prefer explicit, named steps over clever one-liners. Keep imports at the top.

## Output policy
Notebooks are committed **with their executed outputs** so they render results on
GitHub and reinforce the "what you should see" notes. Re-run a notebook before
committing so its outputs match its code. Keep figures modest in size.

## Data rules (hard constraints)
- **Only openly-licensed data in `data/`.** Never commit data you don't have the
  right to redistribute; before adding a dataset, confirm it is cleared for public
  release and record its licence in `data/README.md`.
- The high-speed maps are **CC BY 4.0** — cite *Besharatloo & Wheeler, J. Mater.
  Res. 36, 2198–2212 (2021)*. See `data/README.md`.
- **No private file paths** (e.g. local `C:\…` / `E:\…` folders) in any committed
  file — notebooks, docs, wiki or CI.

## Method guardrails
- The latent-space notebook (`05`) stays a **plain autoencoder**: reconstruct first,
  then cluster the latent space as a **separate** step. **Do not** merge the two, i.e.
  do not add clustering into the training objective. A single "more advanced methods
  exist" line is the limit.
- Keep everything **CPU-only and fast** (a couple of minutes per notebook): small
  models, few epochs, subsampled where needed. No GPU, no large downloads in the
  core path.

## The helper package (`src/mecanano_ml/`)
- `io.py` — `load_map`, `map_to_grid`, `load_afm_grid`, `load_curves`, `list_maps`.
- `features.py` — `standardize`, `curve_scalar_features`.
- `viz.py` — `set_style`, `plot_map`, `scatter_xy`.
Lint it with `ruff check src/` (config in `ruff.toml`; the notebooks' compact style
is intentionally not linted).

## Adding a new notebook
1. Use only shipped/public data and obey the beginner standard above.
2. Keep it CPU-fast; set random seeds; assert on ranges, not exact numbers.
3. Run it end-to-end, commit with outputs, and make sure CI stays green.
4. Add it to the notebook tables in `README.md`, `notebooks/00_start_here.ipynb`,
   and the wiki `Home` page.
