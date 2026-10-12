"""Déplace chaque groupe vers la place libre que probe_clear.py a trouvée (tools/clear_moves.json).

Un groupe de zone de combat n'appartient à sa zone que s'il est DANS son cercle : un déplacement qui l'en sortirait
est refusé et signalé (sauf départ de convoi : le cercle de la zone est alors recentré sur lui). Les déplacements
passent par set_group_properties (toute la route suit le groupe), dans un lot écrit avant d'être exécuté.

    python apply_clear_moves.py            -> écrit et exécute tools/batches/17-clairieres.json
"""
import json
import math
import sys

from lib import Batch, M
from mcp import cat
from paths import ROOT, TOOLS
from veaf_mission_mcp.mission_folder import load_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
moves = json.load(open(TOOLS / "clear_moves.json", encoding="utf-8"))
m = load_folder_mission(ROOT).mission_content
zones = m["triggers"]["zones"]
zones = zones if isinstance(zones, list) else [zones[k] for k in sorted(zones)]
zone = {z["name"]: (z["x"], z["y"], z["radius"]) for z in zones}

b, refused = Batch(), []
for g, (x, y, r) in sorted(moves.items()):
    if r == 0:
        continue
    if g.startswith("combatZone_"):
        zn = g.split("-", 1)[0]
        zx, zy, zr = zone[zn]
        d = math.hypot(x - zx, y - zy)
        if d > zr - 50:
            if "-Convoi" in g:
                b.act("edit_zone", zone_name=zn, position={"x": x, "y": y})
                print(f"  {zn} recentré sur le départ du convoi ({r} m)")
            else:
                refused.append(f"{g} : la place libre est à {d:.0f} m du centre, la zone fait {zr:.0f} m")
                continue
    b.act("set_group_properties", group_name=g, move_to={"x": x, "y": y})
for line in refused:
    print("  REFUSÉ", line)
b.save(sys.argv[1] if len(sys.argv) > 1 else "17-clairieres.json")
for i, it in enumerate(b.items, 1):
    res = cat.run_action(it["name"], it["params"])
    w = [x for x in res.get("warnings", []) if "surface not checked" not in str(x)]
    if w:
        print(f"  [{i}] {it['params'].get('group_name') or it['params'].get('zone_name')} : {w}")
print(f"VERDICT : {len(b.items)} actions, {len(refused)} déplacements refusés")
