"""Lot 16 : dessins F10 (add_map_drawing, pour qu'ils survivent au build).

Chaque zone a son contour à son rayon réel ET son étiquette ; ligne de front, sanctuaires, QRA, hippodromes de
soutien, arène. Étiquettes sur fond clair opaque (sans fond, l'action met du noir à moitié transparent et le texte
sombre devient illisible, Caucase 29/09/2026). Pas de trait en tirets : add_map_drawing n'écrit que du plein
(VMCT FIX-OPEN-TRAINING-CAUCASUS-FINDINGS ticket 03).
Couches : Common pour ce que les deux camps partagent (front, zones, sanctuaires, QRA, arène), Blue / Red pour
les hippodromes de soutien de chaque camp.
"""
import math

import gen_07_entrainement as e
import gen_08_zones as z
from gen_09_qra_cap import QRAS
from gen_10_joueurs import ARENA, SANCTUARIES
from lib import Batch, xy

LABEL_BG = "0xffffffe0"
RED, BLUE, ORANGE, GREEN, MAGENTA = "0xcc0000ff", "0x0040ccff", "0xe07000ff", "0x008000ff", "0xb000b0ff"


def above(c, r, gap=800):
    return (c[0] + r + gap, c[1])


b = Batch()


def circle(layer, name, c, r, color, fill="0x00000000", thickness=3):
    b.act("add_map_drawing", layer=layer, shape="circle", name=name, position=xy(c), radius=r, color=color,
          fill_color=fill, thickness=thickness)


def label(layer, name, p, text, color, size=12):
    b.act("add_map_drawing", layer=layer, shape="textbox", name=name, position=xy(p), text=text, color=color,
          fill_color=LABEL_BG, font_size=size)


# ── front (approximatif) : perpendiculaire au détroit Rota–Tinian, en son milieu ──
mid, axis = (121000, 69000), math.radians(24.5 + 90)
pa = (mid[0] + 60000 * math.cos(axis), mid[1] + 60000 * math.sin(axis))
pb = (mid[0] - 60000 * math.cos(axis), mid[1] - 60000 * math.sin(axis))
b.act("add_map_drawing", layer="Common", shape="line", name="Front", points=[xy(pa), xy(pb)], color=RED, thickness=6)
label("Common", "Front étiquette", (pa[0] + 4000, pa[1]), "FRONT (approximatif) : détroit Rota – Tinian", RED, 14)

# ── zones d'entraînement : un cercle et une étiquette par famille (niveaux imbriqués sur le même cercle) ──
for zone, c, r, fname, *_ in e.ZONES:
    if not zone.endswith("_Easy"):
        continue
    fam = fname.split()[0][0]
    text = {"H": "H1-H3 Entraînement hélicoptères — Talofofo", "A": "A1-A3 Entraînement attaque — North West Field",
            "S": "S1-S3 Entraînement SEAD — Rota"}[fam]
    circle("Common", f"Zone {zone[:-5]}", c, r, ORANGE, "0xe0700018")
    label("Common", f"Zone {zone[:-5]} étiquette", above(c, r), text, ORANGE)

# ── vraies zones de combat ──
for zone, c, r, fname, *_ in z.ZONES:
    circle("Common", f"Zone {zone}", c, r, RED, "0xcc000018")
    label("Common", f"Zone {zone} étiquette", above(c, r), fname, RED, 11)

# ── QRA ──
for q in QRAS:
    col = MAGENTA if q["side"]["coalition"] == "red" else BLUE
    circle("Common", f"QRA {q['name']}", q["center"], q["radius"], col, thickness=2)
    label("Common", f"QRA {q['name']} étiquette", (q["center"][0] + q["radius"] - 6000, q["center"][1]),
          f"{q['name']} ({round(q['radius'] / 1852)} nm)", col, 11)

# ── sanctuaires ──
for name, tz, c, r, side in SANCTUARIES:
    circle("Common", name, c, r, GREEN, "0x00800018", thickness=2)
    label("Common", f"{name} étiquette", (c[0] - r - 1500, c[1]), name, GREEN, 10)

# ── arène ──
circle("Common", "Arène cercle", ARENA[0], ARENA[1], GREEN, thickness=3)
label("Common", "Arène étiquette", above(ARENA[0], ARENA[1], 3000), "ARÈNE joueurs contre joueurs (slots en vol)", GREEN, 14)

# ── hippodromes de soutien ──
TRACKS = [
    ("Blue", "Texaco 1", (30000, -70000), (90000, -70000), "Texaco 1 — 50Y — U290.0 — FL220"),
    ("Blue", "Arco 1", (-30000, -50000), (20000, -50000), "Arco 1 — 51Y — U291.0 — FL180"),
    ("Blue", "Texaco 2", (190000, 265000), (250000, 265000), "Texaco 2 — 52Y — U292.0 — FL240"),
    ("Blue", "Arco 2", (70000, 135000), (130000, 135000), "Arco 2 — 53Y — U293.0 — FL200"),
    ("Blue", "Magic 1", (60000, -130000), (140000, -130000), "Magic 1 AWACS — U282.0"),
    ("Blue", "Overlord 1", (120000, 295000), (220000, 295000), "Overlord 1 AWACS — U283.0"),
    ("Red", "Shell 1", (250000, 60000), (300000, 40000), "Shell 1 IL-78 — U294.0 — FL200"),
    ("Red", "Wizard 1", (330000, 60000), (400000, 60000), "Wizard 1 AWACS — U284.0"),
]
for layer, n, a, bb, text in TRACKS:
    col = BLUE if layer == "Blue" else RED
    b.act("add_map_drawing", layer=layer, shape="line", name=f"Piste {n}", points=[xy(a), xy(bb)], color=col,
          thickness=4)
    label(layer, f"Piste {n} étiquette", ((a[0] + bb[0]) / 2, (a[1] + bb[1]) / 2 + 6000), text, col, 10)

b.save("16-dessins.json")
