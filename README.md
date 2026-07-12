# Machine Learning for Nanomechanics — MecaNano Tutorials

[![CI — execute notebooks](https://github.com/edrossi93/mecanano-ml-nanomechanics/actions/workflows/ci.yml/badge.svg)](https://github.com/edrossi93/mecanano-ml-nanomechanics/actions/workflows/ci.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edrossi93/mecanano-ml-nanomechanics/HEAD?labpath=notebooks%2F00_start_here.ipynb)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edrossi93/mecanano-ml-nanomechanics/blob/main/notebooks/00_start_here.ipynb)

> 🐍 **New to Python or machine learning?** You're exactly who this is for. Start with
> `notebooks/00_start_here.ipynb`; the [**wiki**](../../wiki) has a setup guide, a plain-English
> ML glossary, and an FAQ.

Hands-on companion to **Tutorial 1 — Machine learning bases and advanced
applications for nanoindentation data analysis** (MecaNano WG4). You *read a
method, then run it* on real nanoindentation data. Everything runs on a CPU in
a couple of minutes per notebook.

Each notebook is **step-by-step**: the machine-learning steps are shown in full,
while data loading and plotting live in a small helper package (`src/`) so the
method stays in focus.

## Quick start

```bash
git clone https://github.com/edrossi93/mecanano-ml-nanomechanics.git
cd mecanano-ml-nanomechanics

# option A — pip
pip install -r requirements.txt

# option B — conda
conda env create -f environment.yml && conda activate ml-nano

jupyter lab      # then open notebooks/00_start_here.ipynb
```

**No install needed to try it:**
- **Colab** — open any notebook via the badge and just run the first cell. It
  clones the repo *and* installs the few extra packages Colab lacks (~1 min, once).
- **Binder** — click the badge; the `binder/` environment uses CPU-only PyTorch so
  it builds faster.

If a fresh local `pip install -r requirements.txt` ever breaks because a library
shipped a breaking change, use the pinned known-good set: `pip install -r
requirements-lock.txt`.

## The notebooks

Read them in order; each is self-contained.

Read them in order. The **`a` notebooks are extra beginner on-ramps** — take them if you'd
like a gentler build-up.

| # | Notebook | What you learn |
|---|----------|----------------|
| 00 | `00_start_here` | the datasets and how to run everything |
| 01 | `01_features_and_pca` | curve → features, standardisation, **PCA** (scree, loadings), t-SNE/UMAP |
| 01a | `01a_linear_and_logistic_regression` | the gentlest models: fit a line (R²), predict a class (decision boundary) |
| 02 | `02_clustering_phases` | **k-means + silhouette**, **GMM** (uncertainty), **HDBSCAN** → phase map |
| 02a | `02a_knn_classifier` | classify by **nearest neighbours**; how `k` trades off overfit vs underfit |
| 03 | `03_supervised_trees_rf_shap` | **decision tree → random forest → boosting**, **SMOTE**, **SHAP**, permutation importance |
| 03a | `03a_evaluating_models` | **cross-validation**, learning curves, **precision/recall**, **ROC/PR** — trust a model |
| 04 | `04_curve_as_image_cnn` | **GAF** curve→image + a small **CNN**; shape vs scale |
| 04a | `04a_1d_cnn_on_curves` | a **1-D CNN** on the raw curve (keeps magnitude) — the other side of the lesson |
| 05 | `05_autoencoder_latent_space` | **autoencoder**, the **latent space**, anomaly detection |
| 06 | `06_correlative_registration` | aligning two maps: **NCC**, transform recovery, agreement & confusion |
| 07 | `07_substrate_layer_deconvolution` | **coating vs substrate** deconvolution (physics + ML) on a real CrN–Cr bilayer |
| 08 | `08_single_vs_depth_resolved` | **single-depth vs depth-resolved** phase mapping — one depth vs the whole curve (Al–Cu) |
| 10 | `10_cnn_mnist` | the classic MNIST **CNN** warm-up (refreshed) |
| 11 | `11_popin_detection` | a transparent **pop-in** detector, validated on a known signal |
| 12 | `12_regression_curvefitting` | Kick's-law **curve fitting** + **Random-Forest regression** |
| 13 | `13_yolo_defect_detection` | object detection in micrographs with **YOLO** (optional) |

Every notebook runs top-to-bottom on CPU; see [`RUN_REPORT.md`](RUN_REPORT.md) for the latest
run and what each one should produce.

## Data

All datasets are **openly licensed** and shipped as open, human-readable **CSV**
(see [`data/README.md`](data/README.md)):
- the **CC BY 4.0** Al–Cu / duplex-steel HSNM maps (Besharatloo & Wheeler, 2021) and MNIST;
- the author's own (CC BY 4.0) raw load–depth curves, AFM-collocated grid, the
  depth-resolved **CrN-on-Cr bilayer** used for the coating/substrate deconvolution (notebook 07),
  and a depth-resolved **Al–Cu** map used for single-depth-vs-whole-curve phase mapping (notebook 08);
- a transparent **synthetic** bilayer set for method validation.

The whole ML arc — unsupervised → supervised → multimodal → depth-resolved deconvolution —
is taught on these.

## Repository layout

```
mecanano-ml-nanomechanics/
├── notebooks/            # the tutorials (00–08 core, 01a/02a/03a/04a on-ramps, 10–13 classics)
├── src/mecanano_ml/      # shared loaders, features and plotting helpers
├── data/                 # openly-licensed datasets (+ provenance)
├── wiki/                 # source for the GitHub Wiki (setup, glossary, FAQ)
├── .github/workflows/    # CI: executes every notebook on push/PR
├── requirements.txt      # pip install -r requirements.txt
├── environment.yml       # conda env create -f environment.yml
├── CLAUDE.md             # repo conventions & contribution rules
├── RUN_REPORT.md         # latest full run: status, results, runtimes
└── README.md
```

## Using the helpers

```python
import sys; sys.path.insert(0, "src")
import mecanano_ml as mm
df  = mm.load_map("alcu_2um")     # HSNM property map as a DataFrame
afm = mm.load_afm_grid()          # small grid: scalars + depth curves
curves = mm.load_curves(10)       # list of (depth_nm, load_mN)
```

## Citation & license

Code is released under the terms in [`LICENSE`](LICENSE). If you use the
notebooks, please credit *MecaNano — Machine Learning for Nanomechanics
Tutorials (E. Rossi)* and cite the dataset source in `data/README.md`.

**Contact:** Edoardo Rossi · Università degli Studi Roma Tre · edoardo.rossi@uniroma3.it
