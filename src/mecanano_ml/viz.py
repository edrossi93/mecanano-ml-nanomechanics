"""Consistent, clean plotting for the tutorials (black boxes, big fonts)."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def set_style():
    plt.rcParams.update({
        "figure.dpi": 110, "font.size": 12,
        "axes.linewidth": 1.2, "axes.edgecolor": "black",
        "axes.spines.top": True, "axes.spines.right": True,
        "xtick.direction": "in", "ytick.direction": "in",
        "image.cmap": "cividis",
    })

def plot_map(grid2d, extent=None, ax=None, cmap="cividis", label="",
             title="", vmin=None, vmax=None):
    """Show a 2-D property/label map with a full-height colour bar."""
    if ax is None: _, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(grid2d, origin="lower", extent=extent, cmap=cmap,
                   vmin=vmin, vmax=vmax, aspect="equal")
    if title: ax.set_title(title)
    ax.set_xlabel("x (µm)"); ax.set_ylabel("y (µm)")
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    if label: cb.set_label(label)
    return ax, im

def scatter_xy(x, y, c, ax=None, cmap="tab10", s=8, label="", discrete=True):
    """Scatter indents at their (x, y) positions coloured by cluster/value."""
    if ax is None: _, ax = plt.subplots(figsize=(5, 4))
    sc = ax.scatter(x, y, c=c, cmap=cmap, s=s, linewidths=0)
    ax.set_aspect("equal"); ax.set_xlabel("x (µm)"); ax.set_ylabel("y (µm)")
    cb = ax.figure.colorbar(sc, ax=ax, fraction=0.046, pad=0.03)
    if label: cb.set_label(label)
    return ax, sc
