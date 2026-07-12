"""Data loading for the tutorial datasets (all openly licensed)."""
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
    "duplex_3p5um":"nanoindent_maps/Duplex Steel 3p5um.csv",
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

def load_hsnm_map(name: str = "crn_cr_bilayer") -> dict:
    """High-speed nanoindentation map that keeps the full depth-resolved response
    at every point (e.g. a CrN-on-Cr coating, or the AFM-collocated grid).

    Reads ``data/hsnm_maps/<name>.csv`` (a plain, openable long-format table with
    columns ``indent, x_um, y_um, depth_nm, H_GPa, E_GPa`` and, when available,
    ``load_mN``) and returns a dict of numpy arrays:
      ``X, Y``      per-indent position (um)
      ``depth_nm``  the common depth axis (nm)
      ``H, E``      arrays of shape (n_indents, n_depth): hardness / modulus vs
                    depth (GPa). Missing depth points are left as NaN.
      ``load``      (n_indents, n_depth) load vs depth (mN), if present.
    """
    path = os.path.join(DATA, "hsnm_maps", name + ".csv")
    df = pd.read_csv(path)
    depth = np.sort(df["depth_nm"].unique())
    def _pivot(col):
        return df.pivot_table(col, "indent", "depth_nm").reindex(columns=depth).values
    xy = df.groupby("indent")[["x_um", "y_um"]].first()
    out = dict(depth_nm=depth, H=_pivot("H_GPa"), E=_pivot("E_GPa"),
               X=xy["x_um"].values, Y=xy["y_um"].values)
    if "load_mN" in df.columns:
        out["load"] = _pivot("load_mN")
    return out

def load_afm_grid() -> dict:
    """AFM-collocated high-speed nanoindentation grid (depth-resolved, fast demo).

    A convenience view of the ``afm_grid_g`` high-speed nanoindentation map using
    the field names the notebooks expect: per-indent scalars ``X, Y, H, E, HE``
    (taken at the deepest reliable depth) plus the depth-resolved curves
    ``H_curve, E_curve, load_mN`` on the common axis ``depth_nm``.
    """
    d = load_hsnm_map("afm_grid_g")
    H, E = d["H"], d["E"]

    def _deepest(a):                       # last finite value along each curve
        out = np.full(a.shape[0], np.nan, float)
        for i in range(a.shape[0]):
            fin = np.where(np.isfinite(a[i]))[0]
            if fin.size:
                out[i] = a[i, fin[-1]]
        return out

    Hs, Es = _deepest(H), _deepest(E)
    return dict(X=d["X"], Y=d["Y"], H=Hs, E=Es, HE=Hs / Es,
                depth_nm=d["depth_nm"], H_curve=H, E_curve=E, load_mN=d.get("load"))

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
