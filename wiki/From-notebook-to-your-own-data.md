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

### The AFM-grid format (`.npz`)
`mm.load_afm_grid()` returns a dictionary of arrays. To build your own, save an `.npz`
with the same keys:

| key | shape | meaning |
|-----|-------|---------|
| `X`, `Y`, `H`, `E`, `HE` | `(n,)` | per-indent position and scalars |
| `H_curve`, `load_mN` | `(n, 64)` | per-indent depth-resolved curves |
| `depth_nm` | `(64,)` | the common depth axis |

```python
import numpy as np
np.savez("my_grid.npz", X=X, Y=Y, H=H, E=E, HE=H/E,
         H_curve=H_curve, load_mN=load_mN, depth_nm=depth_nm)
```

## Sensible first steps on new data
1. Start with **notebook 00** patterns: load, print shapes, plot a map and a few curves.
2. Run **01 (PCA)** and **02 (clustering)** — do you see coherent regions? How many?
3. Only then move to supervised models (03), and always evaluate honestly (**03a**).

## Please respect data licences
If you publish results or share data, keep the attribution rules in **[[Datasets]]**,
and never commit data you don't have the right to redistribute.
