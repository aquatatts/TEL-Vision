#!/usr/bin/env python3
"""TEL — retouch pass two.

Two frames Ben flagged by eye after the first pass went live on the draft theme.

  jars05  The top-down open-jars frame. Pass one was rim-only by design: both
          product discs were hard-masked so nothing inside the balm or cream
          could be altered. That left the specks sitting ON the product
          surfaces. Those are dust and lint on a waxy surface, not the product,
          so this pass heals them - but only points that are tiny, compact and
          darker than their own immediate surroundings. The swirl of the tool
          marks is low-frequency and wide, so the detector cannot see it, and a
          structure check asserts the swirl survives.

  back    The studio back shot. Pass one neutralised white balance off the wall
          and then lifted highlight warmth; the studio LEDs are strongly warm,
          so the two decisions compounded into orange skin. This pass balances
          off the floor tile instead, drops the warm lift, pulls saturation back
          in the skin band only, and runs a wider acne pass that reaches the
          upper arms and the lower back. Every inked pixel stays hard-masked
          with a zero-change assertion, as before.

No skin smoothing. No ink sharpening or darkening. No fabricated vignette.
"""
from __future__ import annotations
import os, sys
import cv2, numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "images", "web")
AUDIT = "/tmp/claude-0/-home-user-TEL-Vision/18075893-7f05-5187-adae-72a06c6fb232/scratchpad/pass2"
LONG_EDGE, Q = 4000, 92


def save(bgr, name, quality=Q):
    h, w = bgr.shape[:2]
    s = LONG_EDGE / max(w, h)
    if s < 1:
        bgr = cv2.resize(bgr, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
    p = os.path.join(OUT, name)
    cv2.imwrite(p, bgr, [cv2.IMWRITE_JPEG_QUALITY, quality, cv2.IMWRITE_JPEG_OPTIMIZE, 1])
    print(f"  wrote {p}  {bgr.shape[1]}x{bgr.shape[0]}")
    return p


def crop(bgr, x, y, w, h, name):
    c = bgr[max(0, y):y + h, max(0, x):x + w]
    cv2.imwrite(os.path.join(AUDIT, name), c, [cv2.IMWRITE_JPEG_QUALITY, 94])
    return c


# --------------------------------------------------------------- jars 05 ---

def find_discs(bgr):
    """The two product surfaces: the only large bright blobs in the frame."""
    s = 0.15
    small = cv2.resize(bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(g, 90, 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(th, 8)
    blobs = sorted(range(1, n), key=lambda i: -st[i, cv2.CC_STAT_AREA])[:2]
    out = []
    for i in blobs:
        m = (lab == i).astype(np.uint8)
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (cx, cy), r = cv2.minEnclosingCircle(cnts[0])
        out.append((cx / s, cy / s, r / s))
    out.sort(key=lambda c: c[0])
    return out


def jars05(src="DSC02885(2).jpg", out="tel-ritual-duo-05-both-open-top-down-r2.jpg"):
    bgr = cv2.imread(os.path.join(REPO, src))
    assert bgr is not None, src
    h, w = bgr.shape[:2]
    print(f"jars05  source {w}x{h}")
    discs = find_discs(bgr)
    for i, (cx, cy, r) in enumerate(discs):
        print(f"  disc {i}: centre {cx:.0f},{cy:.0f}  radius {r:.0f}")

    # --- pass A: dust ON the product, inside each disc, 4% inside the rim ---
    inside = np.zeros((h, w), np.uint8)
    for cx, cy, r in discs:
        cv2.circle(inside, (int(cx), int(cy)), int(r * 0.94), 1, -1)

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    med = cv2.medianBlur(gray, 15)                     # 15 px: wider than a speck,
    dark = med.astype(np.int16) - gray.astype(np.int16)  # far narrower than a swirl
    spots = ((dark > 9) & (inside > 0)).astype(np.uint8)
    spots = cv2.morphologyEx(spots, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))

    n, lab, st, _ = cv2.connectedComponentsWithStats(spots, 8)
    keep, hit, rej = np.zeros_like(spots), 0, 0
    for i in range(1, n):
        a = st[i, cv2.CC_STAT_AREA]
        bw, bh = st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]
        aspect = max(bw, bh) / max(1, min(bw, bh))
        fill = a / max(1, bw * bh)
        if 2 <= a <= 60 and aspect <= 2.6 and fill >= 0.42:
            keep[lab == i] = 1
            hit += 1
        else:
            rej += 1
    print(f"  disc specks kept {hit}, rejected {rej}")

    ov = bgr.copy()
    ov[cv2.dilate(keep, np.ones((9, 9), np.uint8)) > 0] = (0, 0, 255)
    cv2.imwrite(os.path.join(AUDIT, "05_disc_mask.jpg"),
                cv2.resize(ov, None, fx=0.35, fy=0.35), [cv2.IMWRITE_JPEG_QUALITY, 92])

    work = bgr
    if hit:
        m = cv2.dilate(keep, np.ones((5, 5), np.uint8)) & inside
        work = cv2.inpaint(bgr, m, 4, cv2.INPAINT_TELEA)
        # inpaint reads a neighbourhood, so composite the result back through the
        # disc mask: outside it, the original pixels are kept bit for bit.
        work = np.where(inside[..., None] > 0, work, bgr)
        d = cv2.absdiff(work, bgr).max(axis=2)
        print(f"  disc pass changed {int((d > 0).sum()):,} px")
        assert d[inside == 0].max() == 0, "disc pass touched pixels outside the discs"

    # --- pass B: rim, bright specks on the black annulus (pass one, repeated) ---
    ann = np.zeros((h, w), np.uint8)
    for cx, cy, r in discs:
        cv2.circle(ann, (int(cx), int(cy)), int(r * 1.30), 1, -1)
        cv2.circle(ann, (int(cx), int(cy)), int(r * 1.005), 0, -1)

    gray = cv2.cvtColor(work, cv2.COLOR_BGR2GRAY)
    med = cv2.medianBlur(gray, 9)
    bright = gray.astype(np.int16) - med.astype(np.int16)
    spots = ((bright > 12) & (ann > 0)).astype(np.uint8)
    spots = cv2.morphologyEx(spots, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(spots, 8)
    keep, hit, rej = np.zeros_like(spots), 0, 0
    for i in range(1, n):
        a = st[i, cv2.CC_STAT_AREA]
        bw, bh = st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]
        aspect = max(bw, bh) / max(1, min(bw, bh))
        fill = a / max(1, bw * bh)
        if 3 <= a <= 260 and aspect <= 2.6 and fill >= 0.42:
            keep[lab == i] = 1
            hit += 1
        else:
            rej += 1
    print(f"  rim specks kept {hit}, gloss rejected {rej}")
    if hit:
        before = work
        m = cv2.dilate(keep, np.ones((7, 7), np.uint8)) & ann
        work = cv2.inpaint(work, m, 5, cv2.INPAINT_TELEA)
        work = np.where(ann[..., None] > 0, work, before)
        d = cv2.absdiff(work, before).max(axis=2)
        print(f"  rim pass changed {int((d > 0).sum()):,} px")
        assert d[ann == 0].max() == 0, "rim pass leaked off the annulus"

    # swirl must survive: compare low-frequency structure inside the discs
    def swirl_energy(img):
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
        band = cv2.GaussianBlur(g, (0, 0), 6) - cv2.GaussianBlur(g, (0, 0), 40)
        return float(np.abs(band)[inside > 0].mean())
    e0, e1 = swirl_energy(bgr), swirl_energy(work)
    print(f"  swirl structure {e0:.3f} -> {e1:.3f}  ({100*(e1-e0)/e0:+.2f}%)")
    assert e1 > e0 * 0.97, "the swirl lost structure - too aggressive"

    for i, (cx, cy, r) in enumerate(discs):
        x, y, s = int(cx - r), int(cy - r), int(r * 2)
        a = crop(bgr, x, y, s, s, f"05_jar{i}_before.jpg")
        b = crop(work, x, y, s, s, f"05_jar{i}_after.jpg")
        cv2.imwrite(os.path.join(AUDIT, f"05_jar{i}_ba.jpg"), np.hstack([a, b]),
                    [cv2.IMWRITE_JPEG_QUALITY, 94])
    save(work, out)
    return work




# ------------------------------------------------------------------ back ---

def _masks(bgr):
    """Ink (protect absolutely), and skin (where acne may be healed)."""
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    L, A = lab[..., 0].astype(np.int16), lab[..., 1].astype(np.int16)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0].astype(np.int16), hsv[..., 1].astype(np.int16), hsv[..., 2].astype(np.int16)

    # Ink and shading read dark and desaturated. Generous, then dilated: the rule
    # is that nothing under the artwork may be altered, so the mask errs wide.
    ink = ((L < 108) | (V < 104)).astype(np.uint8)
    ink = cv2.dilate(ink, np.ones((9, 9), np.uint8))

    skin = ((H >= 2) & (H <= 26) & (S >= 38) & (V >= 88) & (ink == 0)).astype(np.uint8)
    # Only where skin dominates a wide neighbourhood - kills the wooden mirror
    # frames, the timber shelf and anything else warm but not a body. On a fully
    # covered back the bare skin is a lattice between linework, so the bar is set
    # at a quarter of the window rather than a majority.
    dens = cv2.blur(skin.astype(np.float32), (201, 201))
    skin = ((skin > 0) & (dens > 0.22)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return ink, skin, A


def _wb_gains(bgr):
    """Neutral from the floor tile: low-saturation mid-bright pixels, bottom strip."""
    h, w = bgr.shape[:2]
    strip = bgr[int(h * 0.86):, :, :]
    hsv = cv2.cvtColor(strip, cv2.COLOR_BGR2HSV)
    ok = (hsv[..., 1] < 60) & (hsv[..., 2] > 90) & (hsv[..., 2] < 245)
    if ok.sum() < 5000:
        return np.ones(3, np.float32)
    mean = strip[ok].reshape(-1, 3).mean(axis=0).astype(np.float32)
    g = mean.mean() / np.maximum(mean, 1e-3)
    return np.clip(g, 0.86, 1.16).astype(np.float32)


def back(src="DSC00760(1).jpeg", out="tel-founder-back-studio-r2.jpg"):
    bgr = cv2.imread(os.path.join(REPO, src))
    assert bgr is not None, src
    h, w = bgr.shape[:2]
    print(f"back  source {w}x{h}")
    orig = bgr.copy()
    ink, skin, A = _masks(bgr)
    print(f"  skin {skin.mean()*100:.1f}% of frame, ink mask {ink.mean()*100:.1f}%")

    ov = bgr.copy()
    ov[skin > 0] = (0.45 * ov[skin > 0] + 0.55 * np.array([0, 255, 0])).astype(np.uint8)
    cv2.imwrite(os.path.join(AUDIT, "back_skinmask.jpg"),
                cv2.resize(ov, None, fx=0.28, fy=0.28), [cv2.IMWRITE_JPEG_QUALITY, 90])

    # --- acne: compact points that are redder than their own surroundings ---
    Amed = cv2.medianBlur(cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[..., 1], 31)
    red = (A - Amed.astype(np.int16))
    spots = ((red >= 4) & (skin > 0)).astype(np.uint8)
    spots = cv2.morphologyEx(spots, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    scale = (h * w) / (7545 * 5033)
    lo, hi = max(4, int(6 * scale)), int(2600 * scale)
    n, lab_, st, _ = cv2.connectedComponentsWithStats(spots, 8)
    keep, hit, rej = np.zeros_like(spots), 0, 0
    for i in range(1, n):
        a = st[i, cv2.CC_STAT_AREA]
        bw, bh = st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]
        aspect = max(bw, bh) / max(1, min(bw, bh))
        fill = a / max(1, bw * bh)
        if lo <= a <= hi and aspect <= 2.4 and fill >= 0.45:
            keep[lab_ == i] = 1
            hit += 1
        else:
            rej += 1
    print(f"  acne marks kept {hit}, rejected {rej}  (area {lo}-{hi} px)")

    ov = bgr.copy()
    ov[cv2.dilate(keep, np.ones((15, 15), np.uint8)) > 0] = (0, 0, 255)
    cv2.imwrite(os.path.join(AUDIT, "back_acne_mask.jpg"),
                cv2.resize(ov, None, fx=0.28, fy=0.28), [cv2.IMWRITE_JPEG_QUALITY, 90])

    if hit:
        m = cv2.dilate(keep, np.ones((9, 9), np.uint8))
        m[ink > 0] = 0                                   # never under the artwork
        m &= skin
        healed = cv2.inpaint(bgr, m, 6, cv2.INPAINT_TELEA)
        bgr = np.where(skin[..., None] > 0, healed, bgr)  # composite through skin
        d = cv2.absdiff(bgr, orig).max(axis=2)
        print(f"  acne pass changed {int((d > 0).sum()):,} px")
        assert d[ink > 0].max() == 0, "acne pass touched inked pixels"
        assert d[skin == 0].max() == 0, "acne pass left the skin mask"

    # --- grade ---
    g = _wb_gains(bgr)
    print(f"  white balance gains B,G,R = {g[0]:.3f}, {g[1]:.3f}, {g[2]:.3f}")
    f = bgr.astype(np.float32) * g[None, None, :]
    f = np.clip(f, 0, 255)

    # Pull the warmth back in the skin band only. The LEDs are tungsten-warm, so
    # a global balance cannot fix skin without turning the room blue.
    hsv = cv2.cvtColor(f.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    Hc, Sc, Vc = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    warm = ((Hc >= 2) & (Hc <= 26) & (Sc >= 30)).astype(np.float32)
    warm = cv2.GaussianBlur(warm, (0, 0), 6)             # no hard edges
    hsv[..., 1] = Sc * (1.0 - 0.42 * warm)               # 42% less orange
    hsv[..., 0] = Hc + 2.0 * warm                        # a touch off red
    f = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    # Black point, gentle curve, highlight roll-off for the two ceiling lamps.
    f = np.clip((f - 9.0) * (255.0 / (255.0 - 9.0)), 0, 255)
    x = f / 255.0
    x = np.clip(x, 0, 1) ** 0.98
    x = x + 0.10 * x * (1 - x) * (x - 0.5) * 2           # low-contrast S
    x = np.clip(x, 0, 1)
    hot = np.clip((x - 0.90) / 0.10, 0, 1)
    x = x - hot * hot * 0.05                             # rolls the lamps back
    graded = np.clip(x * 255.0, 0, 255).astype(np.uint8)

    def warmth(img, m):
        b, r = img[..., 0][m > 0].mean(), img[..., 2][m > 0].mean()
        return r - b
    print(f"  skin red-minus-blue  {warmth(orig, skin):.1f} -> {warmth(graded, skin):.1f}")

    for nm, (x0, y0, x1, y1) in {
        "shoulders": (0.18, 0.14, 0.86, 0.34),
        "armL":      (0.06, 0.30, 0.34, 0.58),
        "armR":      (0.68, 0.30, 0.97, 0.58),
        "lower":     (0.22, 0.60, 0.82, 0.82),
    }.items():
        X0, Y0, X1, Y1 = int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)
        a, b = orig[Y0:Y1, X0:X1], graded[Y0:Y1, X0:X1]
        sc = 1300 / max(1, a.shape[1])
        a = cv2.resize(a, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        b = cv2.resize(b, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(AUDIT, f"back_{nm}_ba.jpg"), np.hstack([a, b]),
                    [cv2.IMWRITE_JPEG_QUALITY, 93])
    save(graded, out)
    return graded


if __name__ == "__main__":
    jobs = sys.argv[1:] or ["jars05", "back"]
    for j in jobs:
        globals()[j]()
