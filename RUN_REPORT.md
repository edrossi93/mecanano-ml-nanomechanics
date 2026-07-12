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
| 01a_linear_and_logistic_regression | ✅ pass | Kick's-law fit `P ∝ h²` R² = 0.999; logistic classifier acc ≈ 1.00 | ~13 s |
| 02_clustering_phases | ✅ pass | all 40k: silhouette peak **k = 2** (0.61); GMM BIC elbow at 2–3 (3rd = interface); HDBSCAN 2 clusters/~3% noise; ARI = 0.86 | ~30 s |
| 02a_knn_classifier | ✅ pass | all 40k (28k train): boundaries jagged→smooth; every k ≈ 0.999, k=1 train = 1.0 is the overfit signal | ~4 s |
| 03_supervised_trees_rf_shap | ✅ pass | tree 0.98, RF/boosting 1.00; SMOTE recall 0.98→0.99; SHAP + permutation | ~13 s |
| 03a_evaluating_models | ✅ pass | CV acc 0.851 ± 0.010; rare-phase **recall 0.61 vs 0.84 acc**; ROC/PR | ~5 s |
| 04_curve_as_image_cnn | ✅ pass | CNN(GAF) **0.72** vs PCA+RF **0.90** (by design — GAF drops scale) | ~13 s |
| 04a_1d_cnn_on_curves | ✅ pass | 1-D CNN on raw curve **0.90** (beats the GAF CNN — keeps scale) | ~7 s |
| 05_autoencoder_latent_space | ✅ pass | reconstruction MSE 0.057; 25 anomalies flagged | ~8 s |
| 06_correlative_registration | ✅ pass | NCC 0.18→0.71; angle 6.0° recovered (true 6.0); agreement 79.7%, Dice 0.80 | ~3 s |
| 07_substrate_layer_deconvolution | ✅ pass | milled logo clustered from real CrN/Cr/Si; synthetic multilayer recovered (CrN 22.1/Cr 5.0/Si 12.0); ML R²=0.98 | ~6 s |
| 08_single_vs_depth_resolved | ✅ pass | Al–Cu two-phase map: single-depth (2.8/8.2 GPa) vs whole-curve (57% hard); **ARI 0.86** | ~9 s |
| 09_multimodal_pipeline | ✅ pass | register (5.0° recovered), transfer 60% of labels, RF fills the rest: held-out acc 0.84, 95% agreement | ~10 s |
| 10_cnn_mnist | ✅ pass | MNIST test accuracy **0.92** | ~8 s |
| 11_popin_detection | ✅ pass | synthetic pop-in detected at the injected load; real curves flagged | ~3 s |
| 12_regression_curvefitting | ✅ pass | Kick's law n ≈ 1.89; RF regression R² ≈ 0.80 | ~4 s |
| 13_yolo_defect_detection | ✅ pass | illustration mode (ultralytics optional) | ~3 s |
| 14_uncertainty_quantification | ✅ pass | ensemble σ 0.095 GPa (±2σ coverage 0.86), RF-variance σ 0.49 (0.99), MC-dropout when torch present + calibration | ~6 s |
| 15_microstructure_segmentation | ✅ pass | synthetic two-phase micrographs: U-Net **Dice 0.98 / IoU 0.95** vs threshold 0.51; phase-fraction MAE 0.008 | ~20 s |
| 16_bayesian_optimization | ✅ pass | GP + UCB finds the hidden optimum (x = 0.72) in ~8 experiments, beating random search | ~8 s |

**21 / 21 notebooks pass on CPU.** Total wall-clock ≈ 2.5 minutes. Notebook 13 runs in
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

**01a · linear_and_logistic_regression (~13 s).** Linear regression fits **Kick's law** on a
load–depth curve: load against depth² is a near-perfect straight line (slope C ≈ 119 mN/µm²,
R² ≈ 0.999) — a genuinely linear physical law, the case where a straight line is the right
model. Logistic regression then separates the two Al–Cu phases with a straight decision
boundary at ≈ 1.00 training accuracy and produces a smooth probability map. Takeaway: the two
simplest models — a line where the physics is linear, and a linear classifier.

**02 · clustering_phases (~30 s).** On all **40,000** indents the silhouette peaks at **k = 2**
(0.61) — the clustering itself uses every point; only the O(n²) silhouette score samples 10,000.
A GMM **BIC** sweep gives a second opinion: gains are large through **k = 2–3** then flatten, and
the third component is an **interface / mixed** mode (H ≈ 3.8 GPa, between the soft ≈ 1.4 and hard
≈ 4.9) — so two is the robust answer, three a defensible finer view. k-means paints two coherent
regions, GMM adds a confidence map that darkens at boundaries, HDBSCAN (also on all 40,000) finds
**2 clusters** plus ~3% noise, and ARI(k-means, GMM) = 0.86 confirms the split is robust. Takeaway:
"how many phases?" becomes a defensible number — two here, with three a reasonable finer split.

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

**09 · multimodal_pipeline (~10 s).** The full correlative workflow end to end: it registers two maps
(recovering a 5.0° rotation), transfers phase labels where they overlap (about 60% of 40,000 indents),
trains a classifier on those, and fills the remaining gaps. Held-out accuracy on the transferred
labels is 0.84, and it agrees with the measured labels 95% of the time. Takeaway: chaining notebooks
06 and 03 turns two partial maps into one complete labelled map.

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

**14 · uncertainty_quantification (~6 s).** Hardness is predicted three ways, each with an honest
error bar: a deep ensemble (mean σ ≈ 0.10 GPa, ±2σ covering 0.86 of held-out points), random-forest
tree variance (σ ≈ 0.49 GPa, coverage 0.99), and MC-dropout where PyTorch is present, then a
calibration check of those coverages. Takeaway: a prediction without an uncertainty is half an answer,
and the uncertainty has to be calibrated rather than assumed.

**15 · microstructure_segmentation (~20 s).** On synthetic two-phase micrographs whose phases share a
brightness but differ in texture, a brightness threshold scores Dice ≈ 0.51 (chance) while a
~66k-parameter tiny U-Net reaches **Dice 0.98 / IoU 0.95**, and its masks recover the phase fraction
to a mean error of 0.008. Takeaway: when phases differ by texture rather than level you need a CNN,
and its mask becomes a quantitative microstructure measurement. The data is fully synthetic, so there
is nothing to download.

**16 · bayesian_optimization (~8 s).** A Gaussian-process surrogate plus a UCB acquisition function
locates the hidden global optimum (x = 0.72, avoiding a decoy peak at 0.25) within about 8
experiments, and its best-so-far curve stays above random search throughout. Takeaway: when
experiments are expensive, model the property with uncertainty and let the acquisition function choose
what to run next. This is the loop behind accelerated materials discovery.

## Verdict
Everything runs top-to-bottom on CPU with no errors. The four issues found during this pass
(NumPy `trapz`, the MNIST shuffle bug, the 03a learning-curve warning, the notebook-13 `/tmp`
path) were fixed and re-verified. CI (`.github/workflows/ci.yml`) reproduces this run on every
push/PR.
