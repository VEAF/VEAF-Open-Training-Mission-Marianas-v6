"""Lot 11 : blocs ASSETS et SANCTUARY de mission.yaml, et missions scénarisées (combat_missions:).

Un nom partout : nom de groupe = indicatif = libellé de preset = texte ASSETS. Chaque camp ne voit que ses
moyens (coalition). Les drones : code laser imposé et fréquence que CTLD calcule pour ce code (35.55 / 35.6 FM,
mesuré sur Syrie v6, limitation ctld-jtac-imposed-code-and-radio).
"""
import re

from gen_10_joueurs import SANCTUARIES
from lib import M
from mcp import cat

ASSETS = [
    ("Magic 1", "Magic 1 (E-3A) — AWACS ouest", "BLUE", "U282.0 — FL300 — orbite à l'ouest de Guam et Rota", "Magic 1 - Escort"),
    ("Overlord 1", "Overlord 1 (E-3A) — AWACS est", "BLUE", "U283.0 — FL310 — orbite à l'est de Saipan", "Overlord 1 - Escort"),
    ("Texaco 1", "Texaco 1 (KC-135, perche) — ouest", "BLUE", "TACAN 50Y TX1 — U290.0 — FL220 — piste à l'ouest de Rota", "Texaco 1 - Escort"),
    ("Arco 1", "Arco 1 (KC-135 MPRS, panier) — ouest", "BLUE", "TACAN 51Y AR1 — U291.0 — FL180 — piste à l'ouest de Guam", "Arco 1 - Escort"),
    ("Texaco 2", "Texaco 2 (KC-135, perche) — est", "BLUE", "TACAN 52Y TX2 — U292.0 — FL240 — piste à l'est de Farallon de Medinilla", "Texaco 2 - Escort"),
    ("Arco 2", "Arco 2 (KC-135 MPRS, panier) — détroit", "BLUE", "TACAN 53Y AR2 — U293.0 — FL200 — piste au nord-est de Rota, près du Tarawa", "Arco 2 - Escort"),
    ("CSG-74 Stennis", "CVN-74 Stennis", "BLUE", "TACAN 74X STN — ICLS 11 — Link 4 336.0 — ACLS — U305.0", None),
    ("CSG-71 Roosevelt", "CVN-71 Roosevelt", "BLUE", "TACAN 71X RSV — ICLS 12 — Link 4 337.0 — ACLS — U306.0", None),
    ("ARG-1 Tarawa", "LHA-1 Tarawa", "BLUE", "TACAN 73X TRW — ICLS 13 — U307.0", None),
    ("CSG-74 Stennis S3B-Tanker", "Shell 5 — S-3B du Stennis (ravitailleur embarqué)", "BLUE", "TACAN 55Y S74 — U295.0", None),
    ("CSG-71 Roosevelt S3B-Tanker", "Shell 6 — S-3B du Roosevelt (ravitailleur embarqué)", "BLUE", "TACAN 56Y S71 — U296.0", None),
    ("Darkstar 1", "Darkstar 1 (E-3A) — AWACS bleu de l'arène", "BLUE", "U285.0 — FL300", None),
    ("Wizard 1", "Wizard 1 (KJ-2000) — AWACS rouge", "RED", "U284.0 — FL300 — orbite entre Anatahan et Sarigan", "Wizard 1 - Escort"),
    ("Shell 1", "Shell 1 (IL-78M) — ravitailleur rouge", "RED", "U294.0 — FL200 — orbite au nord-ouest de Saipan", "Shell 1 - Escort"),
    ("Focus 1", "Focus 1 (A-50) — AWACS rouge de l'arène", "RED", "U286.0 — FL300", None),
]
DRONES = [
    ("Reaper 1", "Reaper 1 (drone laser) — North West Field", 1511, "35.55",
     "Laser 1511 — FM 35.55. 3 000 m sol au-dessus du champ de tir attaque (zone A)."),
    ("Reaper 2", "Reaper 2 (drone laser) — Talofofo", 1512, "35.6",
     "Laser 1512 — FM 35.6. 3 000 m sol au-dessus du champ de tir hélicoptères (zone H)."),
]

assets = []
for i, (name, desc, side, info, linked) in enumerate(ASSETS, 1):
    a = {"sort": i, "name": name, "description": desc, "coalition": side, "information": info}
    if linked:
        a["linked"] = linked
    assets.append(a)
for name, desc, code, freq, info in DRONES:
    assets.append({"sort": len(assets) + 1, "name": name, "description": desc, "coalition": "BLUE", "information": info,
                   "jtac": code, "freq": freq, "mod": "FM"})
print(cat.run_action("set_mission_module", {"mission_yaml_path": M + "/mission.yaml", "module_id": "ASSETS",
                                             "value": {"enabled": True, "assets": assets}}))
sanct = [{"name": n, "trigger_zone": z, "coalition": side, "delay_warning": 0, "delay_instant": 60,
          "protect_from_missiles": True} for n, z, c, r, side in SANCTUARIES]
print(cat.run_action("set_mission_module", {"mission_yaml_path": M + "/mission.yaml", "module_id": "SANCTUARY",
                                             "value": {"enabled": True, "sanctuary_zones": sanct}}))

COMBAT_MISSIONS = '''
# ── Missions scénarisées (module COMBATMISSION) — écrites par tools/gen_11_config.py ──
combat_missions:
- name: Defense-Andersen
  friendly_name: Défense — raid sur Andersen
  secured: false
  briefing: "Deux Su-30 armés de missiles antiradar ouvrent la route à deux Tu-22M3 escortés de J-11A, partis de Tinian vers Andersen. Abattez les bombardiers avant le largage.\nÉchec si la base est bombardée (constaté par vous : la mission ne le vérifie pas)."
  elements:
  - name: SEAD
    groups:
    - SC-Defense-Andersen-SEAD
    scalable: false
  - name: Bombardiers
    groups:
    - SC-Defense-Andersen-Tu22
    scalable: false
  - name: Escorte
    groups:
    - SC-Defense-Andersen-Escort
    scalable: true
- name: Interception-VIP
  friendly_name: Interception — transport VIP de Saipan à Pagan
  secured: false
  briefing: "Un IL-76 emmène l'état-major de la force rouge de Saipan vers Pagan, escorté par deux J-11A. Interceptez-le avant Pagan : la fin de la route est sous le SA-10 de Pagan."
  elements:
  - name: Transport
    groups:
    - SC-Intercept-VIP-Il76
    scalable: false
  - name: Escorte
    groups:
    - SC-Intercept-VIP-Escort
    scalable: true
- name: Protection-Overlord
  friendly_name: Protection — raid de J-11A sur Overlord 1
  secured: false
  briefing: "Quatre J-11A arrivent de la mer, au nord-est de Saipan, pour abattre l'AWACS Overlord 1 sur son orbite, à l'est de Saipan. Interceptez-les avant qu'ils ne l'atteignent ; son escorte de F-15C ne suffira pas."
  elements:
  - name: Raid
    groups:
    - SC-Protect-Overlord-J11
    scalable: true
'''
path = M + "/mission.yaml"
t = open(path, encoding="utf-8").read()
t = re.sub(r"\n# ── Missions scénarisées \(module COMBATMISSION\).*", "", t, flags=re.S)
open(path, "w", encoding="utf-8").write(t.rstrip("\n") + "\n" + COMBAT_MISSIONS)
print("combat_missions écrites")
