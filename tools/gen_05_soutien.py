"""Lot 05 : FARP, groupes aéronavals, ravitailleurs, AWACS, escortes et drones laser.

Plan radio (hors de la bande des tours : 250.0-256.9 et 340.2 en UHF, 38.4-38.6 en FM) :
  AWACS 282-286, ravitailleurs 290-296 (dernier chiffre = TACAN 50Y..56Y), porte-avions 305-307.
"""
import json

from lib import BLUE, RED, RED_CN, ROOT, Batch, land, sea, xy

b = Batch()

# ── FARP ─────────────────────────────────────────────────────────────────────
# Merizo : au sud de Guam, à 9 km du champ de tir hélicoptères de Talofofo.
FARPS = [("FARP Merizo", (-23450, -12150), 40.0, 1)]   # lot 19 : seule place plate et dégagée à 1,2 km (find_farp_spot.py)
for name, p, f, cs in FARPS:
    land(p, name, margin=300)
    b.act("add_farp", name=name, position=xy(p), **BLUE, farp_type="Invisible FARP", frequency_mhz=f,
          modulation="FM", callsign_id=cs)

# ── Groupes aéronavals ───────────────────────────────────────────────────────
# Stennis et Roosevelt (décision du 02/10/2026) en mer des Philippines, à l'ouest de Guam, cap au nord ;
# Tarawa à l'est de Rota, cap à l'est : à 67 km du champ de tir SEAD (SA-11 : 50 km), et à 109 km de Tinian
# pour que son escorteur Arleigh Burke (100 km) ne couvre aucune base rouge avec slots (lot 05d, check_portees.py).
CARRIERS = [
    dict(name="CSG-74 Stennis", carrier_type="Stennis", position=(40000, -110000), heading_deg=0, speed_kt=10,
         tower_mhz=305.0, tacan_channel=74, tacan_callsign="STN", icls_channel=11, link4_mhz=336.0,
         tanker_tacan_channel=55, tanker_tacan_callsign="S74", tanker_frequency_mhz=295.0,
         escorts=["TICONDEROG", "USS_Arleigh_Burke_IIa"]),
    dict(name="CSG-71 Roosevelt", carrier_type="CVN_71", position=(0, -135000), heading_deg=0, speed_kt=10,
         tower_mhz=306.0, tacan_channel=71, tacan_callsign="RSV", icls_channel=12, link4_mhz=337.0,
         tanker_tacan_channel=56, tanker_tacan_callsign="S71", tanker_frequency_mhz=296.0,
         escorts=["TICONDEROG", "USS_Arleigh_Burke_IIa"]),
    dict(name="ARG-1 Tarawa", carrier_type="LHA_Tarawa", position=(60000, 110000), heading_deg=90, speed_kt=8,
         tower_mhz=307.0, tacan_channel=73, tacan_callsign="TRW", icls_channel=13, link4_mhz=None,
         recovery_tanker=False, rescue_helicopter=True, escorts=["USS_Arleigh_Burke_IIa"]),
]
for c in CARRIERS:
    c = dict(c)
    p = c.pop("position")
    sea(p, c["name"], margin=20000)
    b.act("add_carrier_group", **BLUE, position=xy(p), **c)

# ── Ravitailleurs et AWACS ───────────────────────────────────────────────────
# nom, type, camp, a, b (hippodrome), FL, kt, MHz, rôle, TACAN (canal, indicatif), escorte (type, emport)
F15 = ("F-15C", {"payload": "AIM-9*4,AIM-120*4,Fuel"})
# add_air_group ne prend pas loadout_from, et le modèle « J-11A Template Red » du catalogue n'a aucun emport :
# emport du modèle v5 « veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1 » (tools/loadouts-v5.json)
_V5 = json.loads((ROOT / "tools/loadouts-v5.json").read_text(encoding="utf-8"))["groups"]
J11 = ("J-11A", {"pylons": _V5["veafSpawn-J-11A - FOX3 - ECM ON - Radar ON - HARD X1"]["pylons"]})
SUPPORT = [
    # paire ouest, loin du front
    ("Texaco 1", "KC-135", BLUE, (30000, -70000), (90000, -70000), 220, 400, 290.0, "Refueling", (50, "TX1"), F15),
    ("Arco 1", "KC135MPRS", BLUE, (-30000, -50000), (20000, -50000), 180, 380, 291.0, "Refueling", (51, "AR1"), F15),
    ("Magic 1", "E-3A", BLUE, (60000, -130000), (140000, -130000), 300, 360, 282.0, "AWACS", None, F15),
    # paire est, en mer à l'est de Saipan, pour les cibles du nord (escortées : décision du 11/10/2026)
    ("Texaco 2", "KC-135", BLUE, (190000, 265000), (250000, 265000), 240, 400, 292.0, "Refueling", (52, "TX2"), F15),
    ("Arco 2", "KC135MPRS", BLUE, (70000, 135000), (130000, 135000), 200, 380, 293.0, "Refueling", (53, "AR2"), F15),   # lot 18 : près du Tarawa
    ("Overlord 1", "E-3A", BLUE, (120000, 295000), (220000, 295000), 310, 360, 283.0, "AWACS", None, F15),
    # rouge
    ("Shell 1", "IL-78M", RED, (250000, 60000), (300000, 40000), 200, 380, 294.0, "Refueling", None, J11),
    ("Wizard 1", "KJ-2000", RED_CN, (330000, 60000), (400000, 60000), 300, 360, 284.0, "AWACS", None, J11),
    # arène (loin à l'ouest) : un AWACS par camp, sans escorte
    ("Darkstar 1", "E-3A", BLUE, (130000, -430000), (130000, -470000), 300, 360, 285.0, "AWACS", None, None),
    ("Focus 1", "A-50", RED, (300000, -430000), (300000, -470000), 300, 360, 286.0, "AWACS", None, None),
]
for n, typ, side, a, bb, fl, kt, f, task, beacon, esc in SUPPORT:
    b.act("add_air_group", **side, name=n, unit_type=typ, count=1, start="air", position=xy(a),
          altitude_ft=fl * 100, speed_kt=kt, frequency_mhz=f, task=task, skill="High")
    b.act("edit_route", group_name=n, operation="add", position=xy(bb), altitude_ft=fl * 100, speed_kt=kt)
    b.act("edit_route", group_name=n, operation="add_task", index=1, task="set_unlimited_fuel", task_params={"value": True})
    if beacon:
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="activate_beacon",
              task_params={"channel": beacon[0], "mode": "Y", "callsign": beacon[1], "bearing": True, "aa": True})
    if task == "Refueling":
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="tanker", task_params={})
    else:
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="awacs", task_params={})
        b.act("edit_route", group_name=n, operation="add_task", index=1, task="eplrs", task_params={"value": True})
    b.act("edit_route", group_name=n, operation="add_task", index=1, task="orbit",
          task_params={"pattern": "Race-Track", "altitude_ft": fl * 100, "speed_kt": kt})
    if esc:
        etype, loadout = esc
        en = n + " - Escort"
        b.act("add_air_group", **side, name=en, unit_type=etype, count=2, start="air",
              position=xy((a[0] - 3000, a[1] - 3000)), altitude_ft=fl * 100, speed_kt=kt, frequency_mhz=f,
              task="Escort", skill="High", **loadout)
        b.act("edit_route", group_name=en, operation="add_task", index=1, task="set_unlimited_fuel", task_params={"value": True})
        b.act("edit_route", group_name=en, operation="add_task", index=1, task="escort",
              task_params={"group_name": n, "engagement_distance_nm": 30})

# ── Drones de guidage laser (tâche de groupe AFAC, orbite en cercle) ─────────
DRONES = [
    ("Reaper 1", (15471, 6727)),              # au-dessus du champ de tir attaque de North West Field
    ("Reaper 2", (-26000, -15000)),           # posé sur Cocos, déplacé sur Talofofo (-18500, -4000) quand le champ de tir y est passé
]
for n, p in DRONES:
    b.act("add_air_group", **BLUE, name=n, unit_type="MQ-9 Reaper", count=1, start="air", position=xy(p),
          altitude_ft=10000, speed_kt=110, task="AFAC", skill="High")

b.save("05-soutien.json")
