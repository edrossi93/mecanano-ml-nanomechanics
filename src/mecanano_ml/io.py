"""Data loading for the tutorial datasets (all non-proprietary)."""
from __future__ import annotations
import glob, os
import numpy as np
import pandas as pd

# repo-root/data , resolved relative to this file so notebooks work from anywhere
DATA = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

# High-speed nanoindentation property maps (CC BY 4.0, Besharatloo & Wheeler,
# J. Mater. Res. 36, 2198-2212, 2021).  Two-row header: names then units.
_MAPS = {
    "alcu_1um":  "nanoindent_maps/Al-Cu Eutectic 1um.csv",
    "alcu_2um":  "nanoindent_maps/Al-Cu Eutectic 2um.csv",
    "alcu_3um":  "nanoindent_maps/Al-Cu Eutectic 3um.csv",
    "alcu_5um":  "nanoindent_maps/Al-Cu Eutectic 5um.csv",
    "duplex_1um":"nanoindent_maps/Duplex Steel 1um.csv",
    "duplex_2um":"nanoindent_maps/Duplex Steel 2um.csv",
    "duplex_5um":"nanoindent_maps/Duplex Steel 5um.csv",
    "titanium":  "nanoindent_maps/Titanium_dataset.csv",
}

def list_maps() -> list[str]:
    """Names accepted by :func:`load_map`."""
    return sorted(_MAPS)

def load_map(name: str = "alcu_2um") -> pd.DataFrame:
    """Load an HSNM property map as a tidy DataFrame.

    Columns include H (GPa), E (GPa), HE (=H/E), X, Y (um).  One row per
    indent.  Non-finite / non-positive H or E rows are dropped.
    """
    if name not in _MAPS:
        raise KeyError(f"unknown map {name!r}; try {list_maps()}")
    path = os.path.join(DATA, _MAPS[name])
    df = pd.read_csv(path, skiprows=[1])                 # drop the units row
    df = df.rename(columns={"HARDNESS": "H", "MODULUS": "E",
                            "X Position": "X", "Y Position": "Y"})
    if "H/E" in df: df = df.rename(columns={"H/E": "HE"})
    if "HE" not in df: df["HE"] = df["H"] / df["E"]
    df = df[np.isfinite(df["H"]) & np.isfinite(df["E"]) &
            (df["H"] > 0) & (df["E"] > 0)].reset_index(drop=True)
    return df

def map_to_grid(df: pd.DataFrame, value: str = "H"):
    """Reshape a regular-grid map column into a 2-D array (ny, nx).

    Returns (grid2d, extent) with extent = [xmin, xmax, ymin, ymax] for
    ``imshow(origin='lower', extent=extent)``.
    """
    xs = np.sort(df["X"].unique()); ys = np.sort(df["Y"].unique())
    nx, ny = len(xs), len(ys)
    xi = np.searchsorted(xs, df["X"].values)
    yi = np.searchsorted(ys, df["Y"].values)
    g = np.full((ny, nx), np.nan, float)
    g[yi, xi] = df[value].values
    extent = [xs.min(), xs.max(), ys.min(), ys.max()]
    return g, extent

def load_afm_grid() -> dict:
    """Small AFM-collocated nanoindentation grid (patterned standard).

    Returns a dict of numpy arrays: scalars X, Y, H, E, HE, S2P,
    phase_angle and depth-resolved H_curve, E_curve, load_mN on the
    common depth axis ``depth_nm`` (64 points).  ~800 indents — fast.
    """
    z = np.load(os.path.join(DATA, "afm_grid.npz"))
    return {k: z[k] for k in z.files}

def load_4d(name: str = "crn_cr_bilayer") -> dict:
    """Depth-resolved (4D) coating/bilayer map, e.g. CrN on Cr.

    Reads ``data/nanoindent_4d/<name>.csv`` (a plain, openable long-format table
    with columns ``indent, x_um, y_um, depth_nm, H_GPa, E_GPa``) and returns a
    dict of numpy arrays:
      ``X, Y``      per-indent position (um)
      ``depth_nm``  the common depth axis (nm)
      ``H, E``      arrays of shape (n_indents, n_depth): hardness / modulus vs
                    depth (GPa). Missing depth points are left as NaN.
    """
    path = os.path.join(DATA, "nanoindent_4d", name + ".csv")
    df = pd.read_csv(path)
    depth = np.sort(df["depth_nm"].unique())
    H = df.pivot_table("H_GPa", "indent", "depth_nm").reindex(columns=depth)
    E = df.pivot_table("E_GPa", "indent", "depth_nm").reindex(columns=depth)
    xy = df.groupby("indent")[["x_um", "y_um"]].first()
    return dict(depth_nm=depth, H=H.values, E=E.values,
                X=xy["x_um"].values, Y=xy["y_um"].values)

def load_curves(n: int | None = None, kind: str = "training"):
    """Load raw load-depth curves as a list of (depth_nm, load_mN) arrays.

    ``kind='training'`` reads data/nanoindentation_curves/training_curves.
    """
    folder = os.path.join(DATA, "nanoindentation_curves",
                          "training_curves" if kind == "training" else kind)
    files = sorted(glob.glob(os.path.join(folder, "*.CSV")) +
                   glob.glob(os.path.join(folder, "*.csv")))
    if n: files = files[:n]
    out = []
    for f in files:
        d = pd.read_csv(f)
        cols = {c.lower(): c for c in d.columns}
        def _pick(prefs, default):
            for p in prefs:
                for k in cols:
                    if p in k: return cols[k]
            return default
        dc = _pick(["depth", "disp"], d.columns[0])   # surface-referenced depth first
        lc = _pick(["load", "force"], d.columns[1])
        depth = pd.to_numeric(d[dc], errors="coerce").values
        load = pd.to_numeric(d[lc], errors="coerce").values
        m = np.isfinite(depth) & np.isfinite(load)
        out.append((depth[m], load[m]))
    return out
