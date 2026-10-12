"""Pose chaque véhicule d'un convoi sur la route (land.getClosestPointOnRoads), en file derrière la tête.

La tête est déjà sur la route (probe_clear.py, sol 4). Les suivants sont pris en remontant la route
(à l'opposé du premier point), ramenés au point de route le plus proche, à 25 m au moins les uns des autres. Mission de test lancée,
dcs-serve connecté. Écrit et exécute tools/batches/17c-convois.json.
"""
import json
import math
import sys

import probe_scenery as ps
from lib import Batch
from mcp import cat
from paths import ROOT
from veaf_mission_mcp.mission_folder import load_folder_mission

sys.stdout.reconfigure(encoding="utf-8")


def seq(v):
    return list(v.values()) if isinstance(v, dict) else list(v or [])


m = load_folder_mission(ROOT).mission_content
b = Batch()
for co in m["coalition"].values():
    for c in seq(co.get("country")):
        for g in seq((c.get("vehicle") or {}).get("group")):
            if "-Convoi" not in g["name"]:
                continue
            us, pts = seq(g["units"]), seq(g["route"]["points"])
            hx, hy = us[0]["x"], us[0]["y"]
            nx, ny = pts[1]["x"], pts[1]["y"]
            ang = math.atan2(ny - hy, nx - hx)
            # candidats tous les 10 m en remontant la route ; on garde ceux à 25 m au moins des précédents
            want = [(hx - 10 * i * math.cos(ang), hy - 10 * i * math.sin(ang)) for i in range(60)]
            lua = ("local o = {} for _, p in ipairs({%s}) do local x, y = land.getClosestPointOnRoads('roads', p[1], p[2]) "
                   "o[#o + 1] = math.floor(x) .. ',' .. math.floor(y) .. ',' .. land.getSurfaceType({x = x, y = y}) end "
                   "return 'r=' .. table.concat(o, ';')") % ",".join("{%d,%d}" % p for p in want)
            cands = [tuple(map(int, s.split(","))) for s in ps.exec_lua(lua)[2:].split(";")]
            snapped = []
            for x, y, s in cands:
                if s == 4 and all(math.hypot(x - a, y - b_) >= 25 for a, b_, _ in snapped):
                    snapped.append((x, y, s))
                if len(snapped) == len(us):
                    break
            assert len(snapped) == len(us), g["name"]
            for u, (x, y, s) in zip(us, snapped):
                b.act("set_unit_properties", group_name=g["name"], unit_name=u["name"], position={"x": x, "y": y})
            print(g["name"], [(x, y, s) for x, y, s in snapped])
b.save("17d-convois-espaces.json")
for it in b.items:
    cat.run_action(it["name"], it["params"])
print("VERDICT :", len(b.items), "véhicules posés sur la route")
