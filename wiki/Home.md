# MecaNano · Machine Learning for Nanomechanics

Welcome! This is the companion wiki to the **hands-on tutorial repository** for
*Tutorial 1 — Machine learning bases and advanced applications for nanoindentation
data analysis* (MecaNano WG4).

The idea is simple: **read a method in the slides, then run it here on real
nanoindentation data.** Every notebook is short, runs on an ordinary laptop (no GPU,
no big downloads), and is written for someone who has **never done machine learning**
and has **little Python experience**.

> 🐍 Brand new to Python or Jupyter? Start with **[[Setup help]]**, then open
> `notebooks/00_start_here.ipynb`. You only need to know how to run a cell
> (**Shift + Enter**).

## How to run the notebooks

Pick whichever is easiest for you:

| Way | What to do | Best for |
|-----|-----------|----------|
| **Google Colab** | open a notebook via the Colab badge in the `README` — it clones the repo for you | zero install, just a browser |
| **Binder** | click the Binder badge in the `README` | zero install, but slower to start |
| **Local (pip)** | `pip install -r requirements.txt` then `jupyter lab` | working offline / your own data |
| **Local (conda)** | `conda env create -f environment.yml` then `conda activate ml-nano` | if you prefer conda |

Full step-by-step help (installing Python, opening Jupyter, fixing install errors)
is on the **[[Setup help]]** page.

## The learning path

Open the notebooks roughly in this order — each builds on the last.

| # | Notebook | What you'll meet |
|---|----------|------------------|
| 00 | `start_here` | the datasets and how to run everything |
| 01 | `features_and_pca` | features, standardisation, **PCA**, t‑SNE/UMAP |
| 01a | `linear_and_logistic_regression` | the gentlest models: fit a line, predict a class |
| 02 | `clustering_phases` | **k‑means, silhouette, GMM, HDBSCAN** → a phase map |
| 02a | `knn_classifier` | classify by **nearest neighbours** |
| 03 | `supervised_trees_rf_shap` | **decision tree → random forest → boosting**, SMOTE, **SHAP** |
| 03a | `evaluating_models` | cross‑validation, **precision/recall, ROC** — trust a model |
| 04 | `curve_as_image_cnn` | **GASF** (curve→image) + a small **CNN** |
| 04a | `1d_cnn_on_curves` | a **1‑D CNN** on the raw curve (keeps magnitude) |
| 05 | `autoencoder_latent_space` | **autoencoder** and its **latent space** |
| 06 | `correlative_registration` | aligning two maps, agreement & confusion |
| 10–13 | refreshed classics | MNIST CNN · pop‑in detection · curve fitting · YOLO (optional) |

## Wiki pages

- **[[Setup help]]** — install Python/conda, open Jupyter, fix common errors.
- **[[ML glossary]]** — every term in one plain sentence, with a nanoindentation example.
- **[[Datasets]]** — what data ships with the repo and how it's licensed.
- **[[FAQ]]** — kernel restarts, shape errors, the Colab clone note, and more.
- **[[From notebook to your own data]]** — plug your own maps/curves into the helpers.
- **[[Going further]]** — the optional/advanced notebooks and references.

## Ground rules (for contributors)

- **Only public data.** No proprietary / collaborator data; never any private file paths.
- **Beginner-first**, always: define terms, say what the reader should see, add a recap.
- Everything must **run on CPU** in a couple of minutes per notebook.

Data licence: the high-speed maps are **CC BY 4.0** — please cite *Besharatloo &
Wheeler, J. Mater. Res. 36, 2198–2212 (2021)*. See **[[Datasets]]** for details.
