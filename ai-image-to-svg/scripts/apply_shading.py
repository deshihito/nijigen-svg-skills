#!/usr/bin/env python3
"""Layer-2 PNG shading: transfer the original's luminance field onto
the flat redraw as a smooth multiplicative blend.

The shading field S is the smoothed ratio (original luminance / flat
luminance), normalized per flat color cluster by its median (Srel), so
each part keeps its own base brightness and only the light's variation
is transferred. Two calibrated recipes:

  standard: clamp 0.55-1.5, strength 0.85
  soft:     clamp 0.70-1.25, strength 0.55  (originals with extreme
            lighting - dark scene + face spotlight - blow out at
            standard strength; use soft there)

Base image: the flat REDRAW raster, not an SVG render (measured: the
SVG-render base degrades the result). The original and the redraw do
not align pixel-perfectly; the field is heavily smoothed, so the
misalignment reads as soft shading rather than as edges.

Requires: numpy, scipy, pillow.

Usage:
  python3 apply_shading.py ORIGINAL FLAT OUTPUT [--recipe soft]
                           [--strength 0.55] [--clamp 0.70,1.25]
The flat image is expected to still carry its key-color background;
the character mask is derived from the top-left pixel color.
"""
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage

RECIPES = {
    'standard': (0.55, 1.5, 0.85),
    'soft': (0.70, 1.25, 0.55),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('original')
    ap.add_argument('flat')
    ap.add_argument('output')
    ap.add_argument('--recipe', choices=RECIPES, default='standard')
    ap.add_argument('--strength', type=float, default=None)
    ap.add_argument('--clamp', default=None, help='lo,hi')
    args = ap.parse_args()
    lo, hi, strength = RECIPES[args.recipe]
    if args.clamp:
        lo, hi = (float(v) for v in args.clamp.split(','))
    if args.strength is not None:
        strength = args.strength

    flat_im = Image.open(args.flat).convert('RGB')
    W, H = flat_im.size
    orig = Image.open(args.original).convert('RGB').resize((W, H))
    fa = np.asarray(flat_im).astype(float)
    oa = np.asarray(orig).astype(float)
    bgc = fa[0, 0]
    char = np.abs(fa - bgc).sum(axis=2) >= 110

    def lum(x):
        return 0.299 * x[:, :, 0] + 0.587 * x[:, :, 1] + 0.114 * x[:, :, 2]

    Lo = ndimage.gaussian_filter(lum(oa), 18)
    Lf = ndimage.gaussian_filter(lum(fa), 18)
    S = np.ones_like(Lo)
    m = char & (Lf > 12)
    S[m] = Lo[m] / np.maximum(Lf[m], 1)
    q = (fa // 24).astype(int)
    cid = q[:, :, 0] * 512 + q[:, :, 1] * 8 + q[:, :, 2]
    Srel = np.ones_like(S)
    for c in np.unique(cid[m]):
        sel = m & (cid == c)
        if sel.sum() < 800:
            continue
        med = np.median(S[sel])
        if med > 0:
            Srel[sel] = S[sel] / med
    Srel = ndimage.gaussian_filter(Srel, 5)
    Srel = np.clip(Srel, lo, hi)
    factor = 1 + (Srel - 1) * strength
    out = np.clip(fa * factor[:, :, None], 0, 255)
    out[~char] = [255, 255, 255]
    Image.fromarray(out.astype(np.uint8)).save(args.output, quality=90)
    print('written:', args.output)


if __name__ == '__main__':
    main()
