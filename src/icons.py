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

INDEX = f"""[Icon Theme]
Name=Näher zu Jesus Pixel
Comment=8-Bit-Ordner und -Dateien im Sonnenaufgangs-Stil
Example=folder
Inherits=Adwaita,hicolor

Directories=scalable/places,scalable/mimetypes

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
    (OUT / "index.theme").write_text(INDEX)

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
