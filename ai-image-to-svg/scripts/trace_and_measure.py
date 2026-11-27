#!/usr/bin/env python3
"""Trace a (flattened) raster image to SVG with fixed VTracer settings and
report path count / byte size. Fixed settings keep measurements comparable
across runs and images.

Usage:
    python3 trace_and_measure.py input.png output.svg [--render preview.png]

Requires: vtracer, pillow. cairosvg is optional (only for --render).
"""
import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--render", help="also render a PNG preview (needs cairosvg)")
    args = ap.parse_args()

    try:
        import vtracer
        from PIL import Image
    except ImportError:
        print("missing dependency: pip install vtracer pillow", file=sys.stderr)
        return 1

    im = Image.open(args.input).convert("RGBA")
    pixels = list(im.getdata())
    svg = vtracer.convert_pixels_to_svg(
        pixels,
        im.size,
        colormode="color",
        mode="spline",
        filter_speckle=16,
        color_precision=5,
        layer_difference=24,
        corner_threshold=60,
        length_threshold=6.0,
        splice_threshold=45,
        path_precision=2,
    )
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"input:  {args.input} ({im.size[0]}x{im.size[1]})")
    print(f"output: {args.output}")
    print(f"paths:  {svg.count('<path')}")
    print(f"bytes:  {len(svg.encode('utf-8'))}")

    if args.render:
        try:
            from cairosvg import svg2png

            svg2png(bytestring=svg.encode("utf-8"), write_to=args.render,
                    output_width=768, output_height=768)
            print(f"render: {args.render}")
        except ImportError:
            print("skip render: pip install cairosvg", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
