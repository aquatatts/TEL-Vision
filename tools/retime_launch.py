"""Change the doors-open hour on both launch graphics, and prove nothing else moved.

    python3 tools/retime_launch.py <fonts-dir> <in-dir> <out-dir>
"""
import sys, os
from collections import Counter
import numpy as np
import cv2
import post

RUNS_EXPECTED = 29          # glyph ink-runs in the footer line
CELLS_CHANGED = {22, 23}    # 0-based index into the run list: the '9' and the 'A'


def runs(img, band):
    """Ink runs along the footer line, as (x, top, bottom, width)."""
    y0, y1, x0, x1 = band
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(int)
    strip = g[y0:y1 + 1, x0:x1 + 1]
    ink = (strip - int(np.median(strip))) > 12
    cols, out, start = ink.any(axis=0), [], None
    for i, v in enumerate(list(cols) + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            rows = np.where(ink[:, start:i].any(axis=1))[0]
            out.append((start + x0, i - 1 + x0, rows.min() + y0, rows.max() + y0))
            start = None
    return out


def main(fonts, indir, outdir):
    font = os.path.join(fonts, post.FONT)
    os.makedirs(outdir, exist_ok=True)
    ok = True
    for key, name, protect in [
        ('4x5', 'tel-launch-post-4x5.png', None),
        ('9x16', 'tel-launch-story-9x16.png', (332, 355)),
    ]:
        src, dst = os.path.join(indir, name), os.path.join(outdir, name)
        band = post.GRAPHICS[key]['band']
        print('%s  (%s)' % (name, 'pristine' if protect is None else 'already patched'))
        before = cv2.imread(src)
        r = post.retime(src, dst, font, band, protect_from=protect)
        after = cv2.imread(dst)

        rb, ra = runs(before, band), runs(after, band)
        print('  runs: %d before, %d after' % (len(rb), len(ra)))
        ok &= len(ra) == RUNS_EXPECTED

        # Every glyph outside the hour must be bit-identical.
        for i, (b, a) in enumerate(zip(rb, ra)):
            if i in CELLS_CHANGED:
                continue
            if b != a:
                print('  !! run %d moved: %s -> %s' % (i, b, a)); ok = False

        # The new glyphs must sit in the same cap band as their neighbours. The
        # test is the line's own profile, not a single value: soft rendering
        # means the untouched 4:5 legitimately reads two cap tops, so demanding
        # one would fail the original. What must not happen is a glyph topping
        # or sitting outside the values the rest of the line already uses.
        def profile(rs):
            return (Counter(r[2] for r in rs), Counter(r[3] for r in rs))
        pb, pa = profile(rb), profile(ra)
        print('  cap tops  %s -> %s' % (dict(pb[0]), dict(pa[0])))
        print('  baselines %s -> %s' % (dict(pb[1]), dict(pa[1])))
        others = [r for i, r in enumerate(ra) if i not in CELLS_CHANGED]
        allowed_top = {r[2] for r in others}
        allowed_bot = {r[3] for r in others}
        for i in sorted(CELLS_CHANGED):
            t, bt = ra[i][2], ra[i][3]
            inside = t in allowed_top and bt in allowed_bot
            print('  run %d now top=%d baseline=%d  %s'
                  % (i, t, bt, 'in line' if inside else '!! OUT OF LINE'))
            ok &= inside

        ys = r['changed'][:, 0]; xs = r['changed'][:, 1]
        print('  %d pixels changed, x%d-%d y%d-%d'
              % (len(r['changed']), xs.min(), xs.max(), ys.min(), ys.max()))
        # Nothing outside the footer band may have been touched at all.
        ok &= ys.min() >= band[0] and ys.max() <= band[1]
        print()
    print('VERIFIED' if ok else 'FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
