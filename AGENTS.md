# AGENTS.md

Generator of 3D-printable ArUco markers (`generate_aruco.py`). In the
Borinots project these markers are called **borinucos** (ArUco markers
for borinots).

## Borinucos: marker specification

All 50 borinucos use the same dictionary and geometry; only the size
changes with the marker ID.

- Dictionary: `DICT_6X6_50` (IDs 0..49)
- Marker grid: 8x8 cells (6x6 data + 1-cell black border)
- Box thickness: 2.1 mm; groove depth: 0.85 mm
- White margin (quiet zone) around the marker: 10% of the box side

| IDs    | Box side | Margin | Marker side (black border, outer edge) | Cell size |
|--------|----------|--------|----------------------------------------|-----------|
| 0..20  | 100 mm   | 10 mm  | 80 mm                                  | 10 mm     |
| 21..30 | 40 mm    | 4 mm   | 32 mm                                  | 4 mm      |
| 31..40 | 180 mm   | 18 mm  | 144 mm                                 | 18 mm     |
| 41..49 | 210 mm   | 21 mm  | 168 mm                                 | 21 mm     |

210 mm is the MK3S bed depth (250x210 mm), so IDs 41..49 are sliced
without a skirt.

For pose estimation (e.g. OpenCV `estimatePoseSingleMarkers` /
`solvePnP`), the marker length to use is the **marker side** column
(outer edge of the black border), not the box side.

The source of truth for this mapping is the `borinucos` script.

## Generating and slicing

```bash
python3 -m venv aruco_3d_env   # Python 3.11 (pyenv)
aruco_3d_env/bin/pip install -r requirements.txt
./borinucos [output_dir]       # default: borinucos_out/
```

For each ID, `borinucos` writes `borinucoN.stl` and `borinucoN.gcode`:

- Slicing uses the PrusaSlicer CLI
  (`/Applications/Original Prusa Drivers/PrusaSlicer.app/Contents/MacOS/PrusaSlicer`,
  override with `PRUSA_SLICER`) and `borinucos-mk3s-petg.ini`
  (Prusa MK3S, Generic PETG, 0.2 mm layers).
- `insert_color_change.py` adds an `M600` filament change at the first
  layer above the groove floor (Z=1.4 mm with 0.2 mm layers). Load the
  black filament first (groove bottoms), white after the `M600` (top face).
- The PrusaSlicer CLI occasionally hangs idle; the script retries with a
  timeout. `--merge` segfaults on PrusaSlicer 2.9.6: to print several
  markers on one plate, concatenate the translated ASCII STLs into a single
  STL and slice that instead.
