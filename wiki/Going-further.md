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
- **Correlate two modalities end to end.** Notebook **`09`** chains registration (`06`)
  and supervised learning (`03`): align a second technique, transfer its labels, then
  predict the regions it could not measure.
- **Report honest confidence.** Notebook **`14`** puts an error bar on every prediction
  (ensembles, tree variance, MC-dropout) and checks the bar is calibrated. Make it a habit.
- **Beyond nanoindentation.** Notebook **`15`** segments a microstructure with a U-Net
  (a CNN for microscopy), and **`16`** uses Bayesian optimization to pick the next
  experiment. Both run on synthetic data you can swap for your own.

## Natural next methods (not yet in the repo)

- **Active learning on real experiments.** Take the loop in **`16`** to a 2-D or 3-D
  setting and drive an actual measurement campaign, not a synthetic one.
- **UMAP parameter deep-dive.** How `n_neighbors` and `min_dist` trade off local vs
  global structure in an embedding.
- **Graph neural networks** for crystal structures or defect networks, where the input
  is a graph rather than a grid or a curve.
- **Physics-informed models** that fold a known equation (Kick's law, a diffusion PDE)
  into the loss so predictions stay physical.

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
