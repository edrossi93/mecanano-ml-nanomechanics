# Run report

**What this is.** A record of executing every notebook head-to-tail in a clean CPU
environment, with the key result each one produces and what a learner should observe.

**Environment.** Python 3.12 on CPU, the `requirements.txt` stack (NumPy 2.x,
pandas 2/3, scikit-learn 1.x, PyTorch 2.x CPU build, umap-learn, hdbscan, shap, pyts,
scikit-image). Each notebook was run top-to-bottom with `nbclient` (the same thing the
CI does on Python 3.11 via `pytest --nbmake`). Seeds are set, but neural nets, t-SNE
and UMAP wobble slightly run-to-run — treat every number below as "about this".

## Summary table

| Notebook | Status | Key result | Approx. runtime |
|---|---|---|---|
| 00_start_here | ✅ pass | loads 40,000-indent Al–Cu single-depth map + ~6,600-indent AFM grid (etched 5 µm cubes) + curves | ~4 s |
| 01_features_and_pca | ✅ pass | PCA explains 88%/12% on 3 features; whole-curve PCA + t-SNE/UMAP render | ~20 s |
| 01a_linear_and_logistic_regression | ✅ pass | linear E–H R² = 0.71; logistic classifier acc ≈ 1.00 | ~4 s |
| 02_clustering_phases | ✅ pass | all 40k: silhouette peak **k = 2** (0.61); HDBSCAN 2 clusters/~3% noise; ARI(k-means, GMM) = 0.86 | ~9 s |
| 02a_knn_classifier | ✅ pass | all 40k (28k train): boundaries jagged→smooth; every k ≈ 0.999, k=1 train = 1.0 is the overfit signal | ~4 s |
| 03_supervised_trees_rf_shap | ✅ pass | tree 0.98, RF/boosting 1.00; SMOTE recall 0.98→0.99; SHAP + permutation | ~13 s |
| 03a_evaluating_models | ✅ pass | CV acc 0.851 ± 0.010; rare-phase **recall 0.61 vs 0.84 acc**; ROC/PR | ~5 s |
| 04_curve_as_image_cnn | ✅ pass | CNN(GAF) **0.72** vs PCA+RF **0.90** (by design — GAF drops scale) | ~13 s |
| 04a_1d_cnn_on_curves | ✅ pass | 1-D CNN on raw curve **0.90** (beats the GAF CNN — keeps scale) | ~7 s |
| 05_autoencoder_latent_space | ✅ pass | reconstruction MSE 0.057; 25 anomalies flagged | ~8 s |
| 06_correlative_registration | ✅ pass | NCC 0.18→0.71; angle 6.0° recovered (true 6.0); agreement 79.7%, Dice 0.80 | ~3 s |
| 07_substrate_layer_deconvolution | ✅ pass | milled logo clustered from real CrN/Cr/Si; synthetic multilayer recovered (CrN 22.1/Cr 5.0/Si 12.0); ML R²=0.98 | ~6 s |
| 08_single_vs_depth_resolved | ✅ pass | Al–Cu two-phase map: single-depth (2.8/8.2 GPa) vs whole-curve (57% hard); **ARI 0.86** | ~9 s |
| 10_cnn_mnist | ✅ pass | MNIST test accuracy **0.92** | ~8 s |
| 11_popin_detection | ✅ pass | synthetic pop-in detected at the injected load; real curves flagged | ~3 s |
| 12_regression_curvefitting | ✅ pass | Kick's law n ≈ 1.89; RF regression R² ≈ 0.80 | ~4 s |
| 13_yolo_defect_detection | ✅ pass | illustration mode (ultralytics optional) | ~3 s |

**17 / 17 notebooks pass on CPU.** Total wall-clock ≈ 2 minutes. Notebook 13 runs in
illustration mode (no `ultralytics`) and is excluded from CI as optional/heavy.

### Fixes applied during this pass
- **`np.trapz` removed in NumPy 2.x** broke `curve_scalar_features` (notebook 12). Now
  uses `np.trapezoid` with a fallback.
- **Notebook 10 (MNIST) read accuracy 0.10** — the test loader was shuffled and iterated
  twice, misaligning predictions and labels. Fixed to `shuffle=False` + a single aligned
  pass; accuracy is back to 0.92.
- **Notebook 03a** learning curve produced a `FitFailedWarning`/NaN because the imbalanced
  subset was class-ordered; the subset is now shuffled.
- **Notebook 13** used a hard-coded `/tmp` path (absent on Windows); now uses `tempfile`.

## What a learner should see, notebook by notebook

**00 · start_here (~3 s).** The Al–Cu map loads as 40,000 indents with columns including
`H, E, HE, X, Y`; the hardness/modulus maps show the same two-phase pattern and the
hardness histogram is clearly bimodal. The AFM grid loads as ~6,600 indents with depth-resolved
curves. Takeaway: the data is two-phase, and one helper (`mm`) loads everything.

**01 · features_and_pca (~20 s).** `H, E, H/E` are strongly correlated (0.66–0.95), so PCA
puts **88%** of the variance on PC1 and **12%** on PC2 — the PC1–PC2 scatter already splits
into two clouds. On the whole 56-point curve, the first three components capture most of
the variance, and t-SNE/UMAP lay the curves out grouped by hardness. Takeaway: standardise,
then a few components carry the structure.

**01a · linear_and_logistic_regression (~4 s).** Linear regression of `E` on `H` gives a
slope ≈ 7 and R² ≈ 0.71 (a real but imperfect relationship). Logistic regression separates
the two phases with a straight decision boundary at ≈ 1.00 training accuracy and produces a
smooth probability map. Takeaway: the two simplest models — a line, and a linear classifier.

**02 · clustering_phases (~9 s).** On all **40,000** indents the silhouette peaks at **k = 2**
(0.61) — the clustering itself uses every point; only the O(n²) silhouette score samples 10,000.
k-means paints two coherent regions, GMM adds a confidence map that darkens at boundaries,
HDBSCAN (also on all 40,000) finds **2 clusters** plus ~3% noise, and ARI(k-means, GMM) = 0.86
confirms the split is robust. Takeaway: "how many phases?" becomes a defensible number.

**02a · knn_classifier (~4 s).** Now on all **40,000** indents (28,000 train / 12,000 test).
Decision boundaries for k = 1, 15, 101 still go from jagged (overfit) to smooth (underfit). With
this much cleanly-separable data every k classifies at ≈ 0.999, so the test-accuracy curve is
nearly flat; the visible overfitting signal is that **k = 1 scores a perfect 1.0 on *training***
but slightly less on the test set. Takeaway: more data shrinks the overfit gap — read it from the
train-vs-test split, not the test ranking alone.

**03 · supervised_trees_rf_shap (~13 s).** A depth-3 tree reaches 0.98 and prints readable
rules (it splits on **Depth** and **E**, not only H); random forest and boosting reach ~1.00.
Under an enforced 4% minority, recall stays high (0.98→0.99 with SMOTE), and both feature
importance and **permutation importance** plus **SHAP** agree the decision leans on Depth/E.
Takeaway: interpretable → accurate models, and watch recall.

**03a · evaluating_models (~5 s).** With noise and imbalance added on purpose, a single split
reads 0.844 while 5-fold CV gives **0.851 ± 0.010**; the learning curve plateaus; and the
per-class report exposes the honest gap — overall accuracy 0.84 but rare-phase **recall 0.61**.
The ROC bows to the top-left and the PR curve sits well above chance. Takeaway: report
cross-validated scores and, under imbalance, precision/recall/PR — not accuracy alone.

**04 · curve_as_image_cnn (~13 s).** The GAF is verified scale-invariant (`|GAF(x) −
GAF(2x+3)| ≈ 1e-6`), so the CNN on GAF images scores **0.72** while a simple PCA+RF that keeps
magnitude scores **0.90**. Takeaway: match the representation to the class difference — here
the phases differ in *level*, which the GAF discards.

**04a · 1d_cnn_on_curves (~7 s).** The same task with a 1-D CNN on the raw (magnitude-keeping)
curve reaches **0.90**, clearly beating the GAF CNN's 0.72. Takeaway: the same lesson from the
other side — keep whatever separates your classes.

**05 · autoencoder_latent_space (~8 s).** A 64→16→2→16→64 autoencoder trains to reconstruction
MSE ≈ 0.057; the 2-D latent space is smoothly organised by hardness (no labels used), and the
top-3% reconstruction errors flag **25** unusual curves. Guardrail: this stays a *plain*
autoencoder. Takeaway: learned coordinates + a free anomaly detector.

**06 · correlative_registration (~3 s).** A known 6°/(12, −8) misalignment drops NCC from 0.84
to 0.18; the angle search + phase-correlation recovers **6.0°** and restores NCC to 0.71, giving
**79.7%** point-to-point agreement and **Dice 0.80**. Takeaway: the mechanics↔microstructure
registration method, on public H/E channels only.

**07 · substrate_layer_deconvolution (~6 s).** On a real **CrN(200 nm)/Cr(200 nm)/Si** stack with a
milled logo, the shallow (≤64 nm) indents sense only the top layer, so the coating-hardness map traces
the **milled pattern** and clustering segments intact-CrN (~17 GPa) from milled/thinned regions. A
synthetic multilayer (known thicknesses) is fitted to recover all three layer hardnesses (CrN 22.1,
Cr 5.0, Si 12.0 vs true 22/5/12), and a random forest learns the deconvolution (**R² = 0.98**).
Takeaway: match the depth range to the layer you want — cluster shallow maps, deconvolve deep curves.

**08 · single_vs_depth_resolved (~9 s).** The depth-resolved Al–Cu map (19,718 indents) is
clustered two ways into its soft matrix and hard Al₂Cu intermetallic: from **one depth** (50 nm →
2.8 vs 8.2 GPa) and from the **whole hardness curve** (PCA→k-means; 57% hard, 5 components keep
0.98 of the variance). The two phase maps agree at **ARI 0.86**; the single-depth answer matches the
whole-curve one **0.83 at a shallow 15 nm** but **0.93 at 80 nm**. Takeaway: a depth-resolved map is
a stack of single-depth maps — using the whole curve needs no chosen depth and is more robust.

**10 · cnn_mnist (~8 s).** A small CNN reaches **0.92** on MNIST in 2 epochs, with a near-diagonal
confusion matrix. Takeaway: the same convolutional idea as notebook 04 — and never shuffle the
test set while scoring.

**11 · popin_detection (~3 s).** The transparent dh/dP + MAD detector finds the injected pop-in in
the synthetic curve at the right load, then flags bursts in real curves. Takeaway: validate a
detector on a known signal before trusting it.

**12 · regression_curvefitting (~4 s).** Kick's law fits with **n ≈ 1.89** (near the theoretical 2),
and a random-forest regressor predicts hardness from curve features at **R² ≈ 0.80** (parity plot).
Takeaway: physics gives interpretable coefficients; ML captures the trend — judge it with R².

**13 · yolo_defect_detection (~3 s).** Runs in illustration mode (no `ultralytics`), drawing example
detection boxes and explaining how to train on your own micrographs. Takeaway: detection =
classification + localisation; optional and excluded from CI.

## Verdict
Everything runs top-to-bottom on CPU with no errors. The four issues found during this pass
(NumPy `trapz`, the MNIST shuffle bug, the 03a learning-curve warning, the notebook-13 `/tmp`
path) were fixed and re-verified. CI (`.github/workflows/ci.yml`) reproduces this run on every
push/PR.
