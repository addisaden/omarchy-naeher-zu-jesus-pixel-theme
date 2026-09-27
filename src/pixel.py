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
def screensaver():
    """Einfarbiges Pixelbild für den Omarchy-Bildschirmschoner. Zwei Pixel
    übereinander ergeben eine Terminalzelle (▀ ▄ █), so bleiben sie quadratisch."""
    W, H = 91, 60
    on = [[False] * W for _ in range(H)]

    def put(x, y):
        if 0 <= x < W and 0 <= y < H:
            on[y][x] = True

    cx, horizon = W // 2, 30
    # Kreuz
    for y in range(2, 25):
        for x in range(cx - 2, cx + 3):
            put(x, y)
    for y in range(8, 13):
        for x in range(cx - 10, cx + 11):
            put(x, y)
    # Sonne, die am Horizont hinter dem Kreuz aufgeht (gestreift wie im 8-Bit-Spiel)
    for y in range(horizon - 10, horizon):
        if (horizon - y) % 3 == 0 and y < horizon - 3:
            continue
        for x in range(cx - 14, cx + 15):
            if math.hypot(x - cx, (y - horizon) * 1.35) < 14.5 and abs(x - cx) > 3:
                put(x, y)
    # Strahlen
    for a in range(-80, 81, 20):
        r = math.radians(a - 90)
        for d in range(18, 26, 2):
            put(round(cx + math.cos(r) * d * 1.25), round(horizon - 1 + math.sin(r) * d * 0.9))
    # Horizont
    for x in range(4, W - 4):
        if abs(x - cx) < 26 or x % 2 == 0:
            put(x, horizon)
    # Fußspuren Richtung Kreuz
    for sx, sy, spr in ((cx - 7, 33, FOOT_R), (cx + 2, 33, FOOT_L)):
        for j, row in enumerate(spr[::2]):
            for i, ch in enumerate(row):
                if ch == "#":
                    put(sx + i, sy + j)

    def words(s, y):
        x = (W - text_width(s)) // 2
        for ch in s:
            glyph = GLYPH.get(ch, GLYPH["?"])
            if ch in UMLAUT:
                put(x + 1, y), put(x + 3, y)
            for j, row in enumerate(glyph):
                for i, c in enumerate(row):
                    if c == "#":
                        put(x + i, y + 2 + j)
            x += 6

    words("NÄHER ZU JESUS", 41)
    words("JOH 14,6", 51)

    cells = {(False, False): " ", (True, False): "▀", (False, True): "▄", (True, True): "█"}
    lines = ["".join(cells[on[y][x], on[y + 1][x]] for x in range(W)).rstrip()
             for y in range(0, H, 2)]
    (OUT / "screensaver.txt").write_text("\n".join(lines) + "\n")


sunrise()
boot()
hexdump()
unlock()
screensaver()
print("ok")
