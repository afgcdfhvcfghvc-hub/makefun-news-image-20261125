#!/usr/bin/env python3
"""Render the 25 Nov 2026 world-news infographic (1024x1024 PNG).

All artwork is drawn here with PIL primitives - no downloaded images.
Fonts: DejaVu Sans (installed system font).
Story list, sources and date evidence: see SOURCES.md in this repo.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fb(sz):
    return ImageFont.truetype(BOLD, sz)

def fr(sz):
    return ImageFont.truetype(REG, sz)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
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

def text(draw, xy, s, font, fill, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)

def rrect(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

# ---------------- palette ----------------
NAVY = (11, 31, 58)
NAVY2 = (16, 46, 84)
GOLD = (255, 196, 0)
CREAM = (250, 246, 236)
INK = (18, 24, 33)
GREY = (92, 102, 118)
WHITE = (255, 255, 255)
RED = (198, 40, 40)
ORANGE = (230, 92, 0)
BLUE = (18, 96, 196)
TEAL = (0, 130, 130)
GREEN = (28, 140, 70)
PURPLE = (110, 60, 170)
BROWN = (140, 90, 40)
ME = (198, 40, 40)      # Middle East / Africa - red
APAC = (18, 96, 196)    # Asia-Pacific - blue
EU = (0, 130, 130)      # Europe - teal
AM = (28, 140, 70)      # Americas - green
WORLD = (110, 60, 170)  # World / tech / sport - purple

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---------------- header ----------------
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 112, W, 116], fill=GOLD)
text(d, (24, 14), "ONE DAY  •  ONE IMAGE  •  THE WORLD", fb(15), GOLD)
text(d, (24, 34), "THE WORLD IN ONE DAY", fb(46), WHITE)
text(d, (24, 84), "WEDNESDAY  25  NOVEMBER  2026", fb(26), GOLD)
# right chip
rrect(d, [742, 18, 1000, 100], 10, fill=(255, 255, 255))
text(d, (871, 26), "33 STORIES", fb(26), NAVY, anchor="ma")
text(d, (871, 56), "ALL VERIFIED", fb(17), RED, anchor="ma")
text(d, (871, 76), "25 NOV 2026", fb(14), GREY, anchor="ma")

# ---------------- feature cards ----------------
def badge(draw, x, y, kind):
    col = {"CONFIRMED": (28, 140, 70), "OFFICIAL": (18, 96, 196),
           "REPORTED": (190, 120, 0)}[kind]
    w = 12 + draw.textlength(kind, font=fb(11)) + 12
    rrect(draw, [x, y, x + w, y + 20], 10, fill=col)
    text(draw, (x + 12, y + 3), kind, fb(11), WHITE)
    return w

def feature(x, y, w, h, accent, kicker, headline, sub, source, badge_kind, art):
    rrect(d, [x, y, x + w, y + h], 12, fill=WHITE, outline=accent, width=3)
    d.rectangle([x, y, x + w, y + 8], fill=accent)
    text(d, (x + 14, y + 16), kicker, fb(14), accent)
    art(x + 14, y + 42, 84, 72)
    lines = wrap(d, headline, fb(23), w - 128)
    yy = y + 42
    for ln in lines[:4]:
        text(d, (x + 108, yy), ln, fb(23), INK)
        yy += 26
    sub_lines = wrap(d, sub, fr(15), w - 28)
    yy = y + 150
    for ln in sub_lines[:2]:
        text(d, (x + 14, yy), ln, fr(15), (50, 58, 72))
        yy += 19
    bw = badge(d, x + 14, y + h - 30, badge_kind)
    text(d, (x + 14 + bw + 8, y + h - 27), source, fr(13), GREY)

def art_tariff(x, y, w, h):
    # globe with % sign
    d.ellipse([x, y, x + w, y + h], fill=(18, 96, 196), outline=NAVY, width=3)
    d.arc([x + 8, y + 6, x + w - 8, y + h - 6], 200, 340, fill=WHITE, width=4)
    d.arc([x + 8, y + 6, x + w - 8, y + h - 6], 20, 160, fill=WHITE, width=4)
    d.line([x + w // 2, y + 4, x + w // 2, y + h - 4], fill=WHITE, width=4)
    text(d, (x + w - 26, y + h - 32), "%", fb(28), RED)

def art_rocket(x, y, w, h):
    # rocket + flame + Pakistan-green flag
    d.polygon([(x + 46, y + 2), (x + 66, y + 34), (x + 58, y + 66), (x + 34, y + 66),
               (x + 26, y + 34)], fill=(230, 92, 0), outline=NAVY, width=2)
    d.ellipse([x + 40, y + 30, x + 52, y + 48], fill=WHITE, outline=NAVY, width=2)
    d.polygon([(x + 26, y + 52), (x + 10, y + 72), (x + 28, y + 66)], fill=RED)
    d.polygon([(x + 66, y + 52), (x + 82, y + 72), (x + 64, y + 66)], fill=RED)
    d.polygon([(x + 40, y + 66), (x + 46, y + 76), (x + 52, y + 66)], fill=GOLD)
    # small stars
    for sx, sy in [(x + 4, y + 8), (x + 84, y + 14), (x + 88, y + 60)]:
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=GOLD)

def art_blast(x, y, w, h):
    # explosion starburst over a tanker/ship
    cx, cy = x + 46, y + 30
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        r = 34 if i % 2 == 0 else 16
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(255, 140, 0), outline=RED, width=2)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=GOLD)
    # ship hull
    d.polygon([(x + 6, y + 58), (x + 88, y + 58), (x + 78, y + 74), (x + 16, y + 74)],
              fill=NAVY)
    d.rectangle([x + 30, y + 44, x + 62, y + 58], fill=RED)
    d.line([x + 46, y + 30, x + 46, y + 44], fill=NAVY, width=3)

FX, FY, FW, FH = 24, 128, 320, 224
feature(FX, FY, FW, FH, RED, "TOP STORY 1 - TRADE WAR",
        "TRUMP'S NEW TARIFFS HIT 14 PARTNERS",
        "China faces 20% in new 'overcapacity' duties; EU, Japan and Korea hit too.",
        "Reuters / Al Jazeera", "CONFIRMED", art_tariff)
feature(FX + 328, FY, FW, FH, BLUE, "TOP STORY 2 - SPACE",
        "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
        "Shenzhou-24 docks at Tiangong. Ali, 40, is the first foreign guest aboard.",
        "Reuters / Dawn / Al Jazeera", "CONFIRMED", art_rocket)
feature(FX + 656, FY, FW, FH, ORANGE, "TOP STORY 3 - WAR AT SEA",
        "HODEIDAH HIT; TANKERS BURN",
        "Saudi coalition bombs Yemen's port. Iran says tankers hit mines.",
        "CNA / Reuters / IRNA", "CONFIRMED", art_blast)

# ---------------- big numbers strip ----------------
NY, NH = 352, 58
d.rectangle([0, NY, W, NY + NH], fill=NAVY2)
nums = [
    ("-6.16%", "KOSPI CRASHES", GOLD),
    ("14", "PARTNERS TARIFFED", WHITE),
    ("30", "KILLED, CAIRO FIRE", WHITE),
    ("19", "KILLED, SUDAN DRONES", WHITE),
    ("A$740m", "SOLOMONS PACT", GOLD),
]
cw = W // 5
for i, (n, lab, col) in enumerate(nums):
    x0 = i * cw
    if i:
        d.line([x0, NY + 10, x0, NY + NH - 10], fill=(90, 110, 140), width=2)
    text(d, (x0 + cw // 2, NY + 6), n, fb(27), col, anchor="ma")
    text(d, (x0 + cw // 2, NY + 38), lab, fb(12), (200, 210, 225), anchor="ma")

# ---------------- map band ----------------
MY, MH = 410, 152
d.rectangle([0, MY, W, MY + MH], fill=(232, 240, 248))
text(d, (24, MY + 8), "WHERE IT HAPPENED", fb(16), NAVY)
# simplified continents (equirectangular lon -170..190 -> x 24..620, lat 75..-55 -> y)
def mp(lon, lat):
    x = 24 + (lon + 170) / 360 * 596
    y = MY + 34 + (75 - lat) / 130 * 112
    return (x, y)

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
    # South America
    [(-80, 10), (-62, 9), (-52, 5), (-40, -5), (-35, -10), (-40, -22),
     (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -40),
     (-73, -20), (-80, -3), (-80, 10)],
    # Africa
    [(-17, 15), (-10, 30), (10, 37), (20, 32), (32, 31), (43, 12),
     (51, 11), (48, -2), (40, -15), (35, -28), (20, -35), (12, -18),
     (9, -1), (-8, 4), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (18, 56),
     (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 50), (30, 45),
     (28, 40), (23, 36), (12, 38), (3, 38), (-10, 36)],
    # Asia
    [(45, 68), (60, 70), (75, 73), (100, 77), (130, 72), (160, 70),
     (178, 65), (162, 60), (158, 52), (142, 45), (135, 35), (127, 33),
     (120, 25), (108, 18), (105, 9), (98, 8), (92, 16), (88, 22), (80, 13),
     (77, 8), (72, 20), (66, 25), (60, 25), (52, 28), (48, 30), (44, 39),
     (40, 42), (45, 68)],
    # Australia
    [(114, -22), (114, -32), (124, -33), (132, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (126, -14), (114, -22)],
]
for poly in CONTINENTS:
    d.polygon([mp(lo, la) for lo, la in poly], fill=(176, 200, 220),
              outline=(90, 120, 150), width=1)

# (number, lon, lat, colour, badge offset dx, dy) - badges offset with a
# leader line where pins cluster (Hodeidah / Gaza / Cairo / Sudan).
PINS = [
    (1, 43, 15, RED, -46, 6),
    (2, 56, 26, ORANGE, 20, -18),
    (3, 34, 31, RED, -40, -18),
    (4, 31, 30, ORANGE, 28, 14),
    (5, 33, 11, RED, -2, 32),
    (6, 127, 37, BLUE, 0, -20),
    (7, 100, 40, BLUE, 0, -20),
    (8, 149, -35, TEAL, 0, -20),
]
for n, lon, lat, col, dx, dy in PINS:
    x, y = mp(lon, lat)
    bx, by = x + dx, y + dy
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=col, outline=WHITE, width=1)
    d.line([x, y, bx, by], fill=col, width=2)
    d.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=col, outline=WHITE, width=2)
    text(d, (bx, by - 8), str(n), fb(12), WHITE, anchor="ma")

# pin legend (right of map)
LX = 648
text(d, (LX, MY + 8), "MAP KEY", fb(16), NAVY)
LEGEND = [
    ("1", "Hodeidah, Yemen - port struck", RED),
    ("2", "Strait of Hormuz - tankers mined", ORANGE),
    ("3", "Gaza City - Hamas chief killed", RED),
    ("4", "Cairo - fuel fire, 30 killed", ORANGE),
    ("5", "Damazin, Sudan - 19 killed", RED),
    ("6", "Seoul - KOSPI -6.16%", BLUE),
    ("7", "Jiuquan, China - rocket launch", BLUE),
    ("8", "Canberra - Solomons treaty", TEAL),
]
yy = MY + 28
for n, lab, col in LEGEND:
    d.ellipse([LX, yy, LX + 18, yy + 18], fill=col, outline=WHITE, width=1)
    text(d, (LX + 9, yy + 2), n, fb(12), WHITE, anchor="ma")
    text(d, (LX + 24, yy + 2), lab, fr(12), INK)
    yy += 15

# ---------------- UTC timeline ----------------
TY, TH = 562, 52
d.rectangle([0, TY, W, TY + TH], fill=WHITE)
text(d, (24, TY + 16), "UTC", fb(15), NAVY)
text(d, (24, TY + 32), "TIMELINE", fb(15), NAVY)
tl_x0, tl_x1 = 210, 990
d.line([tl_x0, TY + 18, tl_x1, TY + 18], fill=NAVY, width=3)
TIMES = [
    ("00:18", "Launch"),
    ("03:56", "Docked"),
    ("~06:00", "Hodeidah hit"),
    ("09:09", "Sidecar trips"),
    ("15:30", "KOSPI -6.16%"),
    ("Evening", "Tariffs announced"),
]
for i, (t, lab) in enumerate(TIMES):
    x = tl_x0 + i * (tl_x1 - tl_x0) / 5
    d.ellipse([x - 6, TY + 12, x + 6, TY + 24], fill=RED, outline=WHITE, width=2)
    anch = "ma"
    if i == 0:
        anch = "la"
        x = tl_x0
    if i == len(TIMES) - 1:
        anch = "ra"
        x = tl_x1
    text(d, (x, TY + 27), t, fb(12), RED, anchor=anch)
    text(d, (x, TY + 40), lab, fr(11), INK, anchor=anch)
d.line([0, TY + TH - 1, W, TY + TH - 1], fill=(200, 205, 215), width=1)

# ---------------- story grid: 30 more stories, 5 region columns ----------------
GY, GH = 618, 318
COLS = [
    ("MIDDLE EAST & AFRICA", ME),
    ("ASIA-PACIFIC", APAC),
    ("EUROPE", EU),
    ("AMERICAS", AM),
    ("WORLD / TECH / SPORT", WORLD),
]
colw = (W - 48) / 5
for i, (name, col) in enumerate(COLS):
    x0 = 24 + i * colw
    d.rectangle([x0, GY, x0 + colw - 8, GY + 20], fill=col)
    text(d, (x0 + 6, GY + 3), name, fb(12), WHITE)

def icon(draw, kind, x, y, col):
    """Tiny 24x24 drawn glyph at (x, y)."""
    s = 24
    if kind == "blast":
        pts = []
        for i in range(12):
            ang = i * math.pi / 6
            r = 11 if i % 2 == 0 else 5
            pts.append((x + 12 + r * math.cos(ang), y + 12 + r * math.sin(ang)))
        draw.polygon(pts, fill=(255, 140, 0), outline=col, width=1)
    elif kind == "ship":
        draw.polygon([(x + 2, y + 14), (x + 22, y + 14), (x + 19, y + 21),
                      (x + 5, y + 21)], fill=col)
        draw.rectangle([x + 8, y + 6, x + 16, y + 14], fill=RED)
    elif kind == "flame":
        draw.polygon([(x + 12, y + 2), (x + 19, y + 12), (x + 16, y + 20),
                      (x + 8, y + 20), (x + 5, y + 12)], fill=(255, 140, 0),
                     outline=RED, width=1)
        draw.ellipse([x + 9, y + 13, x + 15, y + 19], fill=GOLD)
    elif kind == "drone":
        draw.ellipse([x + 3, y + 3, x + 9, y + 9], fill=col)
        draw.ellipse([x + 15, y + 3, x + 21, y + 9], fill=col)
        draw.ellipse([x + 3, y + 15, x + 9, y + 21], fill=col)
        draw.ellipse([x + 15, y + 15, x + 21, y + 21], fill=col)
        draw.rectangle([x + 9, y + 9, x + 15, y + 15], fill=INK)
    elif kind == "chart":
        draw.line([(x + 2, y + 6), (x + 9, y + 10), (x + 15, y + 8), (x + 22, y + 20)],
                  fill=RED, width=3)
        draw.polygon([(x + 22, y + 20), (x + 18, y + 20), (x + 22, y + 16)], fill=RED)
    elif kind == "treaty":
        draw.rectangle([x + 4, y + 3, x + 20, y + 21], fill=WHITE, outline=col, width=2)
        draw.line([x + 7, y + 8, x + 17, y + 8], fill=col, width=2)
        draw.line([x + 7, y + 13, x + 17, y + 13], fill=col, width=2)
        draw.line([x + 7, y + 18, x + 13, y + 18], fill=col, width=2)
    elif kind == "coin":
        draw.ellipse([x + 3, y + 3, x + 21, y + 21], fill=GOLD, outline=BROWN, width=2)
        draw.text((x + 12, y + 5), "$", font=fb(14), fill=BROWN, anchor="ma")
    elif kind == "chip":
        draw.rectangle([x + 5, y + 5, x + 19, y + 19], fill=col)
        draw.rectangle([x + 9, y + 9, x + 15, y + 15], fill=WHITE)
        for px in (8, 12, 16):
            draw.line([x + px, y + 1, x + px, y + 5], fill=col, width=2)
            draw.line([x + px, y + 19, x + px, y + 23], fill=col, width=2)
    elif kind == "smile":
        draw.ellipse([x + 2, y + 2, x + 22, y + 22], outline=col, width=2)
        draw.ellipse([x + 8, y + 8, x + 10, y + 10], fill=col)
        draw.ellipse([x + 14, y + 8, x + 16, y + 10], fill=col)
        draw.arc([x + 6, y + 11, x + 18, y + 20], 20, 160, fill=col, width=2)
    elif kind == "eye":
        draw.ellipse([x + 2, y + 8, x + 22, y + 16], outline=col, width=2)
        draw.ellipse([x + 9, y + 9, x + 15, y + 15], fill=col)
    elif kind == "train":
        draw.rectangle([x + 4, y + 3, x + 20, y + 19], fill=col)
        draw.rectangle([x + 7, y + 6, x + 11, y + 10], fill=WHITE)
        draw.rectangle([x + 13, y + 6, x + 17, y + 10], fill=WHITE)
        draw.line([x + 2, y + 22, x + 22, y + 22], fill=INK, width=2)
    elif kind == "ban":
        draw.ellipse([x + 2, y + 2, x + 22, y + 22], outline=RED, width=3)
        draw.line([x + 5, y + 5, x + 19, y + 19], fill=RED, width=3)
    elif kind == "doc":
        draw.rectangle([x + 5, y + 2, x + 19, y + 22], fill=WHITE, outline=col, width=2)
        draw.line([x + 8, y + 7, x + 16, y + 7], fill=col, width=2)
        draw.line([x + 8, y + 12, x + 16, y + 12], fill=col, width=2)
    elif kind == "plane":
        draw.polygon([(x + 2, y + 13), (x + 12, y + 10), (x + 22, y + 4),
                      (x + 20, y + 12), (x + 14, y + 15), (x + 12, y + 21),
                      (x + 10, y + 15), (x + 4, y + 16)], fill=col)
    elif kind == "flag":
        draw.rectangle([x + 3, y + 3, x + 21, y + 15], fill=col)
        draw.rectangle([x + 3, y + 15, x + 21, y + 15], fill=WHITE)
        draw.line([x + 3, y + 3, x + 3, y + 22], fill=INK, width=2)
    elif kind == "jet":
        draw.polygon([(x + 2, y + 12), (x + 10, y + 9), (x + 22, y + 3),
                      (x + 19, y + 11), (x + 13, y + 14), (x + 12, y + 20),
                      (x + 9, y + 14), (x + 4, y + 15)], fill=TEAL)
    elif kind == "medal":
        draw.ellipse([x + 6, y + 10, x + 18, y + 22], fill=GOLD, outline=BROWN, width=2)
        draw.polygon([(x + 6, y + 10), (x + 10, y + 2), (x + 14, y + 2),
                      (x + 18, y + 10)], fill=RED)
        draw.text((x + 12, y + 13), "1", font=fb(10), fill=BROWN, anchor="ma")
    elif kind == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = 11 if i % 2 == 0 else 5
            pts.append((x + 12 + r * math.cos(ang), y + 12 + r * math.sin(ang)))
        draw.polygon(pts, fill=GOLD, outline=BROWN, width=1)
    elif kind == "shield":
        draw.polygon([(x + 12, y + 2), (x + 21, y + 6), (x + 21, y + 13),
                      (x + 12, y + 22), (x + 3, y + 13), (x + 3, y + 6)],
                     fill=col, outline=NAVY, width=1)
    elif kind == "storm":
        draw.ellipse([x + 3, y + 7, x + 13, y + 15], fill=GREY)
        draw.ellipse([x + 10, y + 4, x + 21, y + 15], fill=(150, 160, 175))
        draw.line([x + 8, y + 17, x + 6, y + 22], fill=BLUE, width=2)
        draw.line([x + 14, y + 17, x + 12, y + 22], fill=BLUE, width=2)
    elif kind == "capture":
        draw.ellipse([x + 3, y + 8, x + 10, y + 15], outline=INK, width=2)
        draw.ellipse([x + 14, y + 8, x + 21, y + 15], outline=INK, width=2)
        draw.line([x + 10, y + 11, x + 14, y + 11], fill=INK, width=2)
    elif kind == "pope":
        draw.ellipse([x + 4, y + 2, x + 20, y + 18], fill=GOLD, outline=BROWN, width=2)
        draw.ellipse([x + 9, y + 7, x + 15, y + 13], fill=WHITE)
    elif kind == "guitar":
        draw.ellipse([x + 8, y + 10, x + 21, y + 22], fill=BROWN, outline=INK, width=1)
        draw.line([x + 9, y + 11, x + 3, y + 4], fill=BROWN, width=4)
        draw.ellipse([x + 12, y + 14, x + 17, y + 19], fill=INK)
    elif kind == "museum":
        draw.rectangle([x + 3, y + 3, x + 21, y + 7], fill=col)
        for px in (5, 10, 15):
            draw.line([x + px, y + 8, x + px, y + 19], fill=col, width=2)
        draw.line([x + 3, y + 20, x + 21, y + 20], fill=col, width=2)
    elif kind == "talk":
        draw.ellipse([x + 3, y + 3, x + 21, y + 15], outline=col, width=2)
        draw.polygon([(x + 8, y + 15), (x + 6, y + 21), (x + 12, y + 15)], fill=col)
        draw.line([x + 7, y + 8, x + 17, y + 8], fill=col, width=2)
        draw.line([x + 7, y + 12, x + 15, y + 12], fill=col, width=2)
    elif kind == "ball":
        draw.ellipse([x + 2, y + 2, x + 22, y + 22], fill=(230, 92, 0), outline=INK, width=2)
        draw.line([x + 12, y + 2, x + 12, y + 22], fill=INK, width=2)
        draw.arc([x + 2, y + 6, x + 22, y + 18], 270, 90, fill=INK, width=2)

# (headline, source, badge, icon) - headlines kept under ~32 chars so
# they fit on two lines at 14px in a 155px column.
GRID = [
    [("Gaza: Hamas security chief killed", "Reuters / Xinhua", "CONFIRMED", "blast"),
     ("Houthis claim Ras Tanura hit", "Al Jazeera", "REPORTED", "flame"),
     ("LNG tanker hits mine in Hormuz", "Arab News", "REPORTED", "ship"),
     ("Sudan: RSF drones kill 19", "Reuters", "CONFIRMED", "drone"),
     ("Cairo fuel fire kills 30", "Al Jazeera", "CONFIRMED", "flame"),
     ("Nigeria: militants kill 30", "Reports", "REPORTED", "blast")],
    [("KOSPI -6.16%; Samsung -9.9%", "Yonhap", "CONFIRMED", "chart"),
     ("Solomons picks Australia", "Nikkei", "CONFIRMED", "treaty"),
     ("Bangladesh wage up 36%", "Reuters", "CONFIRMED", "coin"),
     ("Japan aims for No. 3 in AI", "Reports", "REPORTED", "chip"),
     ("Taiwan comic defies China", "Reuters", "REPORTED", "smile"),
     ("No proof China ordered spying", "SCMP", "REPORTED", "eye")],
    [("Eurostar strike cancels trains", "Eurostar / AP", "CONFIRMED", "train"),
     ("Denmark bans headscarves", "SCMP", "REPORTED", "ban"),
     ("Burnham vows to end NDAs", "SCMP", "REPORTED", "doc"),
     ("Poland plans eastern no-fly zone", "Reports", "REPORTED", "plane"),
     ("France to Putin: drop delusion", "Reports", "REPORTED", "flag"),
     ("Ukraine gets Gripen jets in Jan", "Reports", "REPORTED", "jet")],
    [("Giuliani gets top US honour", "SCMP", "REPORTED", "medal"),
     ("US soldier sold secrets to China", "SCMP", "REPORTED", "star"),
     ("Colombia hostages freed", "SCMP", "REPORTED", "shield"),
     ("Macy's parade hit by storm", "SCMP", "REPORTED", "storm"),
     ("US Army blasts explosives in Iowa", "SCMP", "REPORTED", "blast"),
     ("Mexico catches 'El Chapo Isidro'", "Reports", "REPORTED", "capture")],
    [("Pope: COP31 failure 'troubling'", "AP / Reuters", "CONFIRMED", "pope"),
     ("Andy Taylor of Duran Duran dies", "AP / Sky", "REPORTED", "guitar"),
     ("Nvidia's Huang 'in therapy'", "SCMP", "REPORTED", "chip"),
     ("London Museum reopens", "Reuters", "REPORTED", "museum"),
     ("Ecuador, US weigh joint drills", "Reports", "REPORTED", "talk"),
     ("Lakers beat Jazz; Doncic 28", "Reuters", "REPORTED", "ball")],
]

row_h = (GH - 22) / 6
for ci, col_items in enumerate(GRID):
    x0 = 24 + ci * colw
    col = COLS[ci][1]
    for ri, (head, src, bdg, ic) in enumerate(col_items):
        y0 = GY + 22 + ri * row_h
        icon(d, ic, x0 + 2, y0 + 4, col)
        lines = wrap(d, head, fb(14), colw - 40)
        yy = y0 + 2
        for ln in lines[:2]:
            text(d, (x0 + 30, yy), ln, fb(14), INK)
            yy += 16
        bcol = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": (190, 120, 0)}[bdg]
        text(d, (x0 + 30, y0 + 34), bdg, fb(10), bcol)
        text(d, (x0 + 30 + d.textlength(bdg, font=fb(10)) + 6, y0 + 34), src, fr(10), GREY)
        if ri < 5:
            d.line([x0, y0 + row_h - 2, x0 + colw - 10, y0 + row_h - 2],
                   fill=(215, 220, 228), width=1)

# ---------------- footer: DATE CHECK + legend ----------------
FY = 940
d.rectangle([0, FY, W, H], fill=NAVY)
d.rectangle([0, FY, W, FY + 3], fill=GOLD)
rrect(d, [20, FY + 10, 648, FY + 76], 8, outline=GOLD, width=2)
text(d, (32, FY + 15), "DATE CHECK - ONLY 25 NOV 2026", fb(14), GOLD)
text(d, (32, FY + 34), "EXCLUDED on purpose: Riyadh tower strike (24 Nov) - Huawei verdict (24 Nov) -",
     fr(12), WHITE)
text(d, (32, FY + 50), "Sinner surgery (announced 24 Nov) - CIA breach (first reported 24 Nov).",
     fr(12), WHITE)
text(d, (664, FY + 12), "BADGES: CONFIRMED = 2+ outlets", fb(12), WHITE)
text(d, (664, FY + 30), "REPORTED = 1 outlet. Sources: Reuters, AP, AFP,", fr(12), (200, 210, 225))
text(d, (664, FY + 46), "Al Jazeera, Yonhap, Dawn, SCMP, Xinhua, CNA, IRNA.", fr(12), (200, 210, 225))
text(d, (664, FY + 64), "Every story: 25 Nov 2026 only.", fr(12), GOLD)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
