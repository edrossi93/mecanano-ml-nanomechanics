# Datasets

All data here is **non-proprietary** and safe to redistribute. No meteorite /
collaborator EBSD data is included.

## `nanoindent_maps/` — high-speed nanoindentation property maps
Al–Cu eutectic and duplex-steel maps (hardness, modulus, H/E per indent) plus a
titanium map. Regular grids, tens of thousands of indents.

**License / attribution — CC BY 4.0.** Please cite:
> H. Besharatloo & J. M. Wheeler, *Influence of indentation size and spacing on
> statistical phase analysis via high-speed nanoindentation mapping of metal
> alloys*, **J. Mater. Res. 36**, 2198–2212 (2021).
> https://doi.org/10.1557/s43578-021-00214-5

## `nanoindentation_curves/` — raw load–depth curves
Individual indentation curves (`DEPTH`, `LOAD`, stiffness, …) used for the
deep-learning and pop-in notebooks, plus an `evaluation_data.xlsx` summary.
Author's own measurements, shared for teaching.

## `afm_grid.npz` — small AFM-collocated grid (fast demo)
~800 indents from a patterned standard, with per-indent scalars (`H`, `E`, `HE`,
`S2P`, `phase_angle`) **and** the depth-resolved curves (`H_curve`, `E_curve`,
`load_mN`) on a common `depth_nm` axis. Author's own measurement.
Load it with `mecanano_ml.load_afm_grid()`.

## `MNIST/`
Standard MNIST digits (Y. LeCun et al.), used only for the classic CNN warm-up
(notebook 10).
