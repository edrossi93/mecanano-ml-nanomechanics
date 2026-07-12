"""Feature engineering helpers."""
from __future__ import annotations
import numpy as np

def standardize(X, return_scaler: bool = False):
    """z-score each column (mean 0, unit variance). Wraps sklearn."""
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    Xs = sc.fit_transform(np.asarray(X, float))
    return (Xs, sc) if return_scaler else Xs

def curve_scalar_features(depth_nm, load_mN) -> dict:
    """Compact, physically-motivated descriptors of one load-depth curve.

    Returns max load, max depth, loading stiffness (dP/dh near the top),
    elastic work / total work ratio and the mean loading curvature
    (Kick's-law C in P = C h^2).  These are the kind of scalars a model
    would use *instead* of the whole curve.
    """
    h = np.asarray(depth_nm, float); P = np.asarray(load_mN, float)
    m = np.isfinite(h) & np.isfinite(P)
    h, P = h[m], P[m]
    if h.size < 5:
        return dict(P_max=np.nan, h_max=np.nan, S=np.nan, We_Wt=np.nan, C=np.nan)
    imax = int(np.argmax(P))
    h_load, P_load = h[:imax + 1], P[:imax + 1]
    # unloading stiffness S = dP/dh over the top 10% of unloading
    if imax < len(h) - 3:
        hu, Pu = h[imax:], P[imax:]
        k = max(3, len(hu) // 10)
        S = np.polyfit(hu[:k], Pu[:k], 1)[0]
    else:
        S = np.polyfit(h_load[-max(3, len(h_load)//10):],
                       P_load[-max(3, len(P_load)//10):], 1)[0]
    Wt = np.trapz(P_load, h_load)
    Wtot = np.trapz(np.abs(P), h)
    We_Wt = float(np.clip((Wtot - Wt) / Wtot, 0, 1)) if Wtot > 0 else np.nan
    C = float(np.polyfit(h_load, P_load, 2)[0])
    return dict(P_max=float(P.max()), h_max=float(h.max()),
                S=float(abs(S)), We_Wt=We_Wt, C=C)
