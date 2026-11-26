#!/usr/bin/env python3
"""Render the 26 November 2026 world-news infographic (1024x1024 PNG).

Everything on the page is laid out from the constants below: six stories
in a 2x3 card grid under a navy masthead, an ALSO strip and a footer.
No randomness, no clock, no network — two runs produce identical bytes.
Run:  python3 draw.py [output.png]
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

PAPER = (247, 242, 231)      # page background
NAVY = (20, 33, 61)          # masthead and ALSO strip
GOLD = (232, 163, 61)        # rule, globe, date
INK = (26, 26, 26)           # headlines
BODY = (74, 74, 74)          # summaries
FOOT = (74, 74, 74)          # footer text
SUB = (201, 210, 224)        # masthead subtitle
WHITE = (255, 255, 255)

SIZE = 1024
CARD_W, CARD_H = 478, 216
CARD_X = (24, 522)
CARD_Y = (182, 414, 646)
TEXT_X = 42
TEXT_W = 442

STORIES = [
    ("US \u2022 TRADE", (14, 124, 123),
     "US proposes 25% tariffs on Indian goods",
     "Washington floats a 25% levy, possibly 17% if a trade deal is "
     "reached, citing market access and labour rules."),
    ("CHINA \u2022 SPACE", (166, 58, 31),
     "First Pakistani astronaut reaches Tiangong",
     "Muhammad Zeeshan Ali joins the Shenzhou-24 mission, the first "
     "foreign astronaut aboard the Chinese station."),
    ("EGYPT \u2022 DISASTER", (166, 28, 46),
     "Fuel tanker fire on Cairo ring road kills at least 31",
     "A petroleum truck overturns and explodes above a tunnel in Giza's "
     "Warraq district; 21 are injured and 27 vehicles burn."),
    ("ISRAEL \u2022 COURTS", (29, 78, 216),
     "Judges urge dropping Netanyahu bribery case",
     "The Jerusalem court tells prosecutors to drop Case 4000 and rethink "
     "Case 2000; the recommendation is not a ruling."),
    ("US \u2022 MARKETS", (109, 40, 217),
     "US stocks slide as AI fears deepen",
     "Indexes fall further, the Nasdaq off almost 4%, as worries over AI "
     "spending and valuations grow."),
    ("NORTH KOREA \u2022 DIPLOMACY", (22, 101, 52),
     "North Korea shuts Swiss office in Pyongyang",
     "Pyongyang expels a Swiss diplomat and orders the newly opened office "
     "closed after a sanctions row."),
]

ALSO_ITEMS = ("Bangladesh raises garment wage 36%  \u2022  "
              "India-China border talks  \u2022  Flipkart CEO to step down")
FOOTER = ("26 NOVEMBER 2026  \u2022  Sources: Reuters / AP / CNN / "
          "Mathrubhumi  \u2022  Original infographic")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns the lines that fit in max_width."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_globe(draw, cx, cy, radius):
    """Gold wireframe globe: outer ring, meridian, parallel, equator."""
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius),
                 outline=GOLD, width=3)
    draw.ellipse((cx - 20, cy - radius, cx + 20, cy + radius),
                 outline=GOLD, width=2)
    draw.ellipse((cx - radius, cy - 25, cx + radius, cy + 25),
                 outline=GOLD, width=2)
    draw.rectangle((cx - radius, cy, cx + radius, cy + 1), fill=GOLD)


def draw_card(draw, x, y, kicker, accent, headline, summary, fonts):
    kicker_f, head_f, sum_f = fonts
    draw.rounded_rectangle((x, y, x + CARD_W, y + CARD_H),
                           radius=12, fill=WHITE)
    # Accent bar across the top: rounded top corners, square bottom.
    draw.rounded_rectangle((x, y, x + CARD_W, y + 14),
                           radius=7, fill=accent)
    draw.rectangle((x, y + 8, x + CARD_W, y + 14), fill=accent)
    draw.text((x + 18, y + 26), kicker, font=kicker_f, fill=accent)
    head_lines = wrap(draw, headline, head_f, TEXT_W)[:2]
    hy = y + 58
    for line in head_lines:
        draw.text((x + 18, hy), line, font=head_f, fill=INK)
        hy += 35
    sum_lines = wrap(draw, summary, sum_f, TEXT_W)[:3]
    sy = y + 134
    for line in sum_lines:
        draw.text((x + 18, sy), line, font=sum_f, fill=BODY)
        sy += 23


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead: navy band, gold rule, title, globe, date, subtitle.
    draw.rectangle((0, 0, SIZE, 147), fill=NAVY)
    draw.rectangle((0, 148, SIZE, 154), fill=GOLD)
    draw.text((28, 20), "THE WORLD IN ONE IMAGE",
              font=font("DejaVuSerif-Bold.ttf", 48), fill=WHITE)
    draw_globe(draw, 930, 74, 46)
    draw.text((28, 86), "THURSDAY, 26 NOVEMBER 2026",
              font=font("DejaVuSans-Bold.ttf", 28), fill=GOLD)
    draw.text((28, 120), "Six stories that defined the day",
              font=font("DejaVuSerif.ttf", 22), fill=SUB)

    # Story grid: 2 columns x 3 rows.
    fonts = (font("DejaVuSans-Bold.ttf", 19),
             font("DejaVuSerif-Bold.ttf", 28),
             font("DejaVuSans.ttf", 18))
    for i, (kicker, accent, headline, summary) in enumerate(STORIES):
        x = CARD_X[i % 2]
        y = CARD_Y[i // 2]
        draw_card(draw, x, y, kicker, accent, headline, summary, fonts)

    # ALSO strip.
    draw.rounded_rectangle((24, 878, 1000, 924), radius=10, fill=NAVY)
    draw.text((42, 890), "ALSO", font=font("DejaVuSans-Bold.ttf", 21),
              fill=WHITE)
    draw.text((120, 892), ALSO_ITEMS, font=font("DejaVuSans.ttf", 18),
              fill=WHITE)

    # Footer.
    draw.text((24, 940), FOOTER, font=font("DejaVuSans.ttf", 16),
              fill=FOOT)
    return img


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("entry.png")
    build().save(out, format="PNG")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
