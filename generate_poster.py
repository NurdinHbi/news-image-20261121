#!/usr/bin/env python3
"""Deterministic newspaper front page for 21 November 2026.

Draws everything with PIL shapes + text. No network, no randomness,
no timestamps in the output, so repeated runs are byte-identical.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (185, 28, 28)
PANEL_BG = (255, 252, 244)
GREY = (90, 85, 75)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, max_w, start=32):
    """Largest headline size (down to 24) that fits in at most 2 lines."""
    for size in range(start, 23, -1):
        fnt = font(SANS_BOLD, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= 2:
            return fnt, lines
    fnt = font(SANS_BOLD, 24)
    return fnt, wrap(draw, text, fnt, max_w)


def motif(draw, kind, x0, y0, x1, y1):
    """One simple geometric motif per story, inside the given box."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    if kind == "handcuffs":
        # Two linked rings + a short chain between them (Mexico capture).
        r = 25
        for cxr in (cx - 36, cx + 36):
            draw.ellipse([cxr - r, cy - r, cxr + r, cy + r],
                         outline=INK, width=5)
            draw.ellipse([cxr - 10, cy - 10, cxr + 10, cy + 10],
                         outline=INK, width=3)
        for link_x in (cx - 8, cx + 8):
            draw.ellipse([link_x - 7, cy - 7, link_x + 7, cy + 7],
                         outline=INK, width=3)
        draw.line([cx - 11, cy, cx - 1, cy], fill=INK, width=4)
    elif kind == "ship":
        # Cargo ship hull, mast, smoke puffs, waves (Baltic).
        draw.polygon([(x0 + 30, cy - 6), (x1 - 30, cy - 6),
                      (x1 - 52, cy + 22), (x0 + 52, cy + 22)],
                     outline=INK, width=4)
        draw.line([cx, cy - 6, cx, cy - 38], fill=INK, width=4)
        draw.line([cx, cy - 38, cx + 26, cy - 26], fill=RED, width=4)
        for sx, sy, sr in ((cx - 52, cy - 34, 7), (cx - 38, cy - 44, 9),
                           (cx - 20, cy - 50, 7)):
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                         outline=GREY, width=3)
        for wy in (cy + 28, cy + 38):
            for wx in range(x0 + 20, x1 - 20, 44):
                draw.arc([wx, wy - 6, wx + 34, wy + 6], 180, 360,
                         fill=INK, width=3)
    elif kind == "blast":
        # Starburst over a building silhouette (Kryvyi Rih strike).
        by1 = y1 - 8
        draw.rectangle([cx - 72, cy + 8, cx - 18, by1], fill=INK)
        draw.rectangle([cx + 6, cy + 20, cx + 60, by1], fill=INK)
        for i in range(12):
            import math
            a = math.pi * i / 6
            x_a = cx + 34 * math.cos(a)
            y_a = cy - 14 + 34 * math.sin(a)
            x_b = cx + 52 * math.cos(a)
            y_b = cy - 14 + 52 * math.sin(a)
            draw.line([x_a, y_a, x_b, y_b], fill=RED, width=4)
        draw.ellipse([cx - 14, cy - 28, cx + 14, cy], fill=RED)
    elif kind == "chart":
        # Falling chart line with arrowhead (markets sell-off).
        draw.line([x0 + 24, y0 + 12, x0 + 24, y1 - 12], fill=INK, width=3)
        draw.line([x0 + 24, y1 - 12, x1 - 16, y1 - 12], fill=INK, width=3)
        pts = [(x0 + 34, y0 + 20), (x0 + 84, y0 + 32), (x0 + 124, y0 + 26),
               (x0 + 174, y0 + 52), (x0 + 224, y0 + 48), (x1 - 30, y1 - 22)]
        draw.line(pts, fill=RED, width=5, joint="curve")
        ex, ey = pts[-1]
        draw.polygon([(ex, ey), (ex - 18, ey - 2), (ex - 4, ey - 18)],
                     fill=RED)
    elif kind == "clock":
        # Clock with a red arc sweeping past 12 (talks run past deadline).
        import math
        r = 28
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
        for ang, ln in ((0, 8), (90, 8), (180, 8), (270, 8)):
            a = math.radians(ang)
            draw.line([cx + (r - ln) * math.cos(a), cy + (r - ln) * math.sin(a),
                       cx + (r - 2) * math.cos(a), cy + (r - 2) * math.sin(a)],
                      fill=INK, width=3)
        # Hands: just past the deadline hour.
        draw.line([cx, cy, cx + 16, cy - 12], fill=INK, width=4)
        draw.line([cx, cy, cx - 4, cy - 20], fill=INK, width=4)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        # Red sweep arc outside the face, arrowhead at its end.
        draw.arc([cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12],
                 -90, 150, fill=RED, width=4)
        ea = math.radians(150)
        ex, ey = cx + (r + 12) * math.cos(ea), cy + (r + 12) * math.sin(ea)
        draw.polygon([(ex, ey), (ex - 14, ey - 2), (ex - 2, ey - 14)],
                     fill=RED)
    elif kind == "crowd":
        # Rows of heads over shoulders (France marches).
        for row, y in enumerate((cy - 28, cy - 6, cy + 14)):
            n = 7 - row
            step = (x1 - x0 - 60) // max(n - 1, 1)
            for i in range(n):
                hx = x0 + 30 + i * step
                draw.ellipse([hx - 9, y - 9, hx + 9, y + 9],
                             outline=INK, width=3)
                draw.arc([hx - 15, y + 10, hx + 15, y + 22], 180, 360,
                         fill=INK, width=3)


STORIES = [
    ("MEXICO", "MEXICO NABS 'EL CHAPO ISIDRO'",
     "FBI Top 10 fugitive seized in Sinaloa; gunbattles erupt.", "handcuffs"),
    ("BALTIC", "DRONES HIT RUSSIAN SHIP IN BALTIC",
     "Sanctioned Sparta II burns, drifts into Finnish waters.", "ship"),
    ("UKRAINE", "MISSILE HITS ZELENSKY'S HOMETOWN",
     "Kryvyi Rih strike kills 2, wounds 60.", "blast"),
    ("MARKETS", "AI SELL-OFF DRAGS MARKETS DOWN",
     "S&P -3.7%, Nikkei -5.1% in global slide.", "chart"),
    ("CLIMATE", "COP31 TALKS RUN PAST DEADLINE",
     "Antalya summit stalls over fossil fuels.", "clock"),
    ("FRANCE", "FRENCH PROTESTS EBB",
     "82,500 march over living costs, turnout down.", "crowd"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    mast = font(SERIF_BOLD, 74)
    d.text((W // 2, 34), "THE WORLD TODAY", font=mast, fill=INK,
           anchor="ma")
    d.line([40, 122, W - 40, 122], fill=RED, width=5)
    date_f = font(SANS_BOLD, 26)
    d.text((W // 2, 138), "SATURDAY, 21 NOVEMBER 2026", font=date_f,
           fill=INK, anchor="ma")

    # 2 x 3 grid.
    gx, gy, gap = 40, 188, 16
    pw = (W - 2 * gx - gap) // 2
    ph = (H - gy - 40 - 2 * gap) // 3
    pad = 18
    for i, (kicker, headline, summary, kind) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=INK, width=2)
        tx = x0 + pad
        tw = pw - 2 * pad
        # Kicker.
        kf = font(SANS_BOLD, 20)
        d.text((tx, y0 + 12), kicker, font=kf, fill=RED)
        # Headline, auto-fit to max 2 lines.
        hf, hlines = fit_headline(d, headline, tw)
        hy = y0 + 44
        for line in hlines:
            d.text((tx, hy), line, font=hf, fill=INK)
            hy += hf.size + 4
        # Summary, max 2 lines.
        sf = font(SANS, 20)
        slines = wrap(d, summary, sf, tw)
        sy = y0 + 44 + len(hlines) * (hf.size + 4) + 8
        for line in slines[:2]:
            d.text((tx, sy), line, font=sf, fill=GREY)
            sy += 26
        # Motif strip at the bottom of the panel.
        motif(d, kind, x0 + 60, y1 - 84, x1 - 60, y1 - 10)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
