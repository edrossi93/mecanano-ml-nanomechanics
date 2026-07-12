# FAQ & troubleshooting

Quick answers to the things beginners hit most. Also see **[[Setup help]]** for
installation problems.

### The notebook says `ModuleNotFoundError: No module named 'mecanano_ml'`
You skipped the **set-up cell** at the very top. Click it and press **Shift + Enter**
first — it puts the repo's `src/` folder on the path. Then re-run from the top.

### I edited a cell and now I get a weird shape or "variable not defined" error
Cells share state, so editing one can leave things half-updated. Use
**Kernel → Restart & Run All** to run everything cleanly from scratch. This fixes the
large majority of "it worked a minute ago" problems.

### A plot didn't appear / the cell shows `[*]`
`[*]` means the cell is still running — wait for it to finish (it becomes a number
like `[4]`). If nothing shows after it finishes, make sure you actually ran the plot
cell and the set-up cell before it.

### My numbers are slightly different from the "you should see" note
Expected. Neural networks, t-SNE and UMAP have some randomness, so accuracies and
layouts wobble a little run-to-run. The **conclusion** (e.g. "the feature route wins
here", "recall improves with SMOTE") is what's stable — not the third decimal.

### On Colab, the first cell downloaded the repo — is that normal?
Yes. On a fresh Colab session there's no local copy, so the set-up cell clones the
repo automatically. On your own machine it just finds the local `src/` and skips the
clone.

### `torch` took forever / downloaded gigabytes
You pulled the GPU build. Install the CPU one instead:
`pip install torch --index-url https://download.pytorch.org/whl/cpu`.

### `hdbscan` or `umap-learn` won't install
`hdbscan` needs a C compiler and `umap-learn` needs `numba`. Easiest fix: use conda
(`conda install -c conda-forge hdbscan umap-learn`), or make sure you're on **Python
3.11 or 3.12** (very new Pythons often lack these wheels). Details in **[[Setup help]]**.

### The MNIST notebook (10) prints accuracy ≈ 0.10
That means predictions got misaligned with labels — almost always because the **test**
loader was shuffled or read twice. Keep `shuffle=False` for the test set and gather
predictions and labels in a single pass (the notebook already does this).

### How long should a notebook take?
Under ~30 seconds each on a normal laptop CPU; most are far quicker. If one hangs,
restart the kernel and re-run. Notebook 13 (YOLO) is optional and heavier.

### Can I use my own data?
Yes — see **[[From notebook to your own data]]**.

### I found a bug / have a question
Open an issue using the **bug report** or **question** template. Include which
notebook, the error's last lines, and how you're running it (local / Colab / Binder).
