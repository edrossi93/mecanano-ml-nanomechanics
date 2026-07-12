# Machine Learning for Nanomechanics — MecaNano Tutorials

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edrossi93/mecanano-ml-nanomechanics/HEAD?labpath=notebooks%2F00_start_here.ipynb)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edrossi93/mecanano-ml-nanomechanics/blob/main/notebooks/00_start_here.ipynb)

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

No install needed to try it: click **Binder** (full repo) above. On **Colab**,
each notebook auto-clones the repo and you just add one `pip install -r
requirements.txt` cell at the top.

## The notebooks

Read them in order; each is self-contained.

| # | Notebook | What you learn |
|---|----------|----------------|
| 00 | `00_start_here` | the datasets and how to run everything |
| 01 | `01_features_and_pca` | curve → features, standardisation, **PCA** (scree, loadings), t-SNE/UMAP |
| 02 | `02_clustering_phases` | **k-means + silhouette**, **GMM** (uncertainty), **HDBSCAN** → phase map |
| 03 | `03_supervised_trees_rf_shap` | **decision tree → random forest → boosting**, **SMOTE**, **SHAP** |
| 04 | `04_curve_as_image_cnn` | **GAF** curve→image + a small **CNN**; shape vs scale |
| 05 | `05_autoencoder_latent_space` | **autoencoder**, the **latent space**, anomaly detection |
| 06 | `06_correlative_registration` | aligning two maps: **NCC**, transform recovery, agreement & confusion |
| 10 | `10_cnn_mnist` | the classic MNIST **CNN** warm-up (refreshed) |
| 11 | `11_popin_detection` | a transparent **pop-in** detector, validated on a known signal |
| 12 | `12_regression_curvefitting` | Kick's-law **curve fitting** + **Random-Forest regression** |
| 13 | `13_yolo_defect_detection` | object detection in micrographs with **YOLO** (optional) |

## Data

All datasets are **non-proprietary** (see [`data/README.md`](data/README.md)):
the CC BY 4.0 Al–Cu / duplex-steel HSNM maps (Besharatloo & Wheeler, 2021), raw
load–depth curves, a small AFM-collocated grid, and MNIST. The whole ML arc —
unsupervised → supervised → multimodal — is taught on these.

## Repository layout

```
mecanano-ml-nanomechanics/
├── notebooks/            # 00–13, the tutorials
├── src/mecanano_ml/      # shared loaders, features and plotting helpers
├── data/                 # non-proprietary datasets (+ provenance)
├── requirements.txt      # pip install -r requirements.txt
├── environment.yml       # conda env create -f environment.yml
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
