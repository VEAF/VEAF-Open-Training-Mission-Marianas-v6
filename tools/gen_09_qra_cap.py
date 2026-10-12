"""Lot 09 : QRA (rouges et bleue) et CAP à la demande.

QRA : cercle dans le territoire du camp qui défend, réponse graduée, deux types différents par niveau tirés au
sort, délai 90 s, pas de réaction aux hélicoptères, pas de menu radio ouvert à tous.
  - Saipan/Tinian : 25 nm autour du milieu des deux îles ; Rota est à 58 nm, le Tarawa à 62 nm.
  - Pagan : 30 nm.
  - Guam : 30 nm ; Rota (champ de tir SEAD) est à 43 nm, hors du cercle.
CAP rouges dans le territoire rouge ; CAP bleue décalée sur le Tarawa, à l'est de Rota (à 56 km du SA-11 du champ de tir SEAD).
"""
import json

from lib import BLUE, RED, RED_CN, ROOT, Batch, xy

V5 = json.loads((ROOT / "tools/loadouts-v5.json").read_text(encoding="utf-8"))["groups"]
J11_FOX3 = {"pylons": V5["veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1"]["pylons"]}
MIG29_FOX1 = {"payload": "R-73*4,R-27R*2"}
SU30_FOX3 = {"payload": "R-73*4,R-77*6"}
SU27_FOX1 = {"payload": "R-73*4,R-27ER*6"}
MIG31 = {"payload": "R-40R*2,R-33*4"}
F16_FOX3 = {"payload": "AIM-120C*4, AIM-9M*2, Fuel"}
F15_FOX3 = {"payload": "AIM-9*4,AIM-120*4,Fuel"}
F14_FOX3 = {"payload": "AIM-54C*4,AIM-9*2,AIM-7*2"}

QRAS = [
    dict(name="QRA Saipan", side=RED, zone="QRA-Saipan", center=(173000, 96000), radius=46300, airfield="Saipan Intl",
         enemy="BLUE", levels=[
             (1, [("QRA-Saipan-MiG29", "MiG-29S", 2, MIG29_FOX1), ("QRA-Saipan-J11", "J-11A", 2, J11_FOX3)]),
             (3, [("QRA-Saipan-Su30", "Su-30", 2, SU30_FOX3), ("QRA-Saipan-Su27", "Su-27", 4, SU27_FOX1)])]),
    dict(name="QRA Pagan", side=RED, zone="QRA-Pagan", center=(512410, 107565), radius=55560, airfield="Pagan Airstrip",
         enemy="BLUE", levels=[
             (1, [("QRA-Pagan-MiG29", "MiG-29S", 2, MIG29_FOX1), ("QRA-Pagan-J11", "J-11A", 2, J11_FOX3)]),
             (3, [("QRA-Pagan-MiG31", "MiG-31", 2, MIG31), ("QRA-Pagan-Su30", "Su-30", 2, SU30_FOX3)])]),
    dict(name="QRA Guam", side=BLUE, zone="QRA-Guam", center=(5000, 2000), radius=55560, airfield="Andersen AFB",
         enemy="RED", levels=[
             (1, [("QRA-Guam-F16", "F-16C bl.50", 2, F16_FOX3), ("QRA-Guam-F15", "F-15C", 2, F15_FOX3)]),
             (3, [("QRA-Guam-F15x4", "F-15C", 4, F15_FOX3), ("QRA-Guam-F14", "F-14A", 2, F14_FOX3)])]),
]

# (nom, type, nombre, camp, a, b, FL, kt, emport, menu, briefing)
CAPS = [
    ("CAP-Tinian-MiG29", "MiG-29S", 2, RED, (163000, 84000), (176000, 96000), 220, 420, MIG29_FOX1,
     "CAP rouge MiG-29 (Fox 1) — Tinian — FL220",
     "Deux MiG-29S armés de R-27R et R-73 patrouillent au-dessus de Tinian et d'Aguijan, au FL220. Emport : R-73*4,R-27R*2."),
    ("CAP-Saipan-J11", "J-11A", 2, RED_CN, (186000, 116000), (204000, 118000), 250, 440, J11_FOX3,
     "CAP rouge J-11A (Fox 3) — Saipan — FL250",
     "Deux J-11A armés de R-77 et R-73 patrouillent à l'est de Saipan, au FL250."),
    ("CAP-Anatahan-MiG31", "MiG-31", 2, RED, (300000, 92000), (345000, 92000), 400, 520, MIG31,
     "CAP rouge MiG-31 (intercepteur haut et rapide) — Anatahan — FL400",
     "Deux MiG-31 patrouillent haut et vite entre Anatahan et Sarigan, au FL400. Emport : R-40R*2,R-33*4."),
    ("Raid-Saipan-Tu22", "Tu-22M3", 2, RED, (215000, 98000), (245000, 98000), 250, 450, {"payload": "FAB-250*69"},
     "Raid rouge Tu-22M3 à intercepter — nord de Saipan — FL250",
     "Deux Tu-22M3 chargés de bombes tournent au nord de Saipan, au FL250, prêts à frapper Guam : les intercepter. "
     "Emport : FAB-250*69."),
    ("CAP-Guam-F16", "F-16C bl.50", 2, BLUE, (20000, 8000), (40000, 22000), 220, 420, F16_FOX3,
     "CAP bleue F-16 (Fox 3) — nord de Guam — FL220",
     "Deux F-16C patrouillent au nord de Guam, entre North West Field et le détroit de Rota, au FL220. "
     "Emport : AIM-120C*4, AIM-9M*2, Fuel."),
    ("CAP-Tarawa-F15", "F-15C", 2, BLUE, (70000, 100000), (90000, 110000), 250, 440, F15_FOX3,
     "CAP bleue F-15 (Fox 3) — Tarawa — FL250",
     "Deux F-15C couvrent le groupe amphibie du Tarawa, à l'est de Rota, au FL250. Emport : AIM-9*4,AIM-120*4,Fuel."),
]

if __name__ == "__main__":
    b = Batch()
    for q in QRAS:
        groups, levels = [], []
        for count, members in q["levels"]:
            names = []
            for gname, typ, n, loadout in members:
                groups.append({"name": gname, "units": [{"type": typ, "count": n}], "position": xy(q["center"]),
                               "altitude_ft": 15000, "speed_kt": 400,   # sans « task » : CAP y ajoute un EngageTargets (lot 09b)
                               **loadout})
                names.append(gname)
            levels.append({"enemy_count": count, "groups": names, "random_pick": 1})
        side = q["side"]
        b.act("create_qra", name=q["name"], coalition=side["coalition"], country_id=side["country_id"],
              country_name=side["country_name"], trigger_zone=q["zone"], position=xy(q["center"]), radius=q["radius"],
              groups=groups, enemy_coalitions=[q["enemy"]],
              qra={"groups_by_enemy_count": levels, "delay_before_activating": 90, "delay_before_rearming": 600,
                   "react_on_helicopters": False, "airport_link": q["airfield"]})
    for name, typ, n, side, a, bb, fl, kt, loadout, menu, brief in CAPS:
        b.act("create_cap_mission", mission_name=name, units=[{"type": typ, "count": n}], **side, position=xy(a),
              route=[{**xy(bb), "altitude_ft": fl * 100}], altitude_ft=fl * 100, speed_kt=kt,
              cap={"menu_name": menu, "briefing": brief}, **loadout)
    b.save("09-qra-cap.json")
