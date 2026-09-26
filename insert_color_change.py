"""Insert a filament color change (M600) into a PrusaSlicer G-code file.

The color change is placed at the first layer whose middle lies above
--z (the groove floor), so the grooves show the first filament color and
the top surface shows the second one.
"""
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gcode", help="G-code file to modify in place")
    parser.add_argument("--z", type=float, required=True,
                        help="Height (mm) from the bed where the second color starts")
    parser.add_argument("--color_change_gcode", default="M600\nG1 E0.3 F1500 ; prime after color change",
                        help="G-code to insert")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.gcode) as f:
        lines = f.read().split("\n")

    z = height = None
    target = None
    for i, line in enumerate(lines):
        if m := re.match(r";Z:([\d.]+)", line):
            z = float(m.group(1))
        elif m := re.match(r";HEIGHT:([\d.]+)", line):
            height = float(m.group(1))
            if target is None and z - height / 2 > args.z:
                target = z
        elif target is not None and z == target and line.startswith(";TYPE:"):
            lines[i:i] = [f";COLOR_CHANGE,T0,z={target}"] + args.color_change_gcode.split("\n")
            break
    else:
        raise SystemExit(f"{args.gcode}: no layer found above z={args.z}")

    with open(args.gcode, "w") as f:
        f.write("\n".join(lines))
    print(f"{args.gcode}: color change at layer z={target}")


if __name__ == "__main__":
    main()
