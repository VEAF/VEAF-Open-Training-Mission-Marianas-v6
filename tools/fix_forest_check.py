"""Sort des forêts les groupes des champs de tir que `veaf-tools dcs forest-check` y trouve (16/11/2026).

Sur Guam et Rota, la jungle couvre presque tout : NWF n'a qu'environ 3 % de son cercle dégagé à 50 m alentour,
Talofofo 2 %. Aucun déplacement d'ensemble ne sort un champ de tir de la forêt ; chaque groupe va donc dans
la clairière la plus proche qui reste dans le cercle de sa zone, à 100 m au moins de tout autre groupe.
Place exigée, ni forêt ni eau sur tous les anneaux de 25 m jusqu'à : 100 m pour un marqueur Medium ou Hard (il fait
apparaître un groupe entier ; repli à 75 m quand rien n'existe à 100 m), 50 m pour une cible Easy. Les marqueurs
sont placés d'abord, les cibles Easy ensuite. Les déplacements vont de 10 m à 3,1 km.
Les valeurs sont le déplacement total de chaque groupe, mesuré entre la mission d'avant et celle d'après.
Exception : le Tor de Talofofo Hard (H4-1) est hors du cercle à dessein, à 13 km du FARP Merizo pour sa portée de
12 km ; il va dans la clairière la plus proche de sa place, pas dans le cercle.
Une seule fois : il refuse de repasser.
"""

import sys

from paths import ROOT  # noqa: F401  (met aussi le code VMCT sur sys.path)
from veaf_mission_mcp.actions import register_default_actions  # noqa: E402
from veaf_mission_mcp.catalog import ActionCatalog  # noqa: E402
from veaf_mission_mcp.mission_folder import load_folder_mission  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
M = ROOT.as_posix()
cat = ActionCatalog()
register_default_actions(cat)

#: groupe -> (décalage nord, décalage est), en mètres
MOVES = {
    "combatZone_NWF_Easy-Inert-BTR-82A-4": (18, 7),
    "combatZone_NWF_Easy-Inert-BTR-82A-5": (-95, 81),
    "combatZone_NWF_Easy-Inert-KAMAZ-8": (-31, 625),
    "combatZone_NWF_Easy-Inert-KAMAZ-9": (290, 957),
    "combatZone_NWF_Easy-Inert-T-72B3-1": (88, 416),
    "combatZone_NWF_Easy-Inert-T-72B3-2": (114, -55),
    "combatZone_NWF_Easy-Inert-T-72B3-3": (-43, 90),
    "combatZone_NWF_Easy-Inert-Ural-4320-31-10": (-352, 237),
    "combatZone_NWF_Easy-Inert-ZBD04A-6": (-95, 81),
    "combatZone_NWF_Easy-Inert-ZBD04A-7": (-427, 347),
    "combatZone_NWF_Easy-Static-Command-3": (-99, 13),
    "combatZone_NWF_Easy-Static-Fuel-1": (-5, -3),
    "combatZone_NWF_Easy-Static-Fuel-2": (-31, 121),
    "combatZone_NWF_Hard-A3-1": (-920, 1301),
    "combatZone_NWF_Hard-A3-2": (1845, 894),
    "combatZone_NWF_Hard-A3-3": (-81, 645),
    "combatZone_NWF_Hard-A3-4": (1043, 897),
    "combatZone_NWF_Medium-A2-1": (-304, 1242),
    "combatZone_NWF_Medium-A2-2": (-131, 401),
    "combatZone_NWF_Medium-A2-3": (356, 1014),
    "combatZone_Rota_Easy-S1-1": (-175, 13),
    "combatZone_Rota_Easy-S1-2": (-126, -20),
    "combatZone_Rota_Hard-S3-1": (-62, -546),
    "combatZone_Rota_Medium-S2-1": (67, 58),
    "combatZone_Rota_Medium-S2-2": (374, 25),
    "combatZone_Rota_Medium-S2-3": (-839, -137),
    "combatZone_Talofofo_Easy-Inert-BTR-82A-3": (-226, -403),
    "combatZone_Talofofo_Easy-Inert-BTR-82A-4": (-287, -8),
    "combatZone_Talofofo_Easy-Inert-KAMAZ-6": (556, 503),
    "combatZone_Talofofo_Easy-Inert-KAMAZ-7": (-896, 364),
    "combatZone_Talofofo_Easy-Inert-T-72B3-1": (-40, 176),
    "combatZone_Talofofo_Easy-Inert-T-72B3-2": (-1165, -495),
    "combatZone_Talofofo_Easy-Inert-ZBD04A-5": (-438, 460),
    "combatZone_Talofofo_Hard-H4-1": (84, -202),
    "combatZone_Talofofo_Hard-H4-2": (-2532, -1075),
    "combatZone_Talofofo_Hard-H4-3": (-283, -854),
    "combatZone_Talofofo_Medium-H2-1": (-2771, -1495),
    "combatZone_Talofofo_Medium-H2-2": (-750, -1377),
    "combatZone_Talofofo_Medium-H2-3": (-1470, -125),
    "combatZone_Talofofo_Medium-H2-4": (-498, 146),
    "combatZone_Talofofo_Medium-H3-1": (-1413, -1534),
    "combatZone_Talofofo_Medium-H3-2": (-1786, -225),
    "combatZone_Talofofo_Medium-H3-3": (-2158, -275),
    "combatZone_Talofofo_Medium-H3-4": (-367, -565),
}
GUARD = ("combatZone_Talofofo_Hard-H4-1", (-14199, -3003))


def as_list(t):
    return [t[k] for k in sorted(t)] if isinstance(t, dict) else (t or [])


content = load_folder_mission(ROOT).mission_content
groups = {
    g["name"]: g
    for co in content["coalition"].values()
    for c in as_list(co.get("country"))
    for kind in ("vehicle", "static")
    for g in as_list((c.get(kind) or {}).get("group"))
}
unit = as_list(groups[GUARD[0]]["units"])[0]
if (round(unit["x"]), round(unit["y"])) != GUARD[1]:
    sys.exit("déjà fait, ou les groupes ne sont plus à la place que ce script attend")

for name, (dx, dz) in MOVES.items():
    g = groups[name]
    res = cat.run_action(
        "set_group_properties", {"mission_path": M, "group_name": name, "move_to": {"x": g["x"] + dx, "y": g["y"] + dz}}
    )
    warn = res.get("warnings") if isinstance(res, dict) else None
    err = res.get("error") if isinstance(res, dict) else None
    print(f"{name}: +{dx} N, +{dz} E" + (f" — {warn}" if warn else "") + (f" — ERREUR {err}" if err else ""))
