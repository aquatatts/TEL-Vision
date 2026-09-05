#!/usr/bin/env python3
"""TEL Collection — product retouch pipeline.

"Invisible clean": removes handling residue, dust, fine scratches and the
packaging damage from the studio frames, while leaving every real reflection,
specular streak, gold letterform and the grain of the shot exactly as shot.

Two techniques, applied only inside declared regions:

  despeck    Bright specks on dark gloss are found with a median high-pass and
             healed with Telea inpainting — what a healing brush does.

  fill_tone  Handling residue and the creased box panel are low-frequency
             blemishes: the surface is the right shape, the wrong brightness.
             Frequency separation splits tone from detail. The tone layer is
             rebuilt by interpolating each column (or row) across the blemish
             from that same column's clean pixels, so the replacement is the
             surface's own gradient and matches perfectly at the mask edge —
             no inpainting, so nothing can be invented or dragged in from the
             background. The detail layer goes straight back, lightly damped
             only where the residue's own granularity lives.

             axis="col" fits down each column and preserves the vertical
             specular banding of a cylindrical jar. axis="row" fits across each
             row and is what erases a vertical crease in the box panel.

  settle     A feathered multiply that drops an over-bright panel into clean
             black. Used on the box end, which is a black surface photographed
             hot; darkening it is an exposure choice, not a fabrication.

The gold print is protected by an HSV mask throughout, every mask is hard-clipped
to the product body before feathering, and nothing outside the declared regions
is touched at all.

Usage:
    python3 tools/retouch.py             # every frame in JOBS
    python3 tools/retouch.py hero plate  # named frames only
"""

from __future__ import annotations

import os
import sys

import cv2
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "images", "web")
LONG_EDGE = 4000          # Shopify rejects over 25 MP; 4000 px long edge stays well under
JPEG_QUALITY = 92

# Low-frequency work happens on a downscaled copy: a low-pass carries no detail,
# so this is equivalent and roughly 16x faster on a 42 MP frame.
LOW_SCALE = 0.25
LOW_SIGMA = 55            # native px; the scale that separates tone from detail


# ----------------------------------------------------------------- masks ---

def gold_mask(bgr: np.ndarray) -> np.ndarray:
    """Protect the gold print. OpenCV hue is 0-179; the foil sits around 6-34."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = ((h >= 6) & (h <= 34) & (s >= 55) & (v >= 40)).astype(np.uint8)
    return cv2.dilate(m, np.ones((11, 11), np.uint8))


def shape_mask(shape, regions, feather: float = 0.0) -> np.ndarray:
    """0..1 float mask from a list of rects and ellipses."""
    m = np.zeros(shape[:2], np.float32)
    for r in regions:
        if r[0] == "ellipse":
            _, cx, cy, ax, ay = r
            cv2.ellipse(m, (cx, cy), (ax, ay), 0, 0, 360, 1.0, -1)
        else:
            _, x0, y0, x1, y1 = r
            cv2.rectangle(m, (x0, y0), (x1, y1), 1.0, -1)
    if feather > 0:
        m = cv2.GaussianBlur(m, (0, 0), feather)
    return np.clip(m, 0.0, 1.0)


# ------------------------------------------------------------ techniques ---

def despeck(bgr, regions, protect, k=9, thresh=12, min_area=3, max_area=900):
    """Heal bright specks (dust, lint, pinhole scratches) inside `regions`."""
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    med = cv2.medianBlur(gray, k)
    diff = gray.astype(np.int16) - med.astype(np.int16)

    spots = (diff > thresh).astype(np.uint8)
    spots[protect > 0] = 0
    spots &= (shape_mask(bgr.shape, regions) > 0.5).astype(np.uint8)
    spots = cv2.morphologyEx(spots, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    n, labels, stats, _ = cv2.connectedComponentsWithStats(spots, 8)
    keep = np.zeros_like(spots)
    hit = 0
    for i in range(1, n):
        if min_area <= stats[i, cv2.CC_STAT_AREA] <= max_area:
            keep[labels == i] = 1
            hit += 1
    if hit == 0:
        return bgr, 0
    keep = cv2.dilate(keep, np.ones((7, 7), np.uint8))   # cover each speck's soft edge
    return cv2.inpaint(bgr, keep, 5, cv2.INPAINT_TELEA), hit


def fill_tone(bgr, regions, body, axis="col", feather=70, hf_damp=0.45):
    """Rebuild the surface tone under a blemish from the surface's own pixels."""
    h, w = bgr.shape[:2]

    m = shape_mask(bgr.shape, regions)                       # hard blemish
    m *= shape_mask(bgr.shape, [body])                       # never leave the product
    if m.max() <= 0:
        return bgr
    m = np.clip(cv2.GaussianBlur(m, (0, 0), feather), 0, 1)  # soften after clipping

    s = LOW_SCALE
    small = cv2.resize(bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
    low_s = cv2.GaussianBlur(small, (0, 0), LOW_SIGMA * s)
    m_s = cv2.resize(m, (small.shape[1], small.shape[0]), interpolation=cv2.INTER_AREA)

    _, bx0, by0, bx1, by1 = body
    X0, Y0 = max(0, int(bx0 * s)), max(0, int(by0 * s))
    X1, Y1 = min(small.shape[1], int(bx1 * s)), min(small.shape[0], int(by1 * s))

    clean_s = low_s.copy()
    bad = m_s > 0.10
    if axis == "col":
        idx = np.arange(Y0, Y1, dtype=np.float32)
        for x in range(X0, X1):
            good = ~bad[Y0:Y1, x]
            if good.sum() < 4 or good.all():
                continue
            for c in range(3):
                clean_s[Y0:Y1, x, c] = np.interp(
                    idx, idx[good], low_s[Y0:Y1, x, c][good])
    else:
        idx = np.arange(X0, X1, dtype=np.float32)
        for y in range(Y0, Y1):
            good = ~bad[y, X0:X1]
            if good.sum() < 4 or good.all():
                continue
            for c in range(3):
                clean_s[y, X0:X1, c] = np.interp(
                    idx, idx[good], low_s[y, X0:X1, c][good])
    clean_s = cv2.GaussianBlur(clean_s, (0, 0), 5)

    low = cv2.resize(low_s, (w, h), interpolation=cv2.INTER_LINEAR)
    clean = cv2.resize(clean_s, (w, h), interpolation=cv2.INTER_LINEAR)
    m3 = m[..., None]
    high = bgr.astype(np.float32) - low
    out = low * (1.0 - m3) + clean * m3 + high * (1.0 - m3 * hf_damp)
    return np.clip(out, 0, 255).astype(np.uint8)


def settle(bgr, regions, amount=0.40, feather=45):
    """Feathered multiply — drops an over-bright panel into clean black."""
    m = shape_mask(bgr.shape, regions, feather)[..., None]
    return np.clip(bgr.astype(np.float32) * (1.0 - m * amount), 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ jobs ---
# Coordinates are native pixels on the camera original, read off a 500 px grid.

JOBS = {
    # Homepage hero (desktop) + social sharing image + first gallery frame.
    "hero": dict(
        src="DSC02912(4).jpg",
        out="tel-ritual-duo-01-sealed-set-hero-r1.jpg",
        work=[("rect", 2150, 1850, 3970, 3710),      # Recovery Cream
              ("rect", 3950, 1830, 5780, 3710),      # Restore Balm
              ("rect", 2430, 600, 5460, 1900)],      # metal card behind
        tone=[
            dict(body=("rect", 2250, 2430, 3900, 3650),
                 regions=[("ellipse", 2420, 2920, 215, 235),
                          ("ellipse", 2400, 3250, 185, 165)]),
            dict(body=("rect", 4020, 2420, 5700, 3650),
                 regions=[("ellipse", 4330, 2760, 235, 360)]),
        ],
    ),
    # Product plate on the homepage.
    "plate": dict(
        src="DSC02917(2).jpg",
        out="tel-ritual-duo-11-pair-and-box-r1.jpg",
        work=[("rect", 700, 1700, 2300, 3470),
              ("rect", 2270, 1770, 3820, 3500),
              ("rect", 3830, 1830, 7270, 3580)],
        tone=[
            dict(body=("rect", 780, 2330, 2240, 3400),
                 regions=[("ellipse", 1060, 2860, 250, 300)]),
            dict(body=("rect", 2350, 2380, 3760, 3430),
                 regions=[("ellipse", 2610, 2900, 225, 285)]),
            # The creased end panel: fit across each row to erase a vertical fold.
            # Both anchors stay well inside the panel — the corner fold and the
            # outer edge are specular highlights and would drag light inwards.
            dict(body=("rect", 6836, 1960, 7232, 3500),
                 regions=[("rect", 6876, 2000, 7192, 3460)],
                 axis="row", hf_damp=0.60, feather=34),
        ],
        panel=[("rect", 6850, 1975, 7225, 3485)],
        panel_amount=0.46,
    ),
    # Homepage hero (mobile) — the same damaged box, corner-on: the front-right
    # corner is scuffed white and the end panel carries the fold.
    "mobile": dict(
        src="DSC02858(2).jpg",
        out="tel-ritual-duo-09-sealed-box-r1.jpg",
        work=[("rect", 372, 1559, 4337, 5058)],
        max_area=1400,                              # the corner scuffs run long
        panel=[("rect", 4125, 3560, 4322, 5090)],
        panel_amount=0.34,
    ),
    # Ritual collection image.
    "collection": dict(
        src="DSC02853(2).jpg",
        out="tel-ritual-duo-15-jars-on-box-r1.jpg",
        work=[("rect", 2181, 1238, 5330, 4240)],
    ),
    # Product gallery.
    "single": dict(
        src="DSC02878(1).jpg",
        out="tel-ritual-duo-13-restore-balm-single-r1.jpg",
        work=[("rect", 2809, 1607, 4987, 3241)],
    ),
    "pair": dict(
        src="DSC02872(1).jpg",
        out="tel-ritual-duo-02-the-pair-r1.jpg",
        work=[("rect", 1999, 1537, 5588, 3184)],
    ),
    "panel8": dict(
        src="DSC02924(1).jpg",
        out="tel-ritual-duo-08-ingredient-panel-r1.jpg",
        work=[("rect", 1701, 1483, 6011, 3734)],
    ),
}

# Deliberately NOT retouched, and why:
#
#   DSC02885(2)  two open jars, top-down   -> the frame is mostly balm and cream.
#   DSC02890(2)  single open jar, macro       That texture is the product; a
#                                             speck detector cannot tell it from
#                                             dust, and smoothing it would be a
#                                             lie about what is in the jar.
#   DSC02860(3)  Chapter One card flat lay -> soft-touch card stock, shot to show
#                                             its grain. Despeckling reads as a
#                                             cheaper, flatter card.
#   DSC03003(2)  settled ink, founder band -> real skin and real ink are the whole
#   Valerio / founder portraits               argument. No skin work, ever.


def run(name: str, job: dict) -> dict:
    src = os.path.join(REPO, job["src"])
    bgr = cv2.imread(src, cv2.IMREAD_COLOR)
    if bgr is None:
        raise SystemExit(f"cannot read {src}")
    h, w = bgr.shape[:2]

    bgr, n = despeck(bgr, job["work"], gold_mask(bgr),
                     thresh=job.get("thresh", 12),
                     max_area=job.get("max_area", 900))

    for grp in job.get("tone", []):
        bgr = fill_tone(bgr, grp["regions"], grp["body"],
                        axis=grp.get("axis", "col"),
                        feather=grp.get("feather", 70),
                        hf_damp=grp.get("hf_damp", 0.45))

    if job.get("panel"):
        bgr = settle(bgr, job["panel"], amount=job.get("panel_amount", 0.38))

    scale = LONG_EDGE / max(w, h)
    if scale < 1:
        bgr = cv2.resize(bgr, (round(w * scale), round(h * scale)),
                         interpolation=cv2.INTER_AREA)
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, job["out"])
    cv2.imwrite(dst, bgr, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY,
                           cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
    print(f"{name:11s} {job['src']:18s} {w}x{h} -> {bgr.shape[1]}x{bgr.shape[0]}  "
          f"specks {n:5d}  {os.path.getsize(dst)//1024:5d} KB  {job['out']}")
    return dict(name=name, specks=n, out=dst)


if __name__ == "__main__":
    for nm in (sys.argv[1:] or list(JOBS)):
        if nm not in JOBS:
            raise SystemExit(f"unknown job {nm}; known: {', '.join(JOBS)}")
        run(nm, JOBS[nm])
