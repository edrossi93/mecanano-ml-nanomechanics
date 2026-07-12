# Setup help

This page gets you from "nothing installed" to "a notebook is running". Pick the
route that suits you. **If you just want to click and go, use Colab** (no install).

---

## Option A — Google Colab (nothing to install)

1. Open the repository on GitHub.
2. Open `notebooks/00_start_here.ipynb` and click the **Open in Colab** badge (or
   the badge in the `README`).
3. Run the first cell (**Shift + Enter**). It automatically clones the repo so the
   data and helpers are available. Then run the rest top to bottom.

That's it — skip the rest of this page unless you want to run locally.

---

## Option B — Run locally

You need **Python 3.10, 3.11 or 3.12**. (3.13/3.14 are very new and some libraries
may not have ready-made installers yet — prefer 3.11 or 3.12 for a smooth ride.)

### 1. Get Python
- **Windows / macOS:** install from [python.org](https://www.python.org/downloads/)
  (tick *"Add Python to PATH"* on Windows), **or** install
  [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
- **Linux:** use your system Python 3.11/3.12 or Miniconda.

### 2. Get the code
```bash
git clone https://github.com/edrossi93/mecanano-ml-nanomechanics.git
cd mecanano-ml-nanomechanics
```
(No git? Download the repo as a ZIP from GitHub and unzip it.)

### 3. Install the libraries

**With pip (a virtual environment keeps things tidy):**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

**Or with conda:**
```bash
conda env create -f environment.yml
conda activate ml-nano
```

### 4. Open Jupyter
```bash
jupyter lab        # or:  jupyter notebook
```
Your browser opens. Navigate to `notebooks/` and open `00_start_here.ipynb`.

---

## How to run a cell (the only Jupyter skill you need)

- A notebook is a list of **cells**. Click a cell, press **Shift + Enter** to run it.
- Run cells **top to bottom, in order** — later cells use things earlier ones created.
- `[*]` next to a cell means it's still running; a number like `[3]` means it finished.
- If things get confused, use the menu **Kernel → Restart & Run All** to start clean.

---

## Fixing common install problems

**`torch` is huge / slow to install.**
You only need the **CPU** build. If a normal install is pulling gigabytes of GPU
libraries, install the CPU wheel explicitly:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**`hdbscan` fails to build on Windows** (needs a C compiler).
Easiest fix: install it with conda instead of pip:
```bash
conda install -c conda-forge hdbscan
```
Or install the *Microsoft C++ Build Tools*, then retry `pip install hdbscan`.

**`umap-learn` won't install** (it depends on `numba`).
`numba` often lags the newest Python by a few months. If you're on Python 3.13/3.14,
create the environment on **Python 3.11 or 3.12** instead.

**`ModuleNotFoundError: mecanano_ml`** when running a notebook.
You skipped the **set-up cell** at the top of the notebook. Run it first — it puts
the repo's `src/` folder on the path.

**A `pip install` fails with a very long path error on Windows.**
Move your clone to a short path (e.g. `C:\mecanano`) and reinstall, or enable
[Windows long paths](https://pip.pypa.io/warnings/enable-long-paths).

Still stuck? See **[[FAQ]]** or open an issue using the bug-report template.
