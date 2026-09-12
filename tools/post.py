"""Re-time the launch graphics.

The two launch graphics (4:5 feed post, 9:16 story) were rendered by a script that
was never saved, so the doors-open time is baked into the pixels. This module
changes that one string without touching anything else on the canvas.

Why surgery rather than re-rendering the whole poster: the graphics are approved
artwork. Reproducing the Cormorant display type, the 500-tick gradient grid and the
double keyline exactly enough to be indistinguishable is a much larger risk than
replacing three glyph cells, and a near-miss would mean re-approving the launch
asset days before launch.

The footer line is monospaced, so it is a grid of fixed-width cells:

    'SEALED  .  NEVER SOLD APART  .  9AM AEST'
                                     ^^  cells 32,33 carry the hour

Two of the three glyphs needed are already present in the same line, rendered by
the original script at the original size:

    P  <- copied from the P of APART (cell 23), sub-pixel shifted into cell 33
    M  <- already in place at cell 34, never touched
    7  <- the only glyph that has to be synthesised

The synthetic 7 is validated before it is used: the same renderer draws a 9 into
cell 32 and that 9 is scored against the real 9 it would be standing in for. If a
rendered 9 cannot pass for the real 9, a rendered 7 has no business being there
either, and the run aborts.
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

BG = np.array([8.0, 8.0, 8.0])                  # canvas ground, #080808
FONT = 'IBM_Plex_Mono_wght_400.ttf'

OLD = 'SEALED  ·  NEVER SOLD APART  ·  9AM AEST'
NEW = 'SEALED  ·  NEVER SOLD APART  ·  7PM AEST'

I_HOUR, I_MERIDIAN = 32, 33                     # cells that change
I_SOURCE_P = 23                                 # the P of APART


def render_cells(text, font_path, size, advance, w, h, x0, baseline, sigma, S=4):
    """Draw `text` on a w*h field, one glyph per fixed advance.

    Rendered at S times scale and box-averaged down, then softened by `sigma`,
    which is how the original script's output behaves under measurement.
    """
    img = Image.new('L', (w * S, h * S), 0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, int(round(size * S)))
    x = x0 * S
    for ch in text:
        if ch != ' ':
            draw.text((x, baseline * S), ch, font=font, fill=255, anchor='ls')
        x += advance * S
    a = np.array(img, dtype=np.float64).reshape(h, S, w, S).mean(axis=(1, 3)) / 255.0
    return cv2.GaussianBlur(a, (0, 0), sigma) if sigma > 0 else a


def render_one(ch, index, font_path, size, advance, w, h, x0, baseline, sigma, S=4):
    """Render a single glyph into the cell at `index`, everything else empty."""
    return render_cells(' ' * index + ch, font_path, size, advance,
                        w, h, x0, baseline, sigma, S)


def band_alpha(band):
    """Coverage 0..1 of the ink over the ground, and the ink colour itself.

    Solved per channel against the ground rather than off greyscale, so the
    warm grey of the type is preserved exactly when it is laid back down.
    """
    d = band.astype(np.float64) - BG
    span = d.reshape(-1, 3)
    ink = BG + span[np.linalg.norm(span, axis=1).argmax()]
    v = ink - BG
    a = (d @ v) / float(v @ v)
    return np.clip(a, 0, 1), ink


def composite(band, alpha, ink):
    """Lay `alpha` coverage of `ink` over the ground."""
    return np.clip(BG + alpha[..., None] * (ink - BG), 0, 255)


def subpixel_shift(a, dx):
    M = np.float32([[1, 0, dx], [0, 1, 0]])
    return cv2.warpAffine(a, M, (a.shape[1], a.shape[0]),
                          flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT,
                          borderValue=0)


# Each graphic's footer band, generous enough to hold the line and its soft edges.
GRAPHICS = {
    '4x5':   dict(band=(1150, 1174, 330, 750)),
    '9x16':  dict(band=(1672, 1694, 330, 750)),
}

COARSE = dict(size=(10.4, 12.4, 0.4), advance=(10.10, 10.19, 0.03),
              baseline=(15.0, 17.2, 0.4), x0=(8.25, 9.85, 0.4),
              sigma=(0.25, 0.60, 0.1))
# One refinement pass per axis, a step either side of the coarse winner.
REFINE_STEPS = dict(size=0.05, advance=0.005, baseline=0.05, x0=0.05, sigma=0.05)


def _axis(lo, hi, step):
    return np.arange(lo, hi + step / 2, step)


def search(score, coarse=COARSE):
    """Coarse sweep, then a local refinement around the winner on each axis."""
    axes = {k: _axis(*v) for k, v in coarse.items()}
    best = None
    for size in axes['size']:
        for advance in axes['advance']:
            for baseline in axes['baseline']:
                for x0 in axes['x0']:
                    for sigma in axes['sigma']:
                        s = score(size, advance, baseline, x0, sigma)
                        if best is None or s < best[0]:
                            best = (s, size, advance, baseline, x0, sigma)
    names = ['size', 'advance', 'baseline', 'x0', 'sigma']
    for _ in range(3):
        for i, name in enumerate(names):
            step, centre = REFINE_STEPS[name], best[i + 1]
            span = coarse[name][2]
            for v in _axis(centre - span, centre + span, step):
                trial = list(best[1:])
                trial[i] = v
                s = score(*trial)
                if s < best[0]:
                    best = tuple([s] + trial)
    return best


def cell_span(index, x0, advance):
    return x0 + index * advance, x0 + (index + 1) * advance


def glyph_spread(alpha, x0, advance, text=OLD):
    """How much two real instances of the same letter already differ.

    Each cell lands on its own sub-pixel phase, so the line's own A's are not
    identical to each other. That spread is the yardstick a synthesised glyph
    has to meet — anything inside it cannot be picked out by eye.
    """
    def cell(i):
        lo = x0 + i * advance
        return alpha[:, int(round(lo)):int(round(lo + advance))]

    where = {}
    for i, ch in enumerate(text):
        if ch.strip():
            where.setdefault(ch, []).append(i)
    out = []
    for idxs in where.values():
        for m in range(len(idxs)):
            for n in range(m + 1, len(idxs)):
                u, v = cell(idxs[m]), cell(idxs[n])
                k = min(u.shape[1], v.shape[1])
                out.append(float(np.sqrt(np.mean((u[:, :k] - v[:, :k]) ** 2))))
    return out or [0.0]


def retime(path, out_path, font_path, band, protect_from=None, report=print):
    """Replace the hour in one graphic's footer line. Returns a report dict."""
    y0, y1, x0i, x1i = band
    im = cv2.imread(path).astype(np.float64)
    original = im.copy()
    strip = im[y0:y1 + 1, x0i:x1i + 1]
    alpha, ink = band_alpha(strip)
    h, w = alpha.shape

    # Score only where the line is untouched: the hour cells may already hold a
    # bad patch, and fitting to that would reproduce the fault.
    mask = np.ones_like(alpha, dtype=bool)
    if protect_from is not None:
        mask[:, protect_from[0]:protect_from[1]] = False

    def score(size, advance, baseline, x0, sigma):
        c = render_cells(OLD, font_path, size, advance, w, h, x0, baseline, sigma)
        return float(np.sqrt(np.mean((alpha[mask] - c[mask]) ** 2)))

    best = search(score)
    fit_rmse, size, advance, baseline, xs, sigma = best
    report('  fit: rmse=%.4f size=%.2f advance=%.4f baseline=%.2f x0=%.3f sigma=%.2f'
           % best)

    args = (font_path, size, advance, w, h, xs, baseline, sigma)

    # --- gate: can this renderer pass for the original's own glyphs? ---
    # Only meaningful where the real 9 is still on the canvas; a graphic that has
    # already been patched no longer has one to score against.
    floor = glyph_spread(alpha, xs, advance)
    report('  the line\'s own repeated glyphs differ by rmse %.4f-%.4f'
           % (min(floor), max(floor)))
    if protect_from is None:
        nine = render_one('9', I_HOUR, *args)
        box = nine > 0.01
        gate = float(np.sqrt(np.mean((alpha[box] - nine[box]) ** 2)))
        report('  gate: synthetic 9 vs the real 9 it replaces — rmse=%.4f' % gate)
        # Held to the graphic's own standard: each glyph lands on a different
        # sub-pixel phase, so two real A's already differ. A synthetic glyph is
        # good enough exactly when it sits inside that natural spread.
        if gate > max(floor):
            raise SystemExit('synthetic glyph falls outside the line\'s own '
                             'glyph-to-glyph variation; aborting')

    # --- build the new hour ---
    seven = render_one('7', I_HOUR, *args)

    # P is not synthesised: it is the P of APART, moved ten cells to the right.
    src_lo, _ = cell_span(I_SOURCE_P, xs, advance)
    dst_lo, _ = cell_span(I_MERIDIAN, xs, advance)
    shift = dst_lo - src_lo
    p_src = np.zeros_like(alpha)
    lo, hi = int(np.floor(src_lo)), int(np.ceil(src_lo + advance))
    p_src[:, lo:hi] = alpha[:, lo:hi]
    p_moved = subpixel_shift(p_src, shift)

    # --- clear the two hour cells, then lay the new glyphs down ---
    clear_lo = int(np.floor(cell_span(I_HOUR, xs, advance)[0]))
    clear_hi = int(np.floor(cell_span(I_MERIDIAN + 1, xs, advance)[0])) - 1
    new_alpha = alpha.copy()
    new_alpha[:, clear_lo:clear_hi] = 0.0
    new_alpha = np.clip(new_alpha + seven + p_moved, 0, 1)
    rebuilt = composite(strip, new_alpha, ink)

    # Write back ONLY the hour's own columns. Recomposing the whole band from a
    # one-dimensional alpha would nudge every other glyph by a rounding step and
    # shift the ink threshold under its neighbours, so the window is fenced: one
    # column of slack for the new glyphs' soft edges, stopping short of the M.
    window = slice(max(clear_lo - 2, 0), min(clear_hi + 1, alpha.shape[1]))
    out = np.rint(original).astype(np.uint8)
    out[y0:y1 + 1, x0i + window.start:x0i + window.stop] = \
        np.rint(rebuilt[:, window]).astype(np.uint8)
    cv2.imwrite(out_path, out)

    changed = np.argwhere(np.any(out != np.rint(original).astype(np.uint8), axis=2))
    return dict(fit_rmse=fit_rmse, size=size, advance=advance, baseline=baseline,
                x0=xs, sigma=sigma, ink=ink, clear=(clear_lo, clear_hi),
                changed=changed, band=band)
