# Näher zu Jesus — Pixel

Ein 8-Bit-Theme für [Omarchy](https://omarchy.org): Sonnenaufgang über dem Nachthimmel, Bernstein-CRT-Terminal, Phosphor-Grün und ein Fensterrahmen im Sonnenaufgangs-Verlauf.

> Kurze Impulse, die dich mindestens einen Schritt näher zu Jesus bringen.

![Vorschau](preview.png)

## Installation

```bash
omarchy theme install https://github.com/<DEIN-GITHUB-NAME>/omarchy-naeher-zu-jesus-pixel-theme.git
```

Danach im Menü unter *Style → Theme* auswählen oder:

```bash
omarchy theme set naeher-zu-jesus-pixel
```

## Hintergründe

Mit `omarchy theme bg next` durchschalten:

| Datei | Motiv |
|---|---|
| `1-pixel-sonnenaufgang.png` | Retro-Game-Szene: Kreuz, Sonne, Fußspuren, HUD „LVL JOH 14,6“ |
| `2-boot.png` | BIOS/systemd-Bootlog: `REACHED TARGET NACHFOLGE.TARGET`, „Gnade braucht kein sudo“ (Eph 2,8) |
| `3-hexdump-joh-1-1.png` | `xxd` von Joh 1,1, das Kreuz leuchtet aus den Bytes |
| `4-titelbild-8bit.png` | Das Titelbild, auf 320×200 gedithert |

Alle Hintergründe sind 3840×2400 (16:10) und haben genug Rand, damit auf 16:9-Monitoren nichts Wichtiges abgeschnitten wird.

## Farben

| Rolle | Farbe |
|---|---|
| Hintergrund | `#0A1020` |
| Text (Bernstein) | `#F7DFA8` |
| Akzent | `#FFD166` |
| Orange | `#FF7A1A` |
| Blau | `#90CAF9` |
| Grün (Phosphor) | `#7CE38B` |
| Rahmen aktiv | `#FFD166 → #E85D04 → #5C2A4D`, 45° |

## Selbst neu rendern

`src/pixel.py` zeichnet die Motive pixelgenau in niedriger Auflösung (eigener 5×7-Bitmap-Font, Bayer-Dithering) und braucht nur Python 3 und ImageMagick:

```bash
python3 src/pixel.py out/
magick out/sunrise.ppm -filter point -resize 800% backgrounds/1-pixel-sonnenaufgang.png
magick out/hex.ppm     -filter point -resize 800% backgrounds/3-hexdump-joh-1-1.png
magick out/boot.ppm    -filter point -resize 400% backgrounds/2-boot.png
magick out/unlock.ppm -transparent '#FF00FF' -filter point -resize 800% unlock.png
```
