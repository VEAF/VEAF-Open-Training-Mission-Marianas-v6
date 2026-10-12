"""Lot 10b : ce que la relecture du 11/10/2026 a trouvé dans la mission.

- porteurs H3-3 / H3-4 : un `-sa18` pose le type « SA-18 Igla manpad » (sa18_squad), pas « Igla-S » ;
- missions scénarisées : le raid de J-11A attaque Overlord 1, les Su-30 attaquent la défense aérienne d'Andersen
  (sans tâche, rien ne disait à ces groupes quoi viser).
"""
import gen_07_entrainement as e
from lib import RED, ROOT, Batch
from mcp import cat  # noqa: F401  (met VMCT sur sys.path)
from veaf_mission_mcp.mission_folder import load_folder_mission

ANDERSEN = {"x": 10575, "y": 14549}
b = Batch()
groups = next(z for z in e.ZONES if z[0] == "combatZone_Talofofo_Hard")[6]
for g in groups:
    if g["units"][0]["type"] == "SA-18 Igla manpad":
        b.act("remove_group", group_name=f"combatZone_Talofofo_Hard-{g['name']}")
        b.act("add_group", **RED, category="vehicle", name=g["name"], position=g["position"], units=g["units"],
              for_combat_zone="combatZone_Talofofo_Hard", keep_position=True)
# describe_units ne rend pas l'identifiant de groupe : lu dans la table de la mission
content = load_folder_mission(ROOT).mission_content
gid = next(g["groupId"] for sd in content["coalition"].values() for c in sd.get("country") or []
           for g in (c.get("plane") or {}).get("group") or [] if g["name"] == "Overlord 1")
b.act("edit_route", group_name="SC-Protect-Overlord-J11", operation="add_task", index=1, task_position=1,
      task="attack_group", task_params={"group_id": gid})
b.act("edit_route", group_name="SC-Defense-Andersen-SEAD", operation="add_task", index=1, task_position=1,
      task="engage_targets_in_zone", task_params={"position": ANDERSEN, "radius_m": 25000, "target_types": ["Air Defence"]})
b.save("10b-corrections.json")
