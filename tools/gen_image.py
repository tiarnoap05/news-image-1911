#!/usr/bin/env python3
"""Build-time generator for the news-image-20261119 entry image.

Draws a newspaper front page for Thursday 19 November 2026 with PIL
(flat colours, exact text). The entrypoint main.py only copies the
resulting entry.png to /output/entry.png with the stdlib, so the graded
run needs no third-party package and no network.
Deterministic: same input, same bytes (PNG written with fixed settings).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 90, 90)
BLUE = (30, 58, 138)

FD = "/usr/share/fonts/truetype/dejavu/"
F_SERIF_B = lambda s: ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: ImageFont.truetype(FD + "DejaVuSans.ttf", s)
F_SANS_B = lambda s: ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
F_SERIF_I = lambda s: ImageFont.truetype(FD + "DejaVuSerif-Italic.ttf", s) if __import__("os").path.exists(FD + "DejaVuSerif-Italic.ttf") else ImageFont.truetype(FD + "DejaVuSerif.ttf", s)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            px = x + cw * (0.08 + c * 0.16)
            py = y + ch * (0.12 + r * 0.19)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star(x + w * 0.16, y + h * 0.28, h * 0.16, h * 0.065), fill=(255, 222, 0))
    for sx, sy in [(0.34, 0.14), (0.42, 0.26), (0.40, 0.42), (0.30, 0.48)]:
        d.polygon(star(x + w * sx, y + h * sy, h * 0.06, h * 0.025), fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # margin

    # Masthead
    d.text((W / 2, 34), "THE WORLD IN ONE PAGE", font=F_SERIF_B(58),
           fill=INK, anchor="ma")
    d.rectangle([mx, 108, W - mx, 142], fill=INK)
    d.text((W / 2, 112), "T H U R S D A Y ,  1 9  N O V E M B E R  2 0 2 6",
           font=F_SANS_B(22), fill=(255, 255, 255), anchor="ma")

    # Main headline
    d.text((W / 2, 162), "SHENZHEN  •  APEC SUMMIT", font=F_SANS_B(21),
           fill=RED, anchor="ma")
    d.text((W / 2, 190), "TRUMP, XI & PUTIN MEET", font=F_SERIF_B(56),
           fill=INK, anchor="ma")
    d.text((W / 2, 252), "IN FIRST THREE-WAY SUMMIT", font=F_SERIF_B(56),
           fill=INK, anchor="ma")
    sub = "The three leaders hold a 90-minute closed-door session and issue a joint " \
          "\u201cpeace declaration\u201d \u2014 silent on Ukraine and Iran."
    y = 322
    for ln in wrap(d, sub, F_SANS(23), W - 2 * mx - 40):
        d.text((W / 2, y), ln, font=F_SANS(23), fill=INK, anchor="ma")
        y += 30

    # Flags
    fy, fw, fh = 402, 300, 150
    gap = (W - 2 * mx - 3 * fw) / 2
    flags = [(flag_us, "UNITED STATES"), (flag_cn, "CHINA"), (flag_ru, "RUSSIA")]
    for i, (fn, label) in enumerate(flags):
        fx = mx + i * (fw + gap)
        fn(d, fx, fy, fw, fh)
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
        d.text((fx + fw / 2, fy + fh + 8), label, font=F_SANS_B(20),
               fill=INK, anchor="ma")

    # Divider
    d.line([mx, 596, W - mx, 596], fill=INK, width=3)

    # 2x2 story grid
    stories = [
        ("JUSTICE  •  THE HAGUE",
         "UN COURT: MYANMAR COMMITTED GENOCIDE",
         "The ICJ rules 9\u20136 the 2017 campaign against the Rohingya was genocide \u2014 its first such finding against a state."),
        ("MIDDLE EAST",
         "IRAN WAR: U.S. STRIKES QESHM ISLAND",
         "Trump: no major strikes until 2027. A Houthi missile damages Riyadh\u2019s PIF Tower as retaliation spreads."),
        ("UKRAINE",
         "CRIMEAN BRIDGE HIT A THIRD TIME",
         "Kyiv strikes the bridge again this week; Moscow vows a harsher response. Allies gather in Berlin."),
        ("MARKETS",
         "ANTHROPIC IPO SMASHES RECORDS",
         "Shares jump 17% after a ~$81bn raise, the largest ever. S&P 500 falls 2.0% for a fifth straight day."),
    ]
    cw, chh = 466, 158
    gx, gy = mx, 614
    for i, (kick, head, body) in enumerate(stories):
        x = gx + (i % 2) * (cw + 20)
        yy = gy + (i // 2) * (chh + 14)
        d.text((x, yy), kick, font=F_SANS_B(19), fill=RED)
        hy = yy + 26
        for ln in wrap(d, head, F_SERIF_B(26), cw):
            d.text((x, hy), ln, font=F_SERIF_B(26), fill=INK)
            hy += 31
        by = hy + 4
        for ln in wrap(d, body, F_SANS(19), cw):
            d.text((x, by), ln, font=F_SANS(19), fill=(40, 40, 40))
            by += 24

    # Bottom strip
    d.line([mx, 962, W - mx, 962], fill=INK, width=2)
    d.text((W / 2, 972), "ALSO: COP31 deadlocked  •  N. Korea expands enrichment  •  Bangladesh unrest: 4 dead  •  Voyager 1: one light-day",
           font=F_SANS(16), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
