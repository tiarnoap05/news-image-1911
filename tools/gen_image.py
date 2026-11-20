#!/usr/bin/env python3
"""Draw the front page of 19 November 2026 as one 1024x1024 PNG.

A newspaper front page: masthead, dateline, the Shenzhen three-way summit
as the lead with the three flags, the day's other big stories in a grid,
a strip of smaller items, and a footer. Every text block is word-wrapped
to the box it lives in, so nothing overflows or overlaps.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (248, 244, 233)
INK = (20, 20, 20)
SOFT = (74, 74, 74)
RED = (163, 22, 33)
RULE = (20, 20, 20)
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to lines that fit max_w pixels (measured, not guessed)."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, align="left", leading=None, max_w=None):
    """Draw lines starting at y; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        lx = x
        if align == "center" and max_w is not None:
            lx = x + (max_w - draw.textlength(line, font=fnt)) / 2
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_usa(draw, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=(178, 34, 52))
    canton_w, canton_h = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + canton_w, y + canton_h], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            sx = x + 10 + c * 15
            sy = y + 8 + r * 13
            draw.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.polygon(star_points(x + 32, y + 32, 22, 9), fill=(255, 222, 0))
    for sx, sy in [(68, 16), (82, 30), (82, 50), (68, 64)]:
        draw.polygon(star_points(x + sx, y + sy, 8, 3.5), fill=(255, 222, 0))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def flag_russia(draw, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def story_cell(draw, x, y, w, kicker, headline, summary):
    """One headed story in a grid cell; returns y below the cell."""
    f_kick, f_head, f_sum = SANS_B(19), SERIF_B(27), SANS(19)
    y = draw_lines(draw, [kicker], f_kick, x, y, RED, leading=24)
    y = draw_lines(draw, wrap(draw, headline, f_head, w), f_head, x, y + 4,
                   INK, leading=32)
    y = draw_lines(draw, wrap(draw, summary, f_sum, w), f_sum, x, y + 6,
                   SOFT, leading=24)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    content_w = W - 2 * MARGIN

    # Masthead
    y = 26
    y = draw_lines(d, ["THE WORLD TODAY"], SERIF_B(68), MARGIN, y, INK,
                   align="center", max_w=content_w, leading=76)
    d.line([(MARGIN, y + 8), (W - MARGIN, y + 8)], fill=RULE, width=3)
    d.line([(MARGIN, y + 14), (W - MARGIN, y + 14)], fill=RULE, width=1)

    # Dateline
    y = draw_lines(d, ["T H U R S D A Y   1 9   N O V E M B E R   2 0 2 6"],
                   SANS_B(23), MARGIN, y + 24, INK, align="center",
                   max_w=content_w, leading=30)
    d.line([(MARGIN, y + 8), (W - MARGIN, y + 8)], fill=RULE, width=1)

    # Lead story: Shenzhen summit
    y = draw_lines(d, ["APEC  ·  SHENZHEN"], SANS_B(22), MARGIN, y + 22, RED,
                   align="center", max_w=content_w, leading=28)
    y = draw_lines(d, ["Trump, Xi and Putin meet", "in first three-way summit"],
                   SERIF_B(44), MARGIN, y + 6, INK, align="center",
                   max_w=content_w, leading=52)
    sub = ("Ninety minutes behind closed doors end in a joint “peace "
           "declaration” — silent on Ukraine and Iran. No major deal.")
    y = draw_lines(d, wrap(d, sub, SANS(21), 880), SANS(21), MARGIN, y + 10,
                   SOFT, align="center", max_w=content_w, leading=27)

    # The three flags
    fw, fh, gap = 200, 104, 24
    fx = (W - (3 * fw + 2 * gap)) // 2
    fy = y + 16
    for draw_flag, label in ((flag_usa, "UNITED STATES"),
                             (flag_china, "CHINA"),
                             (flag_russia, "RUSSIA")):
        draw_flag(d, fx, fy, fw, fh)
        d.text((fx + fw / 2, fy + fh + 8), label, font=SANS_B(16), fill=INK,
               anchor="ma")
        fx += fw + gap
    y = fy + fh + 34
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)

    # Story grid, two columns by two rows
    col_w = (content_w - 24) // 2
    cells = [
        ("THE HAGUE  ·  JUSTICE",
         "Court finds Myanmar guilty of Rohingya genocide",
         "9–6 ruling — the first genocide finding against a state."),
        ("IRAN WAR",
         "US strikes Qeshm Island; no major strikes until 2027",
         "Houthi missile damages Riyadh’s PIF Tower."),
        ("UKRAINE",
         "Crimean Bridge hit for a third time in a week",
         "Kyiv strikes the key crossing again."),
        ("MARKETS",
         "Anthropic IPO raises $81bn; shares jump 17%",
         "S&P 500 falls 2.0%, a fifth straight loss; Nikkei down 4.7%."),
    ]
    gy = y + 18
    row_h = 148
    for i, (kick, head, summ) in enumerate(cells):
        cx = MARGIN + (i % 2) * (col_w + 24)
        cy = gy + (i // 2) * row_h
        if i % 2 == 1:
            d.line([(MARGIN + col_w + 12, cy + 4),
                    (MARGIN + col_w + 12, cy + row_h - 16)], fill=(180, 175, 160),
                   width=1)
        story_cell(d, cx, cy, col_w, kick, head, summ)
    y = gy + 2 * row_h
    d.line([(MARGIN, y + 2), (W - MARGIN, y + 2)], fill=RULE, width=1)

    # Smaller items strip
    y = draw_lines(d, ["ALSO TODAY"], SANS_B(19), MARGIN, y + 14, RED,
                   leading=24)
    minis = [
        "COP31 talks end in deadlock",
        "N. Korea expands enrichment",
        "Bangladesh unrest leaves 4 dead",
        "Voyager 1 reaches one light-day",
    ]
    mini_w = (content_w - 3 * 20) // 4
    my = y + 6
    wrapped = [wrap(d, item, SANS_B(19), mini_w) for item in minis]
    max_lines = max(len(lines) for lines in wrapped)
    for i, lines in enumerate(wrapped):
        mx = MARGIN + i * (mini_w + 20)
        draw_lines(d, lines, SANS_B(19), mx, my, INK, leading=23)
    y = my + max_lines * 23 + 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)

    # Footer
    draw_lines(d, ["All the world’s news of Thursday 19 November 2026 — in one page."],
               SANS(16), MARGIN, y + 10, SOFT, align="center",
               max_w=content_w, leading=20)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
