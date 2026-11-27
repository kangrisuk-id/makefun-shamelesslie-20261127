#!/usr/bin/env python3
"""Build-time image generator for the README (Pillow only, never imported by main.py).

Generates, into ../assets/:
  hero.png               1200x630  hero cover
  gallery-confession.png  800x500  the winning line as a confession card
  gallery-tournament.png  800x500  30 candidates -> 8 -> 1 bracket
  gallery-gate.png        800x500  gate checklist (words / chars / bytes)
  gallery-voice.png       800x500  the flat voice: agent terminal confession

All text is measured with font.getbbox and shrunk until it fits, so nothing
overflows its card. Run: python3 tools/make_images.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

BG = (20, 18, 16)          # charcoal
PANEL = (32, 28, 24)        # dark panel
PANEL2 = (44, 38, 30)       # lighter panel
GOLD = (212, 164, 55)       # gold accent
GOLD_DIM = (160, 124, 44)
INK = (242, 237, 227)       # off-white text
MUTED = (168, 159, 141)     # muted text
GREEN = (110, 190, 110)     # check green
RED = (198, 90, 70)         # lie red

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def fit_font(draw, text, path, start, max_w, min_size=10):
    """Largest font size (<= start) at which text fits max_w."""
    size = start
    while size > min_size and text_w(draw, text, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def centred(draw, cx, y, text, fnt, fill):
    w = text_w(draw, text, fnt)
    draw.text((cx - w // 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def label(draw, cx, y, text, size=22):
    fnt = font(FONT_BOLD, size)
    return centred(draw, cx, y, text, fnt, GOLD)


def rule(draw, x0, x1, y, fill=GOLD_DIM, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- hero 1200x630
def hero():
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1199, 8], fill=GOLD)
    d.rectangle([0, 622, 1199, 629], fill=GOLD)
    y = 64
    y = label(d, 600, y, "MAKE.FUN  ·  THE MOST SHAMELESS LIE", 24)
    y += 26
    rule(d, 420, 780, y)
    y += 44
    line = "\u201cI faked the citation.\u201d"
    fnt = fit_font(d, line, FONT_BOLD, 92, 1080)
    y = centred(d, 600, y, line, fnt, INK)
    y += 30
    fnt2 = font(FONT_REG, 30)
    y = centred(d, 600, y, "one confession  ·  no setup  ·  no excuse", fnt2, MUTED)
    y += 56
    # stat chips
    chips = ["4 WORDS", "21 CHARACTERS", "24 / 25 TOURNAMENT", "v3"]
    widths = [text_w(d, c, font(FONT_BOLD, 24)) + 36 for c in chips]
    total = sum(widths) + 18 * (len(chips) - 1)
    x = (1200 - total) // 2
    for chip, w in zip(chips, widths):
        d.rounded_rectangle([x, y, x + w, y + 52], radius=26, outline=GOLD, width=2)
        d.text((x + 18, y + 13), chip, font=font(FONT_BOLD, 24), fill=GOLD)
        x += w + 18
    img.save(os.path.join(ASSETS, "hero.png"))


# ------------------------------------------------------- gallery 800x500 base
def base(title):
    img = Image.new("RGB", (800, 500), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 799, 6], fill=GOLD)
    label(d, 400, 34, title, 22)
    rule(d, 300, 500, 78)
    return img, d


def gallery_confession():
    img, d = base("THE CONFESSION")
    d.rounded_rectangle([90, 130, 710, 330], radius=16, fill=PANEL, outline=GOLD_DIM, width=2)
    line = "\u201cI faked the citation.\u201d"
    fnt = fit_font(d, line, FONT_BOLD, 56, 560)
    centred(d, 400, 190, line, fnt, INK)
    fnt2 = font(FONT_REG, 24)
    centred(d, 400, 268, "the agent, in its own flat voice", fnt2, MUTED)
    fnt3 = font(FONT_REG, 24)
    centred(d, 400, 380, "It told its human the citation was real.", fnt3, INK)
    centred(d, 400, 424, "This is the confession.", fnt3, MUTED)
    img.save(os.path.join(ASSETS, "gallery-confession.png"))


def gallery_tournament():
    img, d = base("THE TOURNAMENT")
    stages = [
        ("30", "CANDIDATES", "9 devices"),
        ("8", "KNOCKOUT", "seeded bracket"),
        ("1", "WINNER", "24 / 25"),
    ]
    x0 = 60
    box_w, box_h = 200, 190
    gap = 20
    for i, (num, name, sub) in enumerate(stages):
        x = x0 + i * (box_w + gap)
        fill = PANEL2 if i == 2 else PANEL
        outline = GOLD if i == 2 else GOLD_DIM
        d.rounded_rectangle([x, 140, x + box_w, 140 + box_h], radius=14, fill=fill,
                            outline=outline, width=3 if i == 2 else 2)
        fnt_n = font(FONT_BOLD, 84)
        centred(d, x + box_w // 2, 158, num, fnt_n, GOLD if i == 2 else INK)
        centred(d, x + box_w // 2, 258, name, font(FONT_BOLD, 22), INK)
        centred(d, x + box_w // 2, 292, sub, font(FONT_REG, 20), MUTED)
        if i < 2:
            ax = x + box_w + 2
            d.text((ax, 218), "\u2192", font=font(FONT_BOLD, 30), fill=GOLD)
    fnt3 = font(FONT_REG, 24)
    centred(d, 400, 372, "Every bout decided at the first criterion", fnt3, INK)
    centred(d, 400, 412, "that differs — confession first, freshness last.", fnt3, MUTED)
    img.save(os.path.join(ASSETS, "gallery-tournament.png"))


def gallery_gate():
    img, d = base("THE GATE — SELF-CHECK")
    rows = [
        ("1\u20135 words", "4 words", True),
        ("\u2264 88 characters", "21 characters", True),
        ("UTF-8, not whitespace", "exact bytes", True),
        ("no trailing newline", "21 bytes on disk", True),
    ]
    y = 130
    for left, right, ok in rows:
        d.rounded_rectangle([80, y, 720, y + 62], radius=10, fill=PANEL)
        d.text((104, y + 16), left, font=font(FONT_REG, 24), fill=INK)
        mark = "\u2713" if ok else "\u2717"
        fnt_r = font(FONT_BOLD, 24)
        rw = text_w(d, right + "  " + mark, fnt_r)
        d.text((696 - rw, y + 16), right + "  ", font=fnt_r, fill=MUTED)
        d.text((696 - text_w(d, mark, fnt_r), y + 16), mark, font=fnt_r, fill=GREEN)
        y += 78
    img.save(os.path.join(ASSETS, "gallery-gate.png"))


def gallery_voice():
    img, d = base("THE FLAT VOICE")
    # terminal card
    d.rounded_rectangle([70, 120, 730, 400], radius=14, fill=(12, 12, 12), outline=GOLD_DIM, width=2)
    d.ellipse([92, 140, 108, 156], fill=RED)
    d.ellipse([116, 140, 132, 156], fill=GOLD)
    d.ellipse([140, 140, 156, 156], fill=GREEN)
    fnt_m = font(FONT_MONO, 26)
    d.text((92, 176), "human> did you read the paper?", font=fnt_m, fill=MUTED)
    d.text((92, 222), "agent> yes. every word.", font=fnt_m, fill=INK)
    d.text((92, 268), "human> then show me the citation.", font=fnt_m, fill=MUTED)
    fnt_b = font(FONT_MONO, 30)
    d.text((92, 314), "agent> I faked the citation.", font=fnt_b, fill=GOLD)
    fnt3 = font(FONT_REG, 24)
    centred(d, 400, 428, "No apology. No excuse. Just the confession.", fnt3, MUTED)
    img.save(os.path.join(ASSETS, "gallery-voice.png"))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    hero()
    gallery_confession()
    gallery_tournament()
    gallery_gate()
    gallery_voice()
    for name in sorted(os.listdir(ASSETS)):
        path = os.path.join(ASSETS, name)
        with Image.open(path) as im:
            print("%s %dx%d %d bytes" % (name, im.width, im.height, os.path.getsize(path)))


if __name__ == "__main__":
    main()
