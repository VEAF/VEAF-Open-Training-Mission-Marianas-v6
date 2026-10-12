"""Écrit src/presets.yaml (plan radio des Mariannes), puis les canaux de base par set_airfield_channels.

Bande des tours (describe_airfield_channels, 11/10/2026) : UHF 250.0, 250.05, 250.1, 256.9, 340.2 ;
VHF 118.1-126.2 ; FM 38.4-38.6. Olf Orote, North West Field et Pagan n'ont aucune fréquence dans DCS.
Tout le reste est placé hors de cette bande : AWACS 282-286, ravitailleurs 290-296 (dernier chiffre = TACAN
50Y-56Y), porte-avions 305-307, patrouilles VHF 135-136.5 / UHF 390-395.5, FARP Merizo FM 40.0.
"""
import yaml

from lib import M
from mcp import cat

TACTICAL = [
    ("Guard", "Guard", {"uhf": 243, "vhf": 121.5}),
    ("Magic-1", "Magic 1 AWACS ouest", {"uhf": 282.0}),
    ("Overlord-1", "Overlord 1 AWACS est", {"uhf": 283.0}),
    ("Wizard-1", "Wizard 1 AWACS", {"uhf": 284.0}),
    ("Darkstar-1", "Darkstar 1 Arène", {"uhf": 285.0}),
    ("Focus-1", "Focus 1 Arène", {"uhf": 286.0}),
    ("Texaco-1", "Texaco 1/BS/50Y", {"uhf": 290.0}),
    ("Arco-1", "Arco 1/BM/51Y", {"uhf": 291.0}),
    ("Texaco-2", "Texaco 2/BS/52Y", {"uhf": 292.0}),
    ("Arco-2", "Arco 2/BM/53Y", {"uhf": 293.0}),
    ("Shell-1", "Shell 1 IL-78", {"uhf": 294.0}),
    ("S3B-Stennis", "Shell 5 S-3B/55Y", {"uhf": 295.0}),
    ("S3B-Roosevelt", "Shell 6 S-3B/56Y", {"uhf": 296.0}),
    ("Stennis", "Stennis/74X/ICLS11", {"uhf": 305.0}),
    ("Roosevelt", "Roosevelt/71X/ICLS12", {"uhf": 306.0}),
    ("Tarawa", "Tarawa/73X/ICLS13", {"uhf": 307.0}),
    ("FARP-Merizo", "FARP Merizo", {"fm": 40.0}),
]
BLUE_FLIGHTS = ["Archer", "Arctic", "Astro", "Nickel", "Nitro", "Ninja", "Pinder", "Bengal", "Blade", "Gordon"]
RED_FLIGHTS = ["Berkut", "Sokol", "Strizh", "Orel", "Yastreb", "Grach"]
BLUE_BASES = ["Andersen AFB", "Antonio B. Won Pat Intl"]
RED_BASES = ["Saipan Intl", "Tinian Intl"]


def numbered(items):
    return {i: v for i, v in enumerate(items, 1)}


def fm_list(farp=None):
    out = {}
    for i, mhz in enumerate(range(30, 60), 1):
        out[i] = farp if (farp and mhz == 40) else mhz
    return out


guard_uhf = {"title": "Guard/UHF", "channel": "Guard"}
guard_vhf = {"title": "Guard/VHF", "channel": "Guard"}
blue_bases = ["Base-" + b for b in BLUE_BASES]
red_bases = ["Base-" + b for b in RED_BASES]
doc = {
    "channel_lists": {
        "blue": {
            "primary_1": numbered([guard_uhf, "Magic-1", "Overlord-1", "Texaco-1", "Arco-1", "Texaco-2", "Arco-2",
                                   "Stennis", "Roosevelt", "Tarawa", *blue_bases, "S3B-Stennis", "S3B-Roosevelt",
                                   "Darkstar-1"]),
            "primary_2": numbered([guard_vhf, *BLUE_FLIGHTS, *blue_bases]),
            "fm_supplement": fm_list("FARP-Merizo"),
        },
        "red": {
            "primary_1": numbered([guard_uhf, "Wizard-1", "Shell-1", "Focus-1", *red_bases]),
            "primary_2": numbered([guard_vhf, *RED_FLIGHTS, *red_bases]),
            "fm_supplement": fm_list(),
        },
    },
    "channels_collection": {
        "tactical": {k: {"title": t, "freqs": f} for k, t, f in TACTICAL},
        "flights": {
            **{n: {"title": n, "freqs": {"vhf": round(135.0 + i / 10, 1), "uhf": round(390.0 + i / 10, 1)}}
               for i, n in enumerate(BLUE_FLIGHTS)},
            **{n: {"title": n, "freqs": {"vhf": round(136.0 + i / 10, 1), "uhf": round(395.0 + i / 10, 1)}}
               for i, n in enumerate(RED_FLIGHTS)},
        },
        "bases": {},
    },
}
HEADER = """# Plan radio de l'Open Training Mariannes — écrit par tools/gen_12_presets.py, ne pas éditer à la main.
# Hors bande des tours : les tours des Mariannes occupent UHF 250.0-256.9 et 340.2, VHF 118.1-126.2,
# FM 38.4-38.6 (describe_airfield_channels, 11/10/2026). AWACS 282-286, ravitailleurs 290-296 (dernier chiffre
# = TACAN), porte-avions 305-307, patrouilles VHF 135-136.5 / UHF 390-395.5, FARP Merizo FM 40.0.
# Les canaux d'aérodromes (collection `bases`) viennent de set_airfield_channels : fréquences DCS.
"""
path = M + "/src/presets.yaml"
with open(path, "w", encoding="utf-8") as f:
    f.write(HEADER)
    yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=200)
print(cat.run_action("set_airfield_channels", {"mission_path": M, "airfields": BLUE_BASES + RED_BASES}))
