#!/usr/bin/env python3
"""Pixel-Icon-Theme für "Näher zu Jesus — Pixel".

Zeichnet Ordner- und Datei-Icons auf einem 16×16-Raster in den Theme-Farben
und schreibt sie als SVG (ein <rect> pro Pixel-Lauf, crispEdges), damit sie in
jeder Größe scharf bleiben. Alles, was hier fehlt, erbt das Theme von
Adwaita/hicolor.

    python3 src/icons.py icons/
"""
import os
import shutil
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "icons")
NAME = "NaeherZuJesus-Pixel"

# Palette (aus colors.toml)
PAL = {
    "O": "#1B0F0A",  # Umriss
    "H": "#FFE7A0",  # Ordner Licht
    "Y": "#FFD166",  # Ordner vorne / Akzent
    "A": "#F4A340",  # Ordner hinten
    "D": "#E85D04",  # Ordner Schatten
    "N": "#5C2A4D",  # Emblem (Pflaume)
    "P": "#F7DFA8",  # Papier
    "F": "#FFF1C9",  # Papier-Ecke
    "S": "#D9BE85",  # Papier-Schatten
    "M": "#4A5A80",  # gedämpft
    "K": "#0A1020",  # Nachthimmel
    "B": "#1A2A4A",  # Himmel hell
    "G": "#7CE38B",  # Phosphor-Grün
    "g": "#2E7D4F",  # Grün dunkel
    "R": "#D93A2E",  # Rot
    "V": "#B0409F",  # Magenta dunkel
    "L": "#3E6FB0",  # Blau dunkel
    "o": "#FF7A1A",  # Orange
    "b": "#8A4B2C",  # Braun
    "l": "#B06A3C",  # Braun hell
    "C": "#7A89A8",  # Mülleimer
    "c": "#BBDEFB",  # Mülleimer hell
}

# ---------------------------------------------------------------- Grundformen

FOLDER = [
    "................",
    ".OOOOOO.........",
    "OAAAAAAO........",
    "OAAAAAAAOOOOOOO.",
    "OAAAAAAAAAAAAAAO",
    "OOOOOOOOOOOOOOOO",
    "OHHHHHHHHHHHHHHO",
    "OYYYYYYYYYYYYYYO",
    "OYYYYYYYYYYYYYYO",
    "OYYYYYYYYYYYYYYO",
    "OYYYYYYYYYYYYYYO",
    "OYYYYYYYYYYYYYYO",
    "OYYYYYYYYYYYYYYO",
    "OYYYYYYYYYYYYYYO",
    "ODDDDDDDDDDDDDDO",
    ".OOOOOOOOOOOOOO.",
]
FOLDER_AREA = (1, 7, 14, 7)  # x, y, Breite, Höhe für das Emblem

PAGE = [
    "..OOOOOOOO......",
    "..OPPPPPPOO.....",
    "..OPPPPPPOFO....",
    "..OPPPPPPOFFO...",
    "..OPPPPPPOOOOO..",
    "..OPPPPPPPPPPO..",
    "..OPPPPPPPPPSO..",
    "..OPPPPPPPPPSO..",
    "..OPPPPPPPPPSO..",
    "..OPPPPPPPPPSO..",
    "..OPPPPPPPPPSO..",
    "..OPPPPPPPPPSO..",
    "..OPPPPPPPPPSO..",
    "..OPPPPPPPPPSO..",
    "..OSSSSSSSSSSO..",
    "..OOOOOOOOOOOO..",
]
PAGE_AREA = (3, 6, 9, 8)

# ------------------------------------------------------------------ Embleme
# '#' wird in der jeweiligen Farbe gezeichnet, andere Buchstaben sind Palette.

EMB = {
    "download": [
        "..###..",
        "..###..",
        "#######",
        ".#####.",
        "..###..",
        ".......",
        "#######",
    ],
    "music": [
        "..#####",
        "..#####",
        "..#...#",
        "..#...#",
        ".##..##",
        "###.###",
        ".#...#.",
    ],
    "pictures": [
        "......##",
        "..#...##",
        ".###....",
        "#####.#.",
        "########",
        "########",
    ],
    "videos": [
        "#.....",
        "###...",
        "#####.",
        "######",
        "#####.",
        "###...",
        "#.....",
    ],
    "documents": [
        "######.",
        ".......",
        "#######",
        ".......",
        "#####..",
        ".......",
        "######.",
    ],
    "desktop": [
        "########",
        "#......#",
        "#......#",
        "#......#",
        "########",
        "...##...",
        "..####..",
    ],
    "templates": [
        "##.#.##",
        "#.....#",
        ".......",
        "#.....#",
        ".......",
        "#.....#",
        "##.#.##",
    ],
    "publicshare": [
        ".##...##.",
        ".##...##.",
        ".........",
        "####.####",
        "####.####",
        "####.####",
    ],
    "home": [
        "...##...",
        "..####..",
        ".######.",
        "########",
        ".##..##.",
        ".##..##.",
        ".##..##.",
    ],
    "remote": [
        "..###..",
        ".#.#.#.",
        "#######",
        "#..#..#",
        "#######",
        ".#.#.#.",
        "..###..",
    ],
    "cross": [
        "..#..",
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ],
    # Seiteninhalte
    "text": [
        "########.",
        ".........",
        "#########",
        ".........",
        "######...",
        ".........",
        "########.",
    ],
    "script": [
        "#........",
        ".#.#####.",
        "#........",
        ".........",
        "..######.",
        ".........",
        "..#####..",
    ],
    "binary": [
        "#.##.#.##",
        ".........",
        "##.#.##.#",
        ".........",
        "#.#.##.#.",
        ".........",
        "##.##.#.#",
    ],
    "image": [
        "BBBBBBBBB",
        "BBBBYYBBB",
        "BBBYYYYBB",
        "BBYYYYYYB",
        "ooooooooo",
        "NNNoooNNN",
        "NNNNNNNNN",
        "NNNNNNNNN",
    ],
    "audio": [
        "..#####",
        "..#####",
        "..#...#",
        "..#...#",
        ".##..##",
        "###.###",
        ".#...#.",
    ],
    "video": [
        "#......",
        "###....",
        "#####..",
        "#######",
        "#####..",
        "###....",
        "#......",
    ],
    "pdf": [
        "RRRRRRRRR",
        "RFRRFRRFR",
        "RRRRRRRRR",
        ".........",
        "MMMMMMMM.",
        ".........",
        "MMMMMM...",
    ],
    "office": [
        "LLLLLLLLL",
        ".........",
        "MMMMMMMMM",
        ".........",
        "MMMMMMM..",
        ".........",
        "MMMMMMMM.",
    ],
    "spreadsheet": [
        "ggggggggg",
        "g...g...g",
        "ggggggggg",
        "g...g...g",
        "ggggggggg",
        "g...g...g",
        "ggggggggg",
    ],
    "presentation": [
        "ooooooooo",
        "o.......o",
        "o..Y....o",
        "o..YY.Y.o",
        "o.YYY.YYo",
        "ooooooooo",
        "....o....",
    ],
    "font": [
        "...###...",
        "..##.##..",
        ".##...##.",
        ".#######.",
        ".##...##.",
        "###...###",
    ],
    "html": [
        "..#####..",
        ".#.#.#.#.",
        "#########",
        "#..#.#..#",
        "#########",
        ".#.#.#.#.",
        "..#####..",
    ],
}

# ------------------------------------------------------- eigenständige Icons

TERMINAL = [
    "................",
    ".MMMMMMMMMMMMMM.",
    "MYYYYYYYYYYoRGYM",
    "MMMMMMMMMMMMMMMM",
    "MKKKKKKKKKKKKKKM",
    "MKGKKKKKKKKKKKKM",
    "MKKGKKKKKKKKKKKM",
    "MKKKGKKKKKKKKKKM",
    "MKKGKKKKKKKKKKKM",
    "MKGKKGGGGKKKKKKM",
    "MKKKKKKKKKKKKKKM",
    "MKKKKKKKKKKKKKKM",
    "MKKKKKKKKKKKKKKM",
    "MKKKKKKKKKKKKKKM",
    ".MMMMMMMMMMMMMM.",
    "................",
]

PACKAGE = [
    "................",
    "................",
    "................",
    ".OOOOOOOOOOOOOO.",
    "ObbbbbbYYbbbbbbO",
    "OllllllYYllllllO",
    "OOOOOOOOOOOOOOOO",
    ".ObbbbbYYbbbbbO.",
    ".OlllllYYlllllO.",
    ".OllllllllllllO.",
    ".OllllllllllllO.",
    ".OlllOOOOOOlllO.",
    ".OlllOPPPPOlllO.",
    ".OlllOOOOOOlllO.",
    ".ObbbbbbbbbbbbO.",
    ".OOOOOOOOOOOOOO.",
]

TRASH = [
    "................",
    "......OOOO......",
    ".OOOOOOOOOOOOOO.",
    ".OccccccccccccO.",
    ".OOOOOOOOOOOOOO.",
    "..OCCCCCCCCCCO..",
    "..OCCcCCcCCcCO..",
    "..OCCcCCcCCcCO..",
    "..OCCcCCcCCcCO..",
    "..OCCcCCcCCcCO..",
    "..OCCcCCcCCcCO..",
    "..OCCcCCcCCcCO..",
    "..OCCcCCcCCcCO..",
    "..OCCCCCCCCCCO..",
    "...OOOOOOOOOO...",
    "................",
]

TRASH_FULL = [
    "....PPP.FF......",
    "...PFPPPPPP.....",
    ".OOOOOOOOOOOOOO.",
    ".OccccccccccccO.",
    ".OOOOOOOOOOOOOO.",
] + TRASH[5:]


# ------------------------------------------------------------------ Zeichnen

def blank():
    return [["."] * 16 for _ in range(16)]


def grid(rows):
    g = blank()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row[:16]):
            g[y][x] = ch
    return g


def stamp(g, emblem, area, color):
    ax, ay, aw, ah = area
    h, w = len(emblem), max(len(r) for r in emblem)
    ox = ax + (aw - w) // 2
    oy = ay + (ah - h) // 2
    for y, row in enumerate(emblem):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            g[oy + y][ox + x] = color if ch == "#" else ch
    return g


def svg(g):
    rects = []
    for y, row in enumerate(g):
        x = 0
        while x < 16:
            ch = row[x]
            if ch == ".":
                x += 1
                continue
            start = x
            while x < 16 and row[x] == ch:
                x += 1
            rects.append(f'<rect x="{start}" y="{y}" width="{x - start}" height="1" fill="{PAL[ch]}"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" '
        'shape-rendering="crispEdges">' + "".join(rects) + "</svg>\n"
    )


def folder(emblem=None):
    g = grid(FOLDER)
    return stamp(g, EMB[emblem], FOLDER_AREA, "N") if emblem else g


def page(content=None, color="M"):
    g = grid(PAGE)
    return stamp(g, EMB[content], PAGE_AREA, color) if content else g


# Icon-Name → (Kontext, Raster). Weitere Namen werden als Symlink angelegt.
ICONS = {
    "places": {
        "folder": folder(),
        "folder-documents": folder("documents"),
        "folder-download": folder("download"),
        "folder-music": folder("music"),
        "folder-pictures": folder("pictures"),
        "folder-videos": folder("videos"),
        "folder-desktop": folder("desktop"),
        "folder-templates": folder("templates"),
        "folder-publicshare": folder("publicshare"),
        "folder-remote": folder("remote"),
        "user-home": folder("home"),
        "folder-cross": folder("cross"),
        "user-trash": grid(TRASH),
        "user-trash-full": grid(TRASH_FULL),
    },
    "mimetypes": {
        "text-x-generic": page("text"),
        "text-x-script": page("script", "g"),
        "application-x-generic": page("binary"),
        "image-x-generic": page("image"),
        "audio-x-generic": page("audio", "V"),
        "video-x-generic": page("video", "R"),
        "application-pdf": page("pdf"),
        "x-office-document": page("office"),
        "x-office-spreadsheet": page("spreadsheet"),
        "x-office-presentation": page("presentation"),
        "font-x-generic": page("font", "N"),
        "text-html": page("html", "L"),
        "package-x-generic": grid(PACKAGE),
        "application-x-executable": grid(TERMINAL),
    },
}

ALIASES = {
    "places": {
        "folder": ["inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
        "folder-download": ["folder-downloads"],
        "folder-desktop": ["user-desktop"],
        "folder-documents": ["folder-text"],
        "folder-pictures": ["folder-images"],
        "folder-videos": ["folder-video"],
        "folder-remote": ["network-workgroup", "folder-network"],
        "user-home": ["folder-home"],
        "user-trash-full": ["trashcan_full"],
        "user-trash": ["trashcan_empty"],
    },
    "mimetypes": {
        "text-x-generic": ["text-plain", "text-x-readme", "text-markdown", "text-x-changelog"],
        "text-x-script": [
            "application-x-shellscript", "text-x-python", "text-x-csrc", "text-x-chdr",
            "text-x-c++src", "text-x-java", "text-x-ruby", "text-x-go", "text-rust",
            "application-javascript", "text-javascript", "application-json", "text-x-lua",
            "application-x-yaml", "application-toml", "application-xml", "text-css",
        ],
        "application-x-generic": ["application-octet-stream", "unknown"],
        "package-x-generic": [
            "application-zip", "application-x-tar", "application-x-compressed-tar",
            "application-x-7z-compressed", "application-x-rar", "application-gzip",
            "application-x-xz", "application-zstd",
        ],
        "application-x-executable": ["application-x-sharedlib", "application-x-object"],
        "image-x-generic": ["image-png", "image-jpeg", "image-gif", "image-webp", "image-svg+xml"],
        "audio-x-generic": ["audio-mpeg", "audio-flac", "audio-x-wav", "audio-ogg"],
        "video-x-generic": ["video-mp4", "video-x-matroska", "video-webm"],
        "x-office-document": ["application-vnd.openxmlformats-officedocument.wordprocessingml.document",
                              "application-vnd.oasis.opendocument.text", "application-msword"],
        "x-office-spreadsheet": ["text-csv", "application-vnd.oasis.opendocument.spreadsheet",
                                 "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        "x-office-presentation": ["application-vnd.oasis.opendocument.presentation",
                                  "application-vnd.openxmlformats-officedocument.presentationml.presentation"],
    },
}

# ---------------------------------------------------- Symbole (-symbolic)
# Einfarbig; GTK färbt sie in der Textfarbe der jeweiligen Stelle ein.
# Raster 16×16, '#' = gesetzt. Einfache Formen werden berechnet.

def canvas():
    return [[False] * 16 for _ in range(16)]


def from_rows(rows):
    c = canvas()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row[:16]):
            c[y][x] = ch == "#"
    return c


def fill(c, x0, y0, x1, y1, on=True):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < 16 and 0 <= y < 16:
                c[y][x] = on
    return c


def frame(c, x0, y0, x1, y1, t=1):
    fill(c, x0, y0, x1, y0 + t - 1)
    fill(c, x0, y1 - t + 1, x1, y1)
    fill(c, x0, y0, x0 + t - 1, y1)
    fill(c, x1 - t + 1, y0, x1, y1)
    return c


def ring(c, cx, cy, r, t=2, on=True):
    for y in range(16):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if r - t < d <= r:
                c[y][x] = on
    return c


def disc(c, cx, cy, r, on=True):
    return ring(c, cx, cy, r, t=r + 1, on=on)


def line(c, x0, y0, x1, y1, t=2, on=True):
    steps = max(abs(x1 - x0), abs(y1 - y0)) or 1
    for i in range(steps + 1):
        x = round(x0 + (x1 - x0) * i / steps)
        y = round(y0 + (y1 - y0) * i / steps)
        fill(c, x, y, x + t - 1, y + t - 1, on)
    return c


def outline(c):
    o = canvas()
    for y in range(16):
        for x in range(16):
            if c[y][x] and any(
                not (0 <= x + dx < 16 and 0 <= y + dy < 16) or not c[y + dy][x + dx]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ):
                o[y][x] = True
    return o


def chevron(direction, small=False):
    c = canvas()
    n = 3 if small else 5              # halbe Höhe
    top = 8 - n - 1
    for i in range(2 * n + 2):
        d = min(i, 2 * n + 1 - i)
        x = (9 if not small else 8) - d
        fill(c, x, top + i, x + 2 - small, top + i)
    if direction == "right":
        c = [row[::-1] for row in c]
    elif direction in ("up", "down"):
        c = [list(r) for r in zip(*c)]   # links → oben
        if direction == "down":
            c = c[::-1]
    return c


def sym_folder():
    c = canvas()
    fill(c, 1, 2, 5, 2)
    fill(c, 1, 3, 14, 3)
    fill(c, 1, 3, 1, 4)
    fill(c, 14, 3, 14, 4)
    fill(c, 1, 5, 14, 13)
    return c


def sym_clock():
    c = ring(canvas(), 7.5, 7.5, 7.5, 2)
    fill(c, 7, 3, 8, 8)
    fill(c, 7, 7, 11, 8)
    return c


STAR = from_rows([
    "................",
    ".......##.......",
    ".......##.......",
    "......####......",
    "......####......",
    ".##############.",
    "..############..",
    "...##########...",
    "....########....",
    "....########....",
    "...####..####...",
    "...###....###...",
    "..###......###..",
    "..##........##..",
    "................",
    "................",
])

HOME = from_rows([
    "................",
    ".......##.......",
    "......####......",
    ".....######.....",
    "....########....",
    "...##########...",
    "..############..",
    ".##############.",
    "...##########...",
    "...##########...",
    "...####..####...",
    "...####..####...",
    "...####..####...",
    "...####..####...",
    "................",
    "................",
])

PAGE_SYM = from_rows([
    "................",
    "...######.......",
    "...#######......",
    "...########.....",
    "...#########....",
    "...##########...",
    "...#........#...",
    "...##########...",
    "...#........#...",
    "...##########...",
    "...#.....####...",
    "...##########...",
    "...##########...",
    "...##########...",
    "................",
    "................",
])

MUSIC = from_rows([
    "................",
    "......#########.",
    "......#########.",
    "......##.....##.",
    "......##.....##.",
    "......##.....##.",
    "......##.....##.",
    "......##.....##.",
    "......##.....##.",
    "......##.....##.",
    "....####...####.",
    "...#####..#####.",
    "...#####..#####.",
    "....###....###..",
    "................",
    "................",
])

PEOPLE = from_rows([
    "................",
    "................",
    "...##......##...",
    "..####....####..",
    "..####....####..",
    "...##......##...",
    "................",
    ".######..######.",
    ".######..######.",
    ".######..######.",
    ".######..######.",
    "................",
    "................",
    "................",
    "................",
    "................",
])


def sym_download():
    c = canvas()
    fill(c, 6, 1, 9, 6)
    for i, w in enumerate((5, 4, 3, 2, 1)):
        fill(c, 8 - w, 7 + i, 7 + w, 7 + i)
    fill(c, 2, 13, 13, 14)
    return c


def sym_pictures():
    c = frame(canvas(), 1, 2, 14, 13)
    fill(c, 10, 4, 11, 5)
    for i, (a, b) in enumerate(((5, 5), (4, 6), (3, 7), (2, 8))):
        fill(c, a, 8 + i, b, 8 + i)
    fill(c, 9, 10, 9, 10)
    fill(c, 8, 11, 12, 11)
    fill(c, 2, 12, 13, 12)
    return c


def sym_videos():
    c = frame(canvas(), 1, 2, 14, 13)
    for i, w in enumerate((1, 2, 3, 4, 3, 2, 1)):
        fill(c, 6, 4 + i, 5 + w, 4 + i)
    return c


def sym_monitor():
    c = frame(canvas(), 1, 2, 14, 10, 2)
    fill(c, 6, 11, 9, 12)
    fill(c, 4, 13, 11, 13)
    return c


def sym_templates():
    c = canvas()
    for x in (3, 4, 7, 8, 11, 12):
        c[1][x] = c[13][x] = True
    for y in (2, 5, 6, 9, 10, 12):
        c[y][3] = c[y][12] = True
    return c


def sym_globe():
    c = ring(canvas(), 7.5, 7.5, 7.5, 2)
    fill(c, 1, 7, 14, 8)
    fill(c, 7, 1, 8, 14)
    return c


def sym_trash(full=False):
    c = canvas()
    fill(c, 6, 1, 10, 1)
    fill(c, 2, 2, 14, 3)
    fill(c, 3, 5, 13, 13)
    if not full:
        for x in (5, 8, 11):
            fill(c, x, 6, x, 12, on=False)
    return c


def sym_drive():
    c = fill(canvas(), 1, 4, 14, 11)
    fill(c, 3, 6, 12, 6, on=False)
    fill(c, 11, 9, 11, 9, on=False)
    fill(c, 13, 9, 13, 9, on=False)
    return c


def sym_find():
    c = ring(canvas(), 6, 6, 5.5, 2)
    line(c, 10, 10, 13, 13)
    return c


def sym_menu():
    c = canvas()
    for y in (3, 7, 11):
        fill(c, 2, y, 13, y + 1)
    return c


def sym_more():
    c = canvas()
    for y in (2, 7, 12):
        fill(c, 7, y, 8, y + 1)
    return c


def sym_grid():
    c = canvas()
    for x, y in ((2, 2), (9, 2), (2, 9), (9, 9)):
        fill(c, x, y, x + 4, y + 4)
    return c


def sym_list():
    c = canvas()
    for y in (3, 7, 11):
        fill(c, 2, y, 3, y + 1)
        fill(c, 5, y, 13, y + 1)
    return c


def sym_sidebar():
    c = frame(canvas(), 1, 2, 14, 13)
    fill(c, 1, 2, 5, 13)
    return c


def sym_close():
    c = line(canvas(), 3, 3, 11, 11)
    return line(c, 11, 3, 3, 11)


def sym_add():
    c = fill(canvas(), 7, 2, 8, 13)
    return fill(c, 2, 7, 13, 8)


def sym_check():
    c = line(canvas(), 2, 8, 5, 11)
    return line(c, 5, 11, 12, 4)


def sym_clear():
    c = disc(canvas(), 7.5, 7.5, 7.5)
    line(c, 5, 5, 9, 9, on=False)
    return line(c, 9, 5, 5, 9, on=False)


def sym_bookmark():
    c = fill(canvas(), 3, 1, 12, 14)
    for i in range(4):
        fill(c, 4 + i, 14 - i, 11 - i, 14 - i, on=False)
    return c


def sym_maximize():
    return frame(canvas(), 3, 3, 12, 12, 2)


def sym_minimize():
    return fill(canvas(), 3, 11, 12, 12)


def sym_restore():
    c = frame(canvas(), 2, 5, 10, 13, 2)
    fill(c, 5, 2, 13, 3)
    return fill(c, 12, 2, 13, 10)


SYMBOLIC = {
    "folder": sym_folder(),
    "user-home": HOME,
    "folder-documents": PAGE_SYM,
    "folder-download": sym_download(),
    "folder-music": MUSIC,
    "folder-pictures": sym_pictures(),
    "folder-videos": sym_videos(),
    "user-desktop": sym_monitor(),
    "folder-templates": sym_templates(),
    "folder-publicshare": PEOPLE,
    "folder-remote": sym_globe(),
    "user-trash": sym_trash(),
    "user-trash-full": sym_trash(full=True),
    "document-open-recent": sym_clock(),
    "starred": STAR,
    "non-starred": outline(STAR),
    "drive-harddisk": sym_drive(),
    "network-computer": sym_monitor(),
    "go-previous": chevron("left"),
    "go-next": chevron("right"),
    "go-up": chevron("up"),
    "go-down": chevron("down"),
    "pan-start": chevron("left", small=True),
    "pan-end": chevron("right", small=True),
    "pan-up": chevron("up", small=True),
    "pan-down": chevron("down", small=True),
    "edit-find": sym_find(),
    "open-menu": sym_menu(),
    "view-more": sym_more(),
    "view-grid": sym_grid(),
    "view-list": sym_list(),
    "sidebar-show": sym_sidebar(),
    "window-close": sym_close(),
    "window-maximize": sym_maximize(),
    "window-minimize": sym_minimize(),
    "window-restore": sym_restore(),
    "list-add": sym_add(),
    "object-select": sym_check(),
    "edit-clear": sym_clear(),
    "bookmark-new": sym_bookmark(),
}

SYMBOLIC_ALIASES = {
    "go-previous": ["go-previous-ltr"],
    "go-next": ["go-next-ltr"],
    "edit-find": ["system-search"],
    "folder-remote": ["network-workgroup", "network-server"],
    "network-computer": ["computer"],
    "view-more": ["view-more-vertical"],
    "edit-clear": ["edit-clear-rtl"],
    "folder": ["inode-directory"],
}


def svg_sym(c):
    rects = []
    for y, row in enumerate(c):
        x = 0
        while x < 16:
            if not row[x]:
                x += 1
                continue
            start = x
            while x < 16 and row[x]:
                x += 1
            rects.append(f'<rect x="{start}" y="{y}" width="{x - start}" height="1"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" '
        'shape-rendering="crispEdges" fill="#2e3436">' + "".join(rects) + "</svg>\n"
    )


INDEX = f"""[Icon Theme]
Name=Näher zu Jesus Pixel
Comment=8-Bit-Ordner und -Dateien im Sonnenaufgangs-Stil
Example=folder
Inherits=Adwaita,hicolor

Directories=scalable/places,scalable/mimetypes,symbolic

[symbolic]
Context=Actions
Size=16
MinSize=8
MaxSize=512
Type=Scalable

[scalable/places]
Context=Places
Size=64
MinSize=8
MaxSize=512
Type=Scalable

[scalable/mimetypes]
Context=MimeTypes
Size=64
MinSize=8
MaxSize=512
Type=Scalable
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for ctx, icons in ICONS.items():
        d = OUT / "scalable" / ctx
        d.mkdir(parents=True)
        for name, g in icons.items():
            (d / f"{name}.svg").write_text(svg(g))
        for target, names in ALIASES.get(ctx, {}).items():
            for n in names:
                os.symlink(f"{target}.svg", d / f"{n}.svg")
    d = OUT / "symbolic"
    d.mkdir(parents=True)
    for name, c in SYMBOLIC.items():
        (d / f"{name}-symbolic.svg").write_text(svg_sym(c))
    for target, names in SYMBOLIC_ALIASES.items():
        for n in names:
            os.symlink(f"{target}-symbolic.svg", d / f"{n}-symbolic.svg")
    (OUT / "index.theme").write_text(INDEX)

    # Übersicht der Symbole (hell auf Nachthimmel)
    cols, cell = 10, 20
    rows = (len(SYMBOLIC) + cols - 1) // cols
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cols * cell} {rows * cell}" '
             f'width="{cols * cell * 6}" height="{rows * cell * 6}" shape-rendering="crispEdges">',
             '<rect width="100%" height="100%" fill="#0A1020"/>']
    for i, c in enumerate(SYMBOLIC.values()):
        x, y = (i % cols) * cell + 2, (i // cols) * cell + 2
        inner = svg_sym(c).split(">", 1)[1].rsplit("</svg>", 1)[0]
        parts.append(f'<g transform="translate({x},{y})" fill="#F7DFA8">{inner}</g>')
    parts.append("</svg>\n")
    (OUT.parent / "out").mkdir(exist_ok=True)
    (OUT.parent / "out" / "symbolic-preview.svg").write_text("".join(parts))

    # Übersicht (preview-icons.svg) zum Anschauen
    names = [(c, n) for c, icons in ICONS.items() for n in icons]
    cols, cell = 7, 20
    rows = (len(names) + cols - 1) // cols
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cols * cell} {rows * cell}" '
             f'width="{cols * cell * 8}" height="{rows * cell * 8}" shape-rendering="crispEdges">',
             f'<rect width="100%" height="100%" fill="#0A1020"/>']
    for i, (c, n) in enumerate(names):
        x, y = (i % cols) * cell + 2, (i // cols) * cell + 2
        inner = svg(ICONS[c][n]).split(">", 1)[1].rsplit("</svg>", 1)[0]
        parts.append(f'<g transform="translate({x},{y})">{inner}</g>')
    parts.append("</svg>\n")
    (OUT.parent / "out").mkdir(exist_ok=True)
    (OUT.parent / "out" / "icons-preview.svg").write_text("".join(parts))
    print(f"{sum(len(v) for v in ICONS.values())} Icons nach {OUT}/")


if __name__ == "__main__":
    main()
