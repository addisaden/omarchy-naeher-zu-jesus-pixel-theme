#!/usr/bin/env python3
"""Pixel-Art-Generator für das Omarchy-Theme "Näher zu Jesus — Pixel".
Zeichnet in niedriger Auflösung und schreibt PPM-Dateien; das Hochskalieren
(nearest neighbour) erledigt ImageMagick."""
import math
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)


def hx(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


NAVY = hx("#0B1426")
NAVY2 = hx("#13203C")
MID = hx("#1A2A4A")
MID2 = hx("#2E3F63")
PURPLE = hx("#5C2A4D")
RUST = hx("#A23B2A")
ORANGE = hx("#E85D04")
GOLD = hx("#F4A261")
SGOLD = hx("#FFD166")
CREAM = hx("#FFF1C9")
LBLUE = hx("#90CAF9")
WHITE = hx("#FFFFFF")
GRAY = hx("#E0E0E0")
DGRAY = hx("#7A89A8")
GREEN = hx("#7CE38B")
BLACK = hx("#060A14")

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def ramp(colors, t, x, y):
    """Geordnetes Dithering zwischen zwei Nachbarfarben einer Rampe."""
    t = max(0.0, min(len(colors) - 1.0, t))
    i = int(t)
    if i >= len(colors) - 1:
        return colors[-1]
    frac = t - i
    return colors[i + 1] if frac * 16 > BAYER[y % 4][x % 4] + 0.5 else colors[i]


class Canvas:
    def __init__(self, w, h, bg=NAVY):
        self.w, self.h = w, h
        self.px = [[bg] * w for _ in range(h)]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def sprite(self, rows, x, y, c, scale=1):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "#":
                    self.rect(x + i * scale, y + j * scale, scale, scale, c)

    def save(self, name):
        with open(OUT / name, "wb") as f:
            f.write(f"P6 {self.w} {self.h} 255\n".encode())
            f.write(bytes(v for row in self.px for p in row for v in p))


# --- 5x7-Font mit Akzentzeile (Umlaute) -----------------------------------
F = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#",
    "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".###.|#...#|#....|#....|#....|#...#|.###.",
    "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####",
    "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".###.|#...#|#....|#.###|#...#|#...#|.####",
    "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": ".###.|..#..|..#..|..#..|..#..|..#..|.###.",
    "J": "..###|...#.|...#.|...#.|#..#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
    "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
    "N": "#...#|#...#|##..#|#.#.#|#..##|#...#|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
    "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.",
    "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
    "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|#.#.#|.#.#.",
    "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
    "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.",
    "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    "2": ".###.|#...#|....#|...#.|..#..|.#...|#####",
    "3": "####.|....#|....#|.###.|....#|....#|####.",
    "4": "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.",
    "5": "#####|#....|####.|....#|....#|#...#|.###.",
    "6": "..##.|.#...|#....|####.|#...#|#...#|.###.",
    "7": "#####|....#|...#.|..#..|.#...|.#...|.#...",
    "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.",
    "9": ".###.|#...#|#...#|.####|....#|...#.|.##..",
    " ": ".....|.....|.....|.....|.....|.....|.....",
    ".": ".....|.....|.....|.....|.....|.....|..#..",
    ",": ".....|.....|.....|.....|.....|..#..|.#...",
    ":": ".....|.....|..#..|.....|.....|..#..|.....",
    "-": ".....|.....|.....|.###.|.....|.....|.....",
    "_": ".....|.....|.....|.....|.....|.....|#####",
    "/": "....#|....#|...#.|..#..|.#...|#....|#....",
    ">": "#....|.#...|..#..|...#.|..#..|.#...|#....",
    "<": "....#|...#.|..#..|.#...|..#..|...#.|....#",
    "[": ".###.|.#...|.#...|.#...|.#...|.#...|.###.",
    "]": ".###.|...#.|...#.|...#.|...#.|...#.|.###.",
    "(": "...#.|..#..|.#...|.#...|.#...|..#..|...#.",
    ")": ".#...|..#..|...#.|...#.|...#.|..#..|.#...",
    "+": ".....|..#..|..#..|#####|..#..|..#..|.....",
    "=": ".....|.....|#####|.....|#####|.....|.....",
    "$": "..#..|.####|#.#..|.###.|..#.#|####.|..#..",
    "!": "..#..|..#..|..#..|..#..|..#..|.....|..#..",
    "?": ".###.|#...#|....#|...#.|..#..|.....|..#..",
    "'": "..#..|..#..|.....|.....|.....|.....|.....",
    "@": ".###.|#...#|#.###|#.#.#|#.###|#....|.###.",
    "~": ".....|.....|.#...|#.#.#|...#.|.....|.....",
    "%": "##..#|##..#|...#.|..#..|.#...|#..##|#..##",
    "|": "..#..|..#..|..#..|..#..|..#..|..#..|..#..",
    "*": ".....|#.#.#|.###.|#####|.###.|#.#.#|.....",
    "#": "#####|#####|#####|#####|#####|#####|#####",
    "░": "#.#.#|.#.#.|#.#.#|.#.#.|#.#.#|.#.#.|#.#.#",
    "♥": ".....|.#.#.|#####|#####|.###.|..#..|.....",
    "▸": ".....|.#...|.##..|.###.|.##..|.#...|.....",
}
for u, base in (("Ä", "A"), ("Ö", "O"), ("Ü", "U")):
    F[u] = base
UMLAUT = {"Ä", "Ö", "Ü"}
GLYPH = {k: v.split("|") for k, v in F.items()}
for u in UMLAUT:
    GLYPH[u] = GLYPH[F[u]]


def text_width(s, scale=1):
    return len(s) * 6 * scale - scale


def text(cv, s, x, y, color, scale=1, shadow=None):
    """y ist die Oberkante der Akzentzeile; der Buchstabe beginnt 2 Zeilen tiefer."""
    for pass_, col, off in ((0, shadow, scale), (1, color, 0)):
        if col is None:
            continue
        cx = x
        for ch in s:
            c = col if not callable(col) else col(ch)
            if ch in UMLAUT:
                cv.sprite([".#.#."], cx + off, y + off, c, scale)
            cv.sprite(GLYPH.get(ch, GLYPH["?"]), cx + off, y + 2 * scale + off, c, scale)
            cx += 6 * scale


HEX = {
    "0": "###|#.#|#.#|#.#|###", "1": ".#.|##.|.#.|.#.|###",
    "2": "##.|..#|.#.|#..|###", "3": "##.|..#|.#.|..#|##.",
    "4": "#.#|#.#|###|..#|..#", "5": "###|#..|##.|..#|##.",
    "6": ".##|#..|###|#.#|###", "7": "###|..#|.#.|.#.|.#.",
    "8": "###|#.#|###|#.#|###", "9": "###|#.#|###|..#|##.",
    "A": ".#.|#.#|###|#.#|#.#", "B": "##.|#.#|##.|#.#|##.",
    "C": ".##|#..|#..|#..|.##", "D": "##.|#.#|#.#|#.#|##.",
    "E": "###|#..|##.|#..|###", "F": "###|#..|##.|#..|#..",
}
HEX = {k: v.split("|") for k, v in HEX.items()}

FOOT_L = ["##.#.#", "......", ".####.", "######", "######", ".#####", "..####", "..####", ".####.", ".###.."]
FOOT_R = [r[::-1] for r in FOOT_L]


def cross(cv, cx, top, h, arm, thick, y_arm, core=CREAM, edge=SGOLD):
    x0 = cx - thick // 2
    cv.rect(x0 - 1, top - 1, thick + 2, h + 2, edge)
    cv.rect(cx - arm // 2 - 1, y_arm - 1, arm + 2, thick + 2, edge)
    cv.rect(x0, top, thick, h, core)
    cv.rect(cx - arm // 2, y_arm, arm, thick, core)


# === 1) Pixel-Sonnenaufgang ================================================
def sunrise():
    W, H = 480, 300
    cv = Canvas(W, H)
    rnd = random.Random(316)
    horizon = 187
    cx, cy = 240, 77
    sky = [NAVY, NAVY2, MID, MID2, PURPLE, RUST, ORANGE, GOLD]
    ground = [PURPLE, MID, NAVY2, NAVY, BLACK]
    for y in range(H):
        for x in range(W):
            if y < horizon:
                t = (y / horizon) ** 1.7 * (len(sky) - 1)
                d = math.hypot((x - cx) / 1.2, y - cy)
                t += 3.2 * math.exp(-(d / 70) ** 2)
                t += 1.6 * math.exp(-((x - cx) / 150) ** 2) * (y / horizon) ** 3
                cv.set(x, y, ramp(sky, t, x, y))
            else:
                t = (y - horizon) / (H - horizon) * (len(ground) - 1) * 1.3
                t -= 0.8 * math.exp(-((x - cx) / 60) ** 2) * (1 - (y - horizon) / 40)
                cv.set(x, y, ramp(ground, t, x, y))
    # Sterne
    for _ in range(170):
        x, y = rnd.randrange(W), rnd.randrange(int(horizon * 0.55))
        if math.hypot(x - cx, y - cy) < 70 or (y < 40 and (x < 160 or x > 380)):
            continue
        cv.set(x, y, rnd.choice([WHITE, LBLUE, LBLUE, GRAY]))
    for x, y in [(52, 30), (410, 22), (350, 70), (120, 84), (445, 104), (30, 118)]:
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            cv.set(x + dx, y + dy, WHITE if (dx, dy) == (0, 0) else LBLUE)
    # Sonne am Horizont
    for y in range(horizon - 22, horizon):
        for x in range(cx - 40, cx + 41):
            r = math.hypot(x - cx, (y - horizon) * 1.0)
            if r < 22:
                cv.set(x, y, CREAM if r < 16 else ramp([ORANGE, SGOLD, CREAM], (22 - r) / 3, x, y))
    for i, x in enumerate(range(0, W)):  # Horizontlinie
        cv.set(x, horizon, GOLD if abs(x - cx) < 120 else RUST)
    # Kreuz mit Funken
    cross(cv, cx, 45, 72, 34, 5, 59)
    for _ in range(26):
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(24, 46)
        cv.set(int(cx + math.cos(a) * r * 1.3), int(cy + math.sin(a) * r), rnd.choice([SGOLD, CREAM, GOLD]))
    # Lichtpfad Kreuz -> Horizont
    for y in range(119, horizon - 22, 3):
        cv.set(cx + int(3 * math.sin(y / 6)), y, CREAM)
    # Fußspuren auf dem Boden (Perspektive: unten größer)
    steps = [(236, 192, 1, FOOT_L), (244, 206, 1, FOOT_R), (226, 222, 2, FOOT_L)]
    for x, y, s, spr in steps:
        cv.sprite(spr, x, y, SGOLD, s)
    # Titel
    title_col = lambda ch: None
    words = [("NÄHER ", WHITE), ("ZU ", LBLUE), ("JESUS", SGOLD)]
    total = sum(text_width(w, 2) + 2 for w, _ in words)
    x = (W - total) // 2
    for w, c in words:
        text(cv, w, x, 250, c, 2, shadow=BLACK)
        x += len(w) * 12
    # HUD
    text(cv, "LVL JOH 14,6", 20, 16, WHITE, shadow=BLACK)
    text(cv, "WEG ▸ WAHRHEIT ▸ LEBEN", 20, 26, GRAY, shadow=BLACK)
    hud = "STEP +1  ♥♥♥"
    text(cv, hud, W - text_width(hud) - 20, 16, SGOLD, shadow=BLACK)
    sub = "PRESS START TO FOLLOW"
    text(cv, sub, (W - text_width(sub)) // 2, 276, DGRAY)
    cv.save("sunrise.ppm")
    return cv


# === 2) Boot-Screen ========================================================
def boot():
    W, H = 960, 600
    cv = Canvas(W, H, hx("#0A1020"))
    OK = GREEN
    lines = [
        [("NÄHER-ZU-JESUS BIOS V3.16", WHITE), ("   (C) JOH 3,16", DGRAY)],
        [],
        [("CPU : HERZ, 1 KERN / 70X7 THREADS", GRAY), ("   MT 18,22", DGRAY)],
        [("RAM : 66 BÜCHER GELADEN ........... ", GRAY), ("OK", OK)],
        [("PRÜFE /DEV/GLAUBE ................ ", GRAY), ("OK", OK)],
        [],
        [("[  ", GRAY), ("OK", OK), ("  ] STARTED ", GRAY), ("WEG.SERVICE", LBLUE), ("         JOH 14,6", DGRAY)],
        [("[  ", GRAY), ("OK", OK), ("  ] STARTED ", GRAY), ("WAHRHEIT.SERVICE", LBLUE)],
        [("[  ", GRAY), ("OK", OK), ("  ] STARTED ", GRAY), ("LEBEN.SERVICE", LBLUE)],
        [("[  ", GRAY), ("OK", OK), ("  ] MOUNTED ", GRAY), ("/HOME/GNADE", LBLUE)],
        [("[  ", GRAY), ("OK", OK), ("  ] REACHED TARGET ", GRAY), ("NACHFOLGE.TARGET", SGOLD)],
        [],
        [("NAEHER@JESUS", GREEN), (":", GRAY), ("~", LBLUE), ("$ ", GRAY), ("SUDO PACMAN -S NACHFOLGE", WHITE)],
        [("HINWEIS: GNADE BRAUCHT KEIN SUDO.", GOLD), ("       EPH 2,8", DGRAY)],
        [(":: PAKETE (1)  NACHFOLGE-1:1.0-1", GRAY)],
        [(":: INSTALLATION FORTSETZEN? [J/N] ", GRAY), ("J", WHITE)],
        [("(1/1) INSTALLIERE NACHFOLGE  [", GRAY), ("##########", ORANGE), ("] 100%", GRAY)],
        [],
        [("NAEHER@JESUS", GREEN), (":", GRAY), ("~", LBLUE), ("$ ", GRAY), ("ECHO $ZIEL", WHITE)],
        [("EINEN SCHRITT NÄHER.", SGOLD)],
        [("NAEHER@JESUS", GREEN), (":", GRAY), ("~", LBLUE), ("$ ", GRAY), ("#", WHITE)],
    ]
    y = 64
    for segs in lines:
        x = 64
        for s, c in segs:
            text(cv, s, x, y, c, 2)
            x += len(s) * 12
        y += 22
    # ASCII-Kreuz aus Blöcken rechts
    art = [
        "....##....",
        "....##....",
        "##########",
        "##########",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
        "....##....",
    ]
    ox, oy = 730, 110
    for j, row in enumerate(art):
        for i, ch in enumerate(row):
            if ch == "#":
                col = ramp([SGOLD, GOLD, ORANGE], j / (len(art) - 1) * 2, i, j)
                text(cv, "#", ox + i * 18, oy + j * 26, col, 3)
    cap = "ICH BIN DER WEG."
    text(cv, cap, ox + (10 * 18 - text_width(cap, 2)) // 2, oy + 11 * 26 + 12, DGRAY, 2)
    cv.save("boot.ppm")


# === 3) Hexdump Joh 1,1 ====================================================
def hexdump():
    W, H = 480, 300
    cv = Canvas(W, H, hx("#080E1C"))
    verse = ("Im Anfang war das Wort, und das Wort war bei Gott, "
             "und Gott war das Wort. ").encode()
    cx, cy = 240, 128

    def in_cross(x, y):
        return (abs(x - cx) <= 16 and 45 <= y <= 262) or (abs(y - 101) <= 14 and abs(x - cx) <= 70)

    i = 0
    rnd = random.Random(11)
    for row, y in enumerate(range(36, H - 18, 6)):
        for col in range(40):
            b = verse[i % len(verse)]
            i += 1
            s = f"{b:02X}"
            x = col * 12
            glow = in_cross(x + 3, y + 2) or in_cross(x + 7, y + 2)
            if glow:
                d = math.hypot((x - cx) / 1.4, y - 101)
                c = ramp([CREAM, SGOLD, GOLD, ORANGE], d / 40, x, y)
            else:
                d = math.hypot(x + 4 - cx, y - 101)
                c = MID2 if d < 110 and rnd.random() < 0.5 else MID
                if rnd.random() < 0.03:
                    c = LBLUE
            for k, ch in enumerate(s):
                cv.sprite(HEX[ch], x + k * 4, y, c)
    cv.rect(0, 10, W, 17, BLACK)
    text(cv, "$ XXD JOHANNES_1_1.TXT", 14, 12, GREEN)
    right = "UTF-8 ▸ 0X4A 0X45 0X53 0X55 0X53"
    text(cv, right, W - text_width(right) - 14, 12, DGRAY)
    cv.rect(0, H - 16, W, 16, BLACK)
    text(cv, "IM ANFANG WAR DAS WORT.", 14, H - 15, SGOLD)
    tag = "NÄHER ZU JESUS"
    text(cv, tag, W - text_width(tag) - 14, H - 15, LBLUE)
    cv.save("hex.ppm")


# === 4) Lockscreen-Logo ====================================================
def unlock():
    W, H = 100, 11
    cv = Canvas(W, H, (255, 0, 255))
    cross_spr = ["..#..", "..#..", "#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."]
    cv.sprite(cross_spr, 0, 1, SGOLD)
    x = 9
    for w, c in (("NÄHER ", WHITE), ("ZU ", LBLUE), ("JESUS", SGOLD)):
        text(cv, w, x, 0, c)
        x += len(w) * 6
    cv.save("unlock.ppm")


# === 5) Bildschirmschoner (ttfx-Text) ======================================
# Omarchy lässt Textdateien mit ttfx-Effekten erscheinen. Je zwei Pixel
# übereinander ergeben eine Terminalzelle (▀ ▄ █), so bleiben sie quadratisch;
# Beschriftungen stehen als normaler Text in eigenen Zellen.
class Blocks:
    def __init__(self, cols, rows):
        self.w, self.h = cols, rows * 2
        self.on = [[False] * self.w for _ in range(self.h)]
        self.txt = {}

    def put(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.on[y][x] = True

    def rect(self, x, y, w, h):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy)

    def sprite(self, rows, x, y, scale=1):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "#":
                    self.rect(x + i * scale, y + j * scale, scale, scale)

    def text(self, s, x, y, scale=1):
        """5×7-Pixelschrift; y ist die Oberkante der Akzentzeile."""
        for ch in s:
            if ch in UMLAUT:
                self.sprite([".#.#."], x, y, scale)
            self.sprite(GLYPH.get(ch, GLYPH["?"]), x, y + 2 * scale, scale)
            x += 6 * scale

    def center_text(self, s, y, scale=1):
        self.text(s, (self.w - text_width(s, scale)) // 2, y, scale)

    def label(self, s, col, row):
        """Normaler Terminaltext an Zelle (col, row)."""
        for i, ch in enumerate(s):
            self.txt[col + i, row] = ch

    def center_label(self, s, row):
        self.label(s, (self.w - len(s)) // 2, row)

    def save(self, name):
        cells = {(False, False): " ", (True, False): "▀", (False, True): "▄", (True, True): "█"}
        lines = []
        for r in range(self.h // 2):
            line = "".join(self.txt.get((c, r)) or cells[self.on[2 * r][c], self.on[2 * r + 1][c]]
                           for c in range(self.w))
            lines.append(line.rstrip())
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        (OUT / "screensaver").mkdir(exist_ok=True)
        (OUT / "screensaver" / name).write_text("\n".join(lines) + "\n")


HEART = [".#.#.", "#####", "#####", ".###.", "..#.."]
PILGRIM = ["..##..", "..##..", ".####.", "#.##.#", "..##..", ".#..#.", ".#..#."]


def ss_cross_sunrise():
    b = Blocks(91, 30)
    cx, horizon = b.w // 2, 30
    b.rect(cx - 2, 2, 5, 23)
    b.rect(cx - 10, 8, 21, 5)
    # Sonne hinter dem Kreuz, gestreift wie im 8-Bit-Spiel
    for y in range(horizon - 10, horizon):
        if (horizon - y) % 3 == 0 and y < horizon - 3:
            continue
        for x in range(cx - 14, cx + 15):
            if math.hypot(x - cx, (y - horizon) * 1.35) < 14.5 and abs(x - cx) > 3:
                b.put(x, y)
    for a in range(-80, 81, 20):
        r = math.radians(a - 90)
        for d in range(18, 26, 2):
            b.put(round(cx + math.cos(r) * d * 1.25), round(horizon - 1 + math.sin(r) * d * 0.9))
    for x in range(4, b.w - 4):
        if abs(x - cx) < 26 or x % 2 == 0:
            b.put(x, horizon)
    for sx, spr in ((cx - 7, FOOT_R), (cx + 2, FOOT_L)):
        b.sprite(spr[::2], sx, 33)
    b.center_text("NÄHER ZU JESUS", 41)
    b.center_text("JOH 14,6", 51)
    b.save("1-kreuz-sonnenaufgang.txt")


def ss_press_start():
    b = Blocks(96, 30)
    W = b.w
    b.label("LVL JOH 14,6", 2, 0)
    b.label("STEP +1", W - 30, 0)
    for i in range(3):
        b.sprite(HEART, W - 21 + i * 7, 0)
    b.label("WEG · WAHRHEIT · LEBEN", 2, 1)
    rnd = random.Random(7)
    for _ in range(26):
        b.put(rnd.randrange(2, W - 2), rnd.randrange(6, 26))
    # Hügel mit Kreuz, gestreifte Sonne dahinter
    hx_, ground = 70, 46
    top = ground - 9

    def hill(x):
        return ground - round(9 * math.exp(-((x - hx_) / 13) ** 2))

    for x in range(W):
        for y in range(hill(x), ground):
            b.put(x, y)
    def in_cross(x, y):
        return (abs(x - hx_) <= 2 and top - 23 <= y <= top) or (abs(x - hx_) <= 8 and top - 17 <= y <= top - 13)

    for y in range(top - 15, top + 2):
        for x in range(hx_ - 22, hx_ + 23):
            if math.hypot(x - hx_, (y - top) * 1.3) < 19 and (top - y) % 3 and y < hill(x) - 1 and not in_cross(x, y):
                b.put(x, y)
    b.rect(hx_ - 1, top - 22, 3, 22)
    b.rect(hx_ - 7, top - 16, 15, 3)
    for x in range(W):
        if x % 3 or abs(x - hx_) < 30:
            b.put(x, ground)
    # Pilger und Fußspuren den Weg hinauf
    b.sprite(PILGRIM, 14, ground - 7)
    for i, x in enumerate(range(24, 52, 7)):
        b.sprite(["##", "##", ".."] if i % 2 else ["..", "##", "##"], x, ground - 3 - i)
    b.center_label("P R E S S   S T A R T   T O   F O L L O W", 26)
    b.center_label("1 SPIELER  ·  UNBEGRENZTE LEBEN  ·  GNADE AKTIVIERT", 28)
    b.save("2-press-start.txt")


def ss_terminal():
    b = Blocks(74, 20)
    body = [
        "",
        " naeher@jesus:~$ sudo pacman -S nachfolge",
        " Hinweis: Gnade braucht kein sudo.                         Eph 2,8",
        " :: Pakete (1)  nachfolge-1:1.0-1",
        " :: Installation fortsetzen? [J/n] j",
        " (1/1) installiere nachfolge  [####################] 100%",
        "",
        " [  OK  ] Started weg.service                              Joh 14,6",
        " [  OK  ] Started wahrheit.service",
        " [  OK  ] Started leben.service",
        " [  OK  ] Mounted /home/gnade",
        " [  OK  ] Reached target nachfolge.target",
        "",
        " naeher@jesus:~$ echo $ZIEL",
        " Einen Schritt näher.",
        " naeher@jesus:~$ █",
        "",
    ]
    inner = b.w - 2
    title = " NÄHER-ZU-JESUS BIOS v3.16 "
    b.label("╭─" + title + "─" * (inner - len(title) - 1) + "╮", 0, 0)
    for i, line in enumerate(body):
        b.label("│" + line.ljust(inner) + "│", 0, i + 1)
    b.label("╰" + "─" * inner + "╯", 0, len(body) + 1)
    b.save("3-terminal.txt")


def ss_hexdump():
    verse = "Im Anfang war das Wort, und das Wort war bei Gott, und Gott war das Wort. ".encode()
    rows = 22
    b = Blocks(70, rows + 4)
    b.label("$ xxd johannes_1_1.txt", 0, 0)
    arm = 5                  # Querbalken des Kreuzes (Zeile im Dump)

    def in_cross(byte, row):
        return (6 <= byte <= 9 and 1 <= row <= rows - 2) or (arm <= row <= arm + 2 and 2 <= byte <= 13)

    for row in range(rows):
        line = f"{row * 16:08x}: "
        asc = ""
        for i in range(16):
            v = verse[(row * 16 + i) % len(verse)]
            h = f"{v:02x}" if in_cross(i, row) else "··"
            line += h + (" " if i % 2 else "")
            asc += chr(v) if in_cross(i, row) else "·"
        b.label(line + " " + asc, 0, row + 2)
    b.label("Im Anfang war das Wort.  —  Joh 1,1", 0, rows + 3)
    b.save("4-hexdump-joh-1-1.txt")


def ss_der_weg():
    b = Blocks(90, 26)
    b.center_text("ICH BIN", 0, 2)
    b.center_text("DER WEG", 20, 2)
    for i, x in enumerate(range(8, b.w - 8, 10)):
        b.sprite((FOOT_R if i % 2 else FOOT_L)[::2], x, 36 + 4 * (i % 2))
    b.center_label("DIE WAHRHEIT UND DAS LEBEN.", 24)
    b.center_label("JOH 14,6", 25)
    b.save("5-ich-bin-der-weg.txt")


def screensaver():
    ss_cross_sunrise()
    ss_press_start()
    ss_terminal()
    ss_hexdump()
    ss_der_weg()

sunrise()
boot()
hexdump()
unlock()
screensaver()
print("ok")
