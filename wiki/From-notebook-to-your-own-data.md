# From the tutorial to your own data

Once a method makes sense on the shipped data, running it on **your** indents is
mostly a matter of getting your data into the same simple shapes. You have two easy
options.

## Option 1 — skip the loaders, build the arrays yourself
Every notebook only needs plain NumPy/pandas objects. You can create them however you
like and carry on from the modelling cell.

**A property map** just needs a table with columns `H`, `E` (and ideally `X`, `Y`):
```python
import pandas as pd
df = pd.read_csv("my_map.csv")                 # your file
df = df.rename(columns={"Hardness": "H", "Modulus": "E"})
df["HE"] = df["H"] / df["E"]                    # the notebooks expect H, E, HE
# now use df exactly like mm.load_map(...) returns
```

**A set of curves** just needs a list of `(depth_nm, load_mN)` arrays:
```python
curves = [(depth_array_1, load_array_1), (depth_array_2, load_array_2), ...]
# now use it exactly like mm.load_curves(...) returns
```

To turn a map column into an image for `imshow`:
```python
import mecanano_ml as mm
grid, extent = mm.map_to_grid(df, "H")         # 2-D array + [xmin,xmax,ymin,ymax]
```

## Option 2 — match the file conventions so `mm.load_map` reads your file

`mm.load_map` expects the high-speed-mapping CSV layout:

- a **two-row header**: row 1 = column names, row 2 = units (the units row is dropped);
- columns named `HARDNESS`, `MODULUS`, `X Position`, `Y Position` (renamed to
  `H`, `E`, `X`, `Y`); an `H/E` column is used if present, else computed;
- rows with non-finite or non-positive `H`/`E` are dropped automatically.

If your export matches that, add it to the `_MAPS` dictionary in
`src/mecanano_ml/io.py` and load it by name.

### Depth-resolved maps (the AFM grid, CrN–Cr, Al–Cu)
These load from a **long-format CSV** in `data/hsnm_maps/`, one row per (indent, depth)
sample, with columns `indent, x_um, y_um, depth_nm, H_GPa, E_GPa, load_mN`. To use your
own, write that CSV and load it by name:

```python
import mecanano_ml as mm
d = mm.load_hsnm_map("my_grid")   # dict: depth_nm (D,), and H, E, load (n_indents × D), X, Y
```

`mm.load_afm_grid()` is a convenience view of the shipped `afm_grid_g` that also exposes
per-indent curves `H_curve`, `E_curve`, `load_mN` (each `n_indents × D`) plus scalar
`H`, `E`, `HE` — where `D` is the number of depth points (**56** in the shipped grids).

## Sensible first steps on new data
1. Start with **notebook 00** patterns: load, print shapes, plot a map and a few curves.
2. Run **01 (PCA)** and **02 (clustering)** — do you see coherent regions? How many?
3. Only then move to supervised models (03), and always evaluate honestly (**03a**).

## Please respect data licences
If you publish results or share data, keep the attribution rules in **[[Datasets]]**,
and never commit data you don't have the right to redistribute.
