# Going further

You've worked through the core notebooks — here's where to deepen each thread.

## Within this repo

- **Evaluate everything honestly.** Re-read **`03a_evaluating_models`** and apply
  cross-validation + precision/recall/ROC to *every* model you train, not just the
  examples. This is the single highest-value habit in applied ML.
- **Representation matters.** Compare **`04` (GAF/2-D CNN)** with **`04a` (1-D CNN on
  the raw curve)**: the same task, won or lost by whether the input keeps *shape* or
  *magnitude*. Try your own labels and see which representation wins.
- **Interpretability.** Push **`03`** further: contrast built-in, **permutation**, and
  **SHAP** importances. When do they disagree, and why?
- **Anomalies.** Combine the **autoencoder** score (`05`) with the transparent
  **pop-in** detector (`11`) to triage a large map before analysis.
- **Correlation.** Extend **`06`** from a rigid transform to an **affine** one
  (add scale/shear) if your two modalities differ in magnification.

## Natural next methods (not yet in the repo)

- **Uncertainty in regression** — Gaussian-process regression gives predictions *with
  error bars*, valuable when you'll make decisions from the numbers.
- **UMAP parameter deep-dive** — how `n_neighbors` and `min_dist` trade off local vs
  global structure in an embedding.
- **1-D CNN vs classic features, at scale** — when does deep learning actually beat a
  well-chosen feature set? (Often it doesn't, on small data — measure it.)
- **Semantic segmentation** of micrographs (U-Net) as the pixel-level cousin of the
  object detection in notebook 13.

## Background reading

- **Data source (please cite):** Besharatloo & Wheeler, *J. Mater. Res.* **36**,
  2198–2212 (2021), https://doi.org/10.1557/s43578-021-00214-5.
- **scikit-learn user guide** — the clearest free reference for everything in
  notebooks 01–03, 12: https://scikit-learn.org/stable/user_guide.html
- **PyTorch tutorials** — for the CNN/autoencoder notebooks:
  https://pytorch.org/tutorials/
- **The companion Tutorial 1 slides** (MecaNano WG4) — the methods in narrative form.

## A closing principle

Every method here is a way of answering one of two questions — *"what groups are in my
data?"* (unsupervised) or *"can I predict this property/label?"* (supervised) — and the
honest answer always comes with its evaluation. Match the method to the question, match
the representation to what separates your classes, and report what the validation
supports. That mindset outlasts any single algorithm.
