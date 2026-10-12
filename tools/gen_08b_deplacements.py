"""Lot 08b : déplace Z02, Z03 (Obyan → Kagman) et les départs des convois Z07 et Z08.

Les sanctuaires rouges (2,5 km autour de Saipan Intl et de Tinian Intl) ne doivent recouper aucune zone de
combat : un joueur bleu qui attaque la zone y serait détruit. On retire les groupes de chaque zone, on déplace
(et renomme) le cercle, puis on repose les groupes depuis gen_08_zones.py, qui reste la source.
"""
from gen_08_zones import ZONES
from lib import Batch, M, xy
from mcp import cat

import sys
MOVED = {"combatZone_ChalanKanoa": None, "combatZone_Obyan": "combatZone_Kagman",
         "combatZone_Broadway": None, "combatZone_CrossIsland": None}
if "--guguan" in sys.argv:   # lot 08c : Z04 quitte Farallon de Medinilla (sonde DCS du 12/10)
    MOVED = {"combatZone_Medinilla": "combatZone_Guguan"}
# describe_mission ne lit qu'un .miz ; describe_units lit le dossier
# (filtré par zone : sans filtre, describe_units s'arrête à 50 groupes)
names = []
for z in MOVED:
    r = cat.run_action("describe_units", {"mission_path": M, "group_name": z + "-", "include_route": False})
    assert not r.get("truncated"), z
    names += [g["name"] for g in r["groups"]]
b = Batch()
for old, new in MOVED.items():
    for n in names:
        if n.startswith(old + "-"):
            b.act("remove_group", group_name=n)
    zname = new or old
    name, c, r, fname, menu, text, side, catg, groups, statics = next(z for z in ZONES if z[0] == zname)
    b.act("edit_zone", zone_name=old, position=xy(c), radius=r, **({"new_name": new} if new else {}))
    for g in groups:
        b.act("add_group", **side, category=catg, name=g["name"], position=g["position"], units=g["units"],
              for_combat_zone=zname, keep_position=True, **({"route": g["route"]} if g.get("route") else {}))
b.save("08c-guguan.json" if "--guguan" in sys.argv else "08b-deplacements.json")
