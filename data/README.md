# Datasets

All data here is **non-proprietary** and safe to redistribute, and ships as open,
human-readable **CSV** (plus a couple of `.npz`/`.xlsx`/ubyte files for the depth
curves and MNIST). No meteorite / collaborator EBSD / unpublished data is included.

**Licensing at a glance** (see each section):
- The **author's own** measurements (curves, AFM grid, the CrN-on-Cr bilayer, the
  AlCu 4D map) are released **CC BY 4.0** — free to use *with citation*.
- The **third-party** Al–Cu / duplex HSNM maps are **CC BY 4.0** (Besharatloo &
  Wheeler, 2021) — keep their attribution.
- The **synthetic** data is pure simulation (CC0 — no rights reserved).
- MNIST keeps its standard terms.

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
`load_mN`) on a common `depth_nm` axis. Author's own measurement (**CC BY 4.0**).
Load it with `mecanano_ml.load_afm_grid()`. An openable scalar-only CSV mirror is
provided as `afm_grid_scalars.csv`.

## `nanoindent_4d/` — depth-resolved (4D) coating & map data
Long-format CSVs (`indent, x_um, y_um, depth_nm, H_GPa, E_GPa`) with the full
hardness/modulus-vs-depth for each indent — the input for the coating/substrate
deconvolution (notebook 07). Author's own measurements (**CC BY 4.0**).
- `crn_cr_bilayer.csv` — a **CrN-on-Cr bilayer** high-speed map (~486 indents).
- `alcu_eutectic_4d.csv` — a depth-resolved **Al–Cu eutectic** map (~120 indents).
Load either with `mecanano_ml.load_4d("crn_cr_bilayer")`.

## `synthetic/` — simulated data for method validation
`bilayer_synthetic.csv` — film-on-substrate hardness/modulus curves generated from a
Korsunsky-type model with **known** film/substrate values (shipped as
`Hf_true_GPa`, `Hs_true_GPa`), so deconvolution methods can be checked against ground
truth. Pure simulation (CC0).

## `MNIST/`
Standard MNIST digits (Y. LeCun et al.), used only for the classic CNN warm-up
(notebook 10).
