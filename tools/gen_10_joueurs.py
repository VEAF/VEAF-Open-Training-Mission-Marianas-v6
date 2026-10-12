"""Lot 10 : sanctuaires, arène, slots sur les ponts, groupes des missions scénarisées.

Sanctuaires (cercles tirés de zones de déclenchement) : Guam entier et le champ de tir SEAD de Rota côté bleu ;
2,5 km autour des pistes de Saipan et de Tinian côté rouge (aucune zone de combat n'y entre, lot 08b).
Arène : loin à l'ouest en pleine mer, slots en vol des deux camps par type de missile (Fox 1, Fox 3).
"""
import json

from lib import BLUE, RED, RED_CN, ROOT, Batch, xy

V5 = json.loads((ROOT / "tools/loadouts-v5.json").read_text(encoding="utf-8"))["groups"]
TPL = json.loads((ROOT / "tools/template_pylons.json").read_text(encoding="utf-8"))


def v5(name):
    return {"pylons": V5[name]["pylons"]}


SANCTUARIES = [
    ("Sanctuaire Guam", "SANCT-Guam", (-5000, 0), 33000, "BLUE"),
    ("Sanctuaire Rota", "SANCT-Rota", (73500, 44500), 12000, "BLUE"),
    ("Sanctuaire Saipan", "SANCT-Saipan", (180035, 101856), 2500, "RED"),
    ("Sanctuaire Tinian", "SANCT-Tinian", (166860, 89957), 2500, "RED"),
]

ARENA = ((215000, -450000), 74000)   # centre, rayon (40 nm)
ARENA_SLOTS = [
    # nom, camp, type, position, cap, emport
    ("Arène bleue F/A-18C Fox 1 #1", BLUE, "FA-18C_hornet", (160000, -460000), 0, v5("veafSpawn-F/A18C - FOX1 - Radar ON - ECM ON - NORMAL X2")),
    ("Arène bleue F/A-18C Fox 1 #2", BLUE, "FA-18C_hornet", (160000, -455000), 0, v5("veafSpawn-F/A18C - FOX1 - Radar ON - ECM ON - NORMAL X2")),
    ("Arène bleue F-16C Fox 3 #1", BLUE, "F-16C_50", (160000, -445000), 0, {"pylons": TPL["F-16CM Template"]}),
    ("Arène bleue F-16C Fox 3 #2", BLUE, "F-16C_50", (160000, -440000), 0, {"pylons": TPL["F-16CM Template"]}),
    ("Arène rouge Su-27 Fox 1 #1", RED, "Su-27", (270000, -460000), 180, v5("veafSpawn-SU27 - FOX1 - Radar ON - ECM OFF - NORMAL X2")),
    ("Arène rouge Su-27 Fox 1 #2", RED, "Su-27", (270000, -455000), 180, v5("veafSpawn-SU27 - FOX1 - Radar ON - ECM OFF - NORMAL X2")),
    ("Arène rouge J-11A Fox 3 #1", RED_CN, "J-11A", (270000, -445000), 180, v5("veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1")),
    ("Arène rouge J-11A Fox 3 #2", RED_CN, "J-11A", (270000, -440000), 180, v5("veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1")),
]

DECKS = [
    # porte-avions, nom du groupe, type, nombre, départ
    ("CSG-74 Stennis", "Stennis F/A-18C #1", "FA-18C_hornet", 2, "deck-cold"),
    ("CSG-74 Stennis", "Stennis F/A-18C #2", "FA-18C_hornet", 2, "deck-cold"),
    ("CSG-74 Stennis", "Stennis F/A-18C #3", "FA-18C_hornet", 2, "deck-hot"),
    ("CSG-71 Roosevelt", "Roosevelt F/A-18C #1", "FA-18C_hornet", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F-14B #1", "F-14B", 2, "deck-cold"),
    ("CSG-71 Roosevelt", "Roosevelt F-14B #2", "F-14B", 2, "deck-hot"),
    ("ARG-1 Tarawa", "Tarawa AV-8B #1", "AV8BNA", 2, "deck-cold"),
    ("ARG-1 Tarawa", "Tarawa AV-8B #2", "AV8BNA", 2, "deck-hot"),
]

ANDERSEN = (10575, 14549)
# Missions scénarisées : groupes en activation différée (combat_missions: de mission.yaml)
SCENARIO = [
    # nom, camp, type, nombre, départ, altitude ft, kt, tâche, emport, points suivants
    ("SC-Defense-Andersen-SEAD", RED, "Su-30", 2, (150000, 70000), 20000, 480, "SEAD",
     {"payload": "Kh-31P*4,R-73*2,R-77*2,ECM"}, [(60000, 35000), ANDERSEN]),
    ("SC-Defense-Andersen-Tu22", RED, "Tu-22M3", 2, (165000, 80000), 25000, 450, "Ground Attack",
     {"payload": "FAB-250*69"}, [(70000, 40000), ANDERSEN]),
    ("SC-Defense-Andersen-Escort", RED_CN, "J-11A", 2, (163000, 78000), 26000, 450, "Escort",
     v5("veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1"), [(70000, 40000), ANDERSEN]),
    ("SC-Intercept-VIP-Il76", RED, "IL-76MD", 1, (182000, 103000), 18000, 350, "Transport",
     {}, [(350000, 105000), (505000, 107000)]),
    ("SC-Intercept-VIP-Escort", RED_CN, "J-11A", 2, (180000, 101000), 20000, 350, "Escort",
     v5("veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1"), [(350000, 103000), (505000, 105000)]),
    ("SC-Protect-Overlord-J11", RED_CN, "J-11A", 4, (330000, 200000), 30000, 500, "CAP",
     v5("veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1"), [(250000, 270000), (170000, 295000)]),
]

if __name__ == "__main__":
    b = Batch()
    for name, zone, c, r, side in SANCTUARIES:
        b.act("add_trigger_zone", name=zone, position=xy(c), radius=r)
    b.act("add_trigger_zone", name="Arene", position=xy(ARENA[0]), radius=ARENA[1])
    for name, side, typ, p, hdg, loadout in ARENA_SLOTS:
        b.act("add_air_group", **side, name=name, unit_type=typ, count=2, start="air", position=xy(p),
              altitude_ft=25000, speed_kt=450, heading_deg=hdg, skill="Client", task="CAP", **loadout)
    for carrier, name, typ, n, start in DECKS:
        b.act("add_air_group", **BLUE, name=name, unit_type=typ, count=n, start=start, carrier=carrier,
              skill="Client", task="CAP")
    for name, side, typ, n, p, alt, kt, task, loadout, route in SCENARIO:
        b.act("add_air_group", **side, name=name, unit_type=typ, count=n, start="air", position=xy(p),
              altitude_ft=alt, speed_kt=kt, task=task, skill="High", late_activation=True, **loadout)
        for q in route:
            b.act("edit_route", group_name=name, operation="add", position=xy(q), altitude_ft=alt, speed_kt=kt)
    b.act("edit_route", group_name="SC-Defense-Andersen-Tu22", operation="add_task", index=3, task="bombing",
          task_params={"position": xy(ANDERSEN), "expend": "All", "attack_qty": 1})
    for esc, target in [("SC-Defense-Andersen-Escort", "SC-Defense-Andersen-Tu22"),
                        ("SC-Intercept-VIP-Escort", "SC-Intercept-VIP-Il76")]:
        b.act("edit_route", group_name=esc, operation="add_task", index=1, task="escort",
              task_params={"group_name": target, "engagement_distance_nm": 30})
    b.save("10-joueurs.json")
