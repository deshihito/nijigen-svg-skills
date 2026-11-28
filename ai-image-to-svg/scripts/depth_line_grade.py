#!/usr/bin/env python3
"""Grade line width by estimated depth (3 stages).

Uniform line width is part of the "vector taste". This pass breaks it
deterministically in the raster layer: lines are split into depth bands
from a monocular depth estimate, far lines are shaved one layer thinner
and near lines are grown one layer thicker.

Depth model: Depth Anything V2 Small, ONNX (~99 MB), not bundled.
Download once:
  curl -L -o da2_small.onnx \
    https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model.onnx
Requires: numpy, opencv-python-headless, onnxruntime, pillow.

Usage:
  python3 depth_line_grade.py INPUT OUTPUT [--model da2_small.onnx]
                              [--bands 3] [--dark-sum 330] [--line-max-dist 7]

Notes (measured):
- Depth estimation works on flat illustrations too: the model reads
  composition priors (a foreshortened hand reads nearest, far hair
  reads farthest), so the estimate can run on the flat redraw itself
  and stays aligned with the lines being graded.
- A "line" pixel = dark AND within --line-max-dist px of a non-dark
  pixel (distance transform). Large dark fills (black clothing etc.)
  are excluded by construction.
- Shaved pixels are refilled from an inpainted fill image; grown
  pixels take the diffused line color. Work on the flat raster BEFORE
  background removal, with the key color as the background reference
  (top-left pixel).
"""
import argparse
import numpy as np
import cv2
import onnxruntime as ort
from PIL import Image


def estimate_depth(img_rgb, model_path):
    h, w = img_rgb.shape[:2]
    w2 = 518
    h2 = max(14, int(round(518 * h / w / 14)) * 14)
    im = cv2.resize(img_rgb, (w2, h2)).astype(np.float32) / 255.0
    im = (im - np.array([0.485, 0.456, 0.406], np.float32)) / np.array(
        [0.229, 0.224, 0.225], np.float32)
    x = im.transpose(2, 0, 1)[None].astype(np.float32)
    sess = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    d = sess.run(None, {sess.get_inputs()[0].name: x})[0][0]
    d = cv2.resize(d, (w, h))
    lo, hi = np.percentile(d, 2), np.percentile(d, 98)
    return np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1)


def grade(flat_rgb, depth, char_mask, dark_sum=330, line_max_dist=7):
    dark = (flat_rgb.astype(np.int32).sum(axis=2) < dark_sum) & char_mask
    dist = cv2.distanceTransform(dark.astype(np.uint8), cv2.DIST_L2, 5)
    line = dark & (dist <= line_max_dist)
    fill = cv2.inpaint(flat_rgb, line.astype(np.uint8) * 255, 3, cv2.INPAINT_TELEA)
    linecol = cv2.inpaint(flat_rgb, (~line).astype(np.uint8) * 255, 3, cv2.INPAINT_TELEA)
    dvals = depth[line]
    t1, t2 = np.percentile(dvals, 33), np.percentile(dvals, 66)
    band = np.zeros(depth.shape, np.uint8)
    band[depth > t1] = 1
    band[depth > t2] = 2
    out = flat_rgb.copy()
    shave = line & (band == 0) & (dist <= 1.4)
    out[shave] = fill[shave]
    grown = (cv2.dilate(line.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) \
        & char_mask & (band == 2)
    add = grown & ~line
    out[add] = linecol[add]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('output')
    ap.add_argument('--model', default='da2_small.onnx')
    ap.add_argument('--dark-sum', type=int, default=330)
    ap.add_argument('--line-max-dist', type=float, default=7)
    args = ap.parse_args()
    arr = np.asarray(Image.open(args.input).convert('RGB'))
    bgc = arr[5, 5].astype(int)
    char = np.abs(arr.astype(int) - bgc).sum(axis=2) >= 110
    depth = estimate_depth(arr, args.model)
    out = grade(arr, depth, char, args.dark_sum, args.line_max_dist)
    Image.fromarray(out).save(args.output)
    print('written:', args.output)


if __name__ == '__main__':
    main()
