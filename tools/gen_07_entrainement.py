"""Lot 07 : les 3 familles d'entraînement × 3 niveaux (facile ⊂ moyen ⊂ difficile, clé `includes:`).

H — hélicoptères, Talofofo (sud-est de Guam), à 9 km du FARP Merizo, 19 km de Won Pat et d'Orote.
    Difficile = SA-13 (5 km) et SA-18 (5,2 km) : rien ne touche le FARP (8,3 km au plus près, check_portees.py).
A — attaque, North West Field (champ de tir de la v5), à 93 nm du front. Centre décalé à l'ouest :
    10 km d'Andersen ; le difficile s'arrête au SA-13 et au SA-9 (5 km au plus).
S — SEAD, Rota (île évacuée, aérodrome neutre). SA-11 au plus (50 km) : Andersen à 70 km, Tarawa à 64 km,
    piste de ravitailleur la plus proche à plus de 100 km, Tinian à 106 km. Pas de longue portée (décision
    du 01/10/2026).

Cibles inertes des niveaux faciles : groupes d'un véhicule nommés « …-Inert-… », rendus chauds, tir interdit
et sans dispersion par tools/inert_targets.py (aucune action MCP ne règle ROE ni dispersion).
"""
from lib import RED, Batch, cmd_unit, position_text, spot, tankers_text, xy

H = (-18500, -4000)
A = (15200, 5500)
S = (73500, 44500)


def inert(zone_center, items, prefix):
    """Groupes d'un véhicule, en couronne autour du centre : (type, relèvement, distance)."""
    groups = []
    for i, (typ, brg, dist) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{prefix}{i}")
        groups.append({"name": f"Inert-{typ.split()[0]}-{i}", "position": xy(p), "keep_position": True,
                       "units": [{"type": typ, "count": 1}]})
    return groups


def fake(zone_center, items, tagbase):
    """Faux porteurs #command : (alias, type du porteur, relèvement, distance, balises de tirage)."""
    groups = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(zone_center, brg, dist, f"{tagbase}-{i}")
        groups.append({"name": f"{tagbase}-{i}", "position": xy(p), "keep_position": True,
                       "units": [cmd_unit(alias, carrier, f"{tagbase}-{i}", extra)]})
    return groups


ZONES = [
    # ── H : hélicoptères ──
    ("combatZone_Talofofo_Easy", H, 2500, "H1 Hélico Talofofo — facile", "Entraînement hélicoptères", None,
     inert(H, [("T-72B3", 0, 600), ("T-72B3", 60, 700), ("BTR-82A", 120, 500), ("BTR-82A", 180, 800),
               ("ZBD04A", 240, 600), ("KAMAZ Truck", 300, 700), ("KAMAZ Truck", 330, 400)], "H1-"),
     "Champ de tir hélicoptères dans les collines de Talofofo, au sud-est de Guam, à 5 nm du FARP Merizo : "
     "cibles inertes (chars, blindés et camions immobiles, tir interdit)."),
    ("combatZone_Talofofo_Medium", H, 2500, "H2 Hélico Talofofo — moyen", "Entraînement hélicoptères",
     "combatZone_Talofofo_Easy",
     fake(H, [("-zu23", "Ural-375 ZU-23", 30, 1200, '#spawngroup="H2AAA" #spawncount=2'),
              ("-zu23", "Ural-375 ZU-23", 150, 1100, '#spawngroup="H2AAA" #spawncount=2'),
              ("-zu23", "Ural-375 ZU-23", 270, 1300, '#spawngroup="H2AAA" #spawncount=2'),
              ("-shilka", "ZSU-23-4 Shilka", 210, 900, "#spawnchance=50")], "H2"),
     "Champ de tir hélicoptères de Talofofo : de l'artillerie antiaérienne légère (ZU-23, parfois un Shilka) "
     "en plus des cibles du niveau facile."),
    ("combatZone_Talofofo_Hard", H, 2500, "H3 Hélico Talofofo — difficile", "Entraînement hélicoptères",
     "combatZone_Talofofo_Medium",
     fake(H, [("-sa13", "Strela-10M3", 90, 1000, '#spawngroup="H3SR" #spawncount=1'),
              ("-sa13", "Strela-10M3", 300, 1000, '#spawngroup="H3SR" #spawncount=1'),
              ("-sa18", "SA-18 Igla manpad", 0, 1500, '#spawngroup="H3MP" #spawncount=1'),
              ("-sa18", "SA-18 Igla manpad", 200, 1400, '#spawngroup="H3MP" #spawncount=1')], "H3"),
     "Champ de tir hélicoptères de Talofofo, avec une défense courte portée réaliste : un SA-13 et une équipe "
     "de lance-missiles portatifs SA-18, à guidage infrarouge."),
    # ── A : attaque ──
    ("combatZone_NWF_Easy", A, 2500, "A1 Attaque North West Field — facile", "Entraînement attaque", None,
     inert(A, [("T-72B3", 0, 700), ("T-72B3", 40, 900), ("T-72B3", 80, 600), ("BTR-82A", 120, 800),
               ("BTR-82A", 160, 500), ("ZBD04A", 200, 700), ("ZBD04A", 240, 900), ("KAMAZ Truck", 280, 600),
               ("KAMAZ Truck", 320, 800), ("Ural-4320-31", 350, 400)], "A1-"),
     "Champ de tir air-sol de North West Field, à 5 nm à l'ouest d'Andersen : blindés et camions immobiles en "
     "tir interdit, dépôt de carburant et poste de commandement."),
    ("combatZone_NWF_Medium", A, 2500, "A2 Attaque North West Field — moyen", "Entraînement attaque",
     "combatZone_NWF_Easy",
     fake(A, [("-armor, defense 0", "T-72B3", 220, 1300, ""),
              ("-zu23", "Ural-375 ZU-23", 60, 1500, '#spawngroup="A2AAA" #spawncount=1'),
              ("-zu23", "Ural-375 ZU-23", 300, 1400, '#spawngroup="A2AAA" #spawncount=1')], "A2"),
     "Champ de tir de North West Field : une compagnie blindée active et de l'artillerie antiaérienne légère "
     "en plus des cibles du niveau facile."),
    ("combatZone_NWF_Hard", A, 2500, "A3 Attaque North West Field — difficile", "Entraînement attaque",
     "combatZone_NWF_Medium",
     fake(A, [("-armor, defense 1", "T-72B3", 260, 1600, ""),
              ("-sa13", "Strela-10M3", 200, 1200, '#spawngroup="A3SR" #spawncount=1'),
              ("-sa9", "Strela-1 9P31", 320, 1200, '#spawngroup="A3SR" #spawncount=1'),
              ("-shilka", "ZSU-23-4 Shilka", 250, 800, "")], "A3"),
     "Champ de tir de North West Field : un second groupe blindé et une défense courte portée à guidage "
     "infrarouge (SA-13 ou SA-9), avec un Shilka. Pas de radar à longue portée : Andersen est à 5 nm."),
    # ── S : SEAD ──
    ("combatZone_Rota_Easy", S, 3000, "S1 SEAD Rota — facile", "Entraînement SEAD", None,
     fake(S, [("-sa6", "Kub 2P25 ln", 0, 0, '#spawngroup="S1MR" #spawncount=1'),
              ("-sa11", "SA-11 Buk LN 9A310M1", 90, 300, '#spawngroup="S1MR" #spawncount=1')], "S1"),
     "Site SEAD de Rota (île évacuée, plateau de Sabana) : une batterie sol-air moyenne portée, SA-6 ou "
     "SA-11 tirée au sort, avec son canon antiaérien de protection rapprochée."),
    ("combatZone_Rota_Medium", S, 3000, "S2 SEAD Rota — moyen", "Entraînement SEAD", "combatZone_Rota_Easy",
     fake(S, [("-sa15", "Tor 9A331", 45, 1500, '#spawngroup="S2SR" #spawncount=2'),
              ("-sa8", "Osa 9A33 ln", 165, 1500, '#spawngroup="S2SR" #spawncount=2'),
              ("-sa15", "Tor 9A331", 285, 1500, '#spawngroup="S2SR" #spawncount=2')], "S2"),
     "Site SEAD de Rota : la batterie moyenne portée est protégée par une défense courte portée (SA-15, SA-8)."),
    ("combatZone_Rota_Hard", S, 3000, "S3 SEAD Rota — difficile", "Entraînement SEAD", "combatZone_Rota_Medium",
     fake(S, [("-ewr", "55G6 EWR", 120, 2200, "")], "S3"),
     "Site SEAD de Rota en réseau Skynet : un radar d'alerte avancée guide les batteries, qui restent éteintes "
     "jusqu'au dernier moment."),
]

# Statiques du niveau facile attaque : ce qui ne vit pas (dépôt, poste de commandement)
A1_STATICS = [("Fuel tank", 100, 1100), ("Fuel tank", 110, 1200), (".Command Center", 20, 1300)]

if __name__ == "__main__":
    b = Batch()
    for zone, c, r, fname, menu, inc, groups, text in ZONES:
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": True,
              "briefing": f"{text}\n{position_text(c)} {tankers_text(c)}"}
        if inc:
            cz["includes"] = [inc]
        b.act("create_combat_zone", zone_name=zone, position=xy(c), radius=r, groups=groups, **RED,
              category="vehicle", combat_zone=cz)
    for i, (typ, brg, dist) in enumerate(A1_STATICS, 1):
        p = spot(A, brg, dist, f"A1-static-{i}")
        b.act("add_group", **RED, category="static", name=f"Static-{typ.strip('.').split()[0]}-{i}",
              position=xy(p), units=[{"type": typ}], for_combat_zone="combatZone_NWF_Easy", keep_position=True)
    b.save("07-entrainement.json")
