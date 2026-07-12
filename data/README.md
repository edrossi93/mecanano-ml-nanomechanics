# Datasets

All data here is **openly licensed** and safe to redistribute, and ships as open,
human-readable **CSV** (plus `evaluation_data.xlsx` and the MNIST ubyte files).

The maps come in two forms: **single-depth** (one hardness/modulus value per point)
and **depth-resolved** (the full hardness/modulus-vs-depth response at every point).

**Licensing at a glance** (see each section):
- The **author's own** measurements (curves, AFM grid, the CrN-on-Cr bilayer and
  the Al–Cu high-speed nanoindentation maps) are released **CC BY 4.0** — free to
  use *with citation*.
- The **third-party** Al–Cu / duplex HSNM maps are **CC BY 4.0** (Besharatloo &
  Wheeler, 2021) — keep their attribution.
- The **synthetic** data is pure simulation (CC0 — no rights reserved).
- MNIST keeps its standard terms.

## `nanoindent_maps/` — high-speed nanoindentation maps (single depth)
Al–Cu eutectic and duplex-steel maps plus a titanium map, each with **one hardness,
modulus and H/E per indent** (a single-depth map). Regular grids, tens of thousands of
indents. Load with `mecanano_ml.load_map(name)`.

**License / attribution — CC BY 4.0.** Please cite:
> H. Besharatloo & J. M. Wheeler, *Influence of indentation size and spacing on
> statistical phase analysis via high-speed nanoindentation mapping of metal
> alloys*, **J. Mater. Res. 36**, 2198–2212 (2021).
> https://doi.org/10.1557/s43578-021-00214-5

## `nanoindentation_curves/` — raw load–depth curves
Individual indentation curves (`DEPTH`, `LOAD`, stiffness, …) used for the
deep-learning and pop-in notebooks, plus an `evaluation_data.xlsx` summary.
Author's own measurements, shared for teaching.

## `hsnm_maps/` — high-speed nanoindentation maps (depth-resolved)
High-speed nanoindentation maps that keep the **full hardness/modulus/load-vs-depth**
response at every point, as long-format CSVs (`indent, x_um, y_um, depth_nm, H_GPa,
E_GPa, load_mN`). Author's own measurements (**CC BY 4.0**).
- `afm_grid_g.csv` — a small **AFM-collocated grid** on a reference standard
  (~800 indents; the fast demo used by several notebooks).
- `crn_cr_bilayer.csv` — a **CrN-on-Cr coating** map with a milled pattern (~1500 indents).
- `alcu_eutectic.csv` — an **Al–Cu eutectic** map (~900 indents).

Load any of them with `mecanano_ml.load_hsnm_map("crn_cr_bilayer")` (returns the
depth axis and per-indent H/E/load curves). The AFM grid also has a convenience
loader, `mecanano_ml.load_afm_grid()`, using the field names the notebooks expect.

## `synthetic/` — simulated data for method validation
`bilayer_synthetic.csv` — film-on-substrate hardness/modulus curves generated from a
Korsunsky-type model with **known** film/substrate values (shipped as
`Hf_true_GPa`, `Hs_true_GPa`), so deconvolution methods can be checked against ground
truth. Pure simulation (CC0).

## `MNIST/`
Standard MNIST digits (Y. LeCun et al.), used only for the classic CNN warm-up
(notebook 10).
