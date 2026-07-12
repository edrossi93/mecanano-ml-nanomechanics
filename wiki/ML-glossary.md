# ML glossary for materials scientists

Every term you'll meet in the notebooks, in **one plain sentence**, each with a
**nanoindentation example**. Skim it once, then come back when a word puzzles you.

## The basics

- **Feature** — one measured number describing a sample. *Example: an indent's hardness `H`.*
- **Feature vector** — the list of a sample's features stacked together. *Example: `[H, E, H/E]` for one indent.*
- **Label** — the answer you want to predict. *Example: which phase an indent belongs to (matrix or intermetallic).*
- **Model** — a recipe that turns features into a prediction. *Example: a rule that predicts phase from `H` and `E`.*
- **Training** — adjusting a model so its predictions fit example data. *Example: fitting a tree on labelled indents.*
- **Supervised vs unsupervised** — supervised learns from labelled examples; unsupervised finds structure with **no** labels. *Example: clustering (unsupervised) vs classifying named phases (supervised).*

## Preparing data

- **Standardisation (z-score)** — rescale a feature to mean 0, spread 1 so units don't bias the result. *Example: putting `H` (GPa) and `H/E` (unitless) on equal footing.*
- **PCA (Principal Component Analysis)** — rotate the data onto new axes ordered by how much they vary, to compress many correlated numbers into a few. *Example: turning a 56-point hardness–depth curve into 3 numbers.*
- **Variance** — how spread out values are; PCA seeks the directions of greatest variance. *Example: the direction along which indents differ most.*
- **Principal component / loading** — a new PCA axis, and the recipe (per-feature weights) that defines it. *Example: PC1 ≈ overall hardness level.*
- **Scree plot** — the % of variance each component explains, in order; its "elbow" tells you how many to keep. *Example: first 3 curve-PCs explain most of the variance.*
- **Embedding (t-SNE / UMAP)** — a 2-D layout that puts similar samples near each other, for *looking* (not measuring). *Example: curves of similar hardness clustering on screen.*

## Finding groups (unsupervised)

- **Cluster** — a group of samples more alike than the rest. *Example: the soft-matrix indents.*
- **k-means** — split data into `k` groups around `k` moving centres. *Example: 2 clusters = 2 phases on the Al–Cu map.*
- **Silhouette** — a score (−1…1) for how well points sit in their cluster; used to choose `k`. *Example: silhouette peaks at k = 2.*
- **GMM (Gaussian Mixture Model)** — clustering that also gives each point a *probability* of each group. *Example: low confidence at phase boundaries.*
- **HDBSCAN** — density-based clustering that needs no `k` and can label sparse points as **noise (−1)**. *Example: flagging ambiguous indents instead of forcing them into a phase.*
- **ARI (Adjusted Rand Index)** — how much two groupings agree (1 = identical, 0 = chance). *Example: k-means vs GMM agree strongly → the phase split is robust.*

## Predicting (supervised)

- **Classifier** — a model that predicts a category. *Example: matrix vs intermetallic.*
- **Regression / regressor** — predicting a **number** instead of a category. *Example: predict hardness from curve features.*
- **Linear regression** — fit the best straight line/plane to predict a number. *Example: predict `E` from `H`.*
- **Logistic regression** — a linear **classifier** that outputs a probability. *Example: P(hard phase) from `H, E`.*
- **Decision boundary** — the line/surface where a classifier switches its prediction. *Example: the straight split logistic regression draws between phases.*
- **Decision tree** — a flowchart of yes/no threshold questions ending in a prediction. *Example: "is H > 3 GPa? → intermetallic".*
- **Random forest / gradient boosting** — many trees combined (voted / sequential) for accuracy and robustness. *Example: 200 trees voting on each indent's phase.*
- **k-NN (k-nearest-neighbours)** — classify a point by the majority vote of its `k` closest examples. *Example: an indent is 'hard' if most nearby indents are.*
- **Feature importance** — how much a feature was used by the model. *Example: `H` and `Depth` drive the phase call.*
- **Permutation importance** — importance measured by shuffling a feature and seeing the accuracy drop. *Example: confirming `E` really matters on unseen data.*
- **SHAP** — per-prediction credit: how much each feature pushed *this* decision. *Example: why *this* indent was called intermetallic.*
- **Class imbalance / SMOTE** — when one label is rare; SMOTE invents synthetic rare examples to rebalance. *Example: a 4%-abundance phase the model would otherwise ignore.*

## Judging a model

- **Train/test split** — fit on one part, score on a held-out part it never saw. *Example: train on 70% of indents, test on 30%.*
- **Overfitting / underfitting** — memorising noise (great on train, poor on test) / being too simple to capture the pattern. *Example: k-NN with k = 1 overfits.*
- **Cross-validation** — split several ways and average, for a score you can trust (with a spread). *Example: 5-fold accuracy = 0.85 ± 0.01.*
- **Learning curve** — score vs training-set size; shows whether more data would help. *Example: curves flatten → more indents wouldn't help much.*
- **Accuracy** — fraction of predictions that are correct. *Beware: misleading when a class is rare.*
- **Precision / recall / F1** — of predicted-hard, how many are hard / of truly-hard, how many caught / their balance. *Example: recall of a rare phase is the number that matters.*
- **Confusion matrix** — a table of predicted vs true labels; off-diagonal = mistakes. *Example: how many intermetallic indents were missed.*
- **ROC curve / AUC** — performance across all thresholds; AUC = 1 perfect, 0.5 random. *Example: comparing classifiers on a noisy phase task.*
- **Precision–recall curve / AP** — like ROC but better when a class is rare. *Example: the honest view for a 25%-abundance phase.*

## Uncertainty & calibration

- **Predictive uncertainty** — a model's own estimate of how unsure a prediction is, given as a spread σ or an interval. *Example: predicted hardness 6.2 ± 0.3 GPa, not just 6.2.*
- **Prediction interval / coverage** — the band meant to hold the truth a stated fraction of the time; coverage is the fraction it really does. *Example: a ±2σ "95%" band that captures 95% of held-out indents.*
- **Calibration** — whether the stated confidence matches reality; a calibrated 95% band is right 95% of the time. *Example: an over-confident model whose "95%" band only covers 60%.*
- **Deep ensemble** — several models trained from different seeds; their disagreement is the uncertainty. *Example: five nets predicting H, their spread flags hard indents.*
- **MC-dropout** — leave dropout on at inference and run many passes; the spread of outputs is a neural uncertainty. *Example: 50 stochastic passes over one curve give a σ.*
- **Tree variance (bootstrap)** — the disagreement among a random forest's trees, a free uncertainty with no extra models. *Example: high tree σ where the phases overlap.*

## Deep learning

- **Tensor** — a multi-dimensional array a neural network computes with (PyTorch's array). *Example: a batch of curve-images.*
- **CNN (convolutional neural network)** — slides small learnable filters over an image (or sequence) to detect patterns, then classifies. *Example: reading a curve-as-image.*
- **1-D convolution** — a filter sliding along a sequence (the sequence version of image convolution). *Example: reading a load–depth curve directly.*
- **Epoch** — one full pass of the training data through the network. *Example: 25 quick passes on the CPU.*
- **GAF (Gramian Angular Field)** — turns a 1-D curve into a square image; it's **scale-invariant** (keeps shape, drops magnitude). *Example: two phases that differ in level look identical after GAF.*
- **Autoencoder** — a network that squeezes data through a narrow **bottleneck** and rebuilds it, learning a compact code. *Example: 56-point curve → 2 numbers → 56-point curve.*
- **Latent space** — the bottleneck's few numbers: learned coordinates where similar samples sit together. *Example: curves ordered by hardness with no labels given.*
- **Reconstruction error → anomaly** — how badly the autoencoder rebuilds a sample; high = unusual. *Example: flagging pop-ins and cracked indents.*

## Imaging & correlation

- **NCC (normalised cross-correlation)** — one number (−1…1) for how well two images overlap. *Example: scoring the alignment of a hardness and a modulus map.*
- **Registration** — finding the transform that lines up two maps. *Example: aligning mechanics to microstructure.*
- **Phase cross-correlation** — an FFT trick that finds the shift between two images fast. *Example: recovering a (12, −8)-pixel offset.*
- **Dice score** — overlap of a labelled region between two maps (1 = perfect). *Example: do both maps mark the same pixels 'hard'?*
- **Object detection / YOLO** — locating *and* labelling every object with a box + confidence. *Example: boxing defects in a micrograph.*
- **Segmentation** — labelling every pixel of an image with a class, producing a map the same size as the image. *Example: marking each pixel of a micrograph as matrix or precipitate.*
- **IoU (intersection over union)** — overlap of two regions divided by their union; 1 is perfect. *Example: scoring a predicted phase mask against the truth.*
- **U-Net** — an encoder–decoder CNN with skip connections that outputs a full-size label map. *Example: segmenting grains from a micrograph.*
- **Phase fraction** — the share of area belonging to a phase, read straight off a segmentation. *Example: 42% of a two-phase micrograph is the hard phase.*
- **Label transfer** — copying labels from one aligned modality onto another's measurement points. *Example: putting a second technique's phase labels onto the indents beneath them.*
- **Gap-filling (predict everywhere)** — train on the labelled points, then predict the unmeasured ones to complete a map. *Example: a forest filling regions a second technique could not index.*

## Optimisation & discovery

- **Surrogate model** — a cheap stand-in for an expensive property, fit to the data so far and queried instead of experimenting. *Example: a Gaussian process predicting hardness vs a processing setting.*
- **Acquisition function** — a score over settings saying how useful each next experiment would be. *Example: UCB = mean + κ·σ, high where the model is promising or unsure.*
- **Bayesian optimization** — surrogate + acquisition in a loop, to find an optimum in few experiments. *Example: locating the anneal that maximises hardness in ~8 tries.*
- **Exploration vs exploitation** — trying uncertain settings that might hide the optimum versus refining the best-known one. *Example: κ in UCB tunes the balance.*

---

Missing a term? Open a question issue and we'll add it.
