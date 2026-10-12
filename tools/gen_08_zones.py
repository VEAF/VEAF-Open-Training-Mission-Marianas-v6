"""Lot 08 : les 16 vraies zones de combat (menu par type, training: false).

Toutes en territoire rouge (Tinian, Saipan, îles du nord, mer). Portées DCS des défenses actives :
SA-11 50 km, SA-6 25 km, HQ-7 15 km, Tor 12 km ; Type 054A 45 km, Type 052C 150 km. Aucune n'atteint une
base bleue, une piste de ravitailleur ou une zone d'entraînement (tools/check_portees.py).
Les zones ne se chevauchent pas : un groupe appartient à la zone dont il porte le préfixe ET le cercle.
"""
from lib import RED, RED_CN, Batch, cmd_unit, land, position_text, sea, spot, tankers_text, xy

ZONES = []   # (zone, centre, rayon, nom, menu, texte, coalition, catégorie, groupes, statiques)


def zone(name, c, r, fname, menu, text, groups, statics=(), side=RED, category="vehicle"):
    ZONES.append((name, c, r, fname, menu, text, side, category, groups, list(statics)))


def g_fake(c, items, tag):
    """Faux porteurs #command : (alias, porteur, relèvement, distance, balises)."""
    out = []
    for i, (alias, carrier, brg, dist, extra) in enumerate(items, 1):
        p = spot(c, brg, dist, f"{tag}-{i}")
        out.append({"name": f"{tag}-{i}", "position": xy(p), "keep_position": True,
                    "units": [cmd_unit(alias, carrier, f"{tag}-{i}", extra)]})
    return out


def g_native(c, name, brg, dist, units, route=None):
    p = spot(c, brg, dist, name)
    g = {"name": name, "position": xy(p), "keep_position": True, "units": units}
    if route:
        g["route"] = [xy(p)] + [xy(q) for q in route]
    return g


def s_items(c, items):
    """Statiques : (type, relèvement, distance)."""
    return [(typ, spot(c, brg, dist, typ)) for typ, brg, dist in items]


# ── Front ────────────────────────────────────────────────────────────────────
C = (170000, 94500)
zone("combatZone_TinianEst", C, 2000, "Z01 Front — Tinian, plages de l'est", "Front",
     "Le bataillon rouge qui tient la côte est de Tinian (Unai Dankulo) : blindés en position, infanterie et "
     "artillerie antiaérienne. Détruire les blindés ; défense de bataillon : artillerie antiaérienne, parfois des missiles courte portée à guidage infrarouge.",
     g_fake(C, [("-armor, defense 1", "ZTZ96B", 0, 600, ""),
                ("-armor, defense 2", "ZTZ96B", 140, 700, ""),
                ("-infantry, defense 1", "Infantry AK", 250, 500, ""),
                ("-zu23", "Ural-375 ZU-23", 300, 900, "")], "Z01"))   # pas -mortar : l'alias pose une équipe US
C = (184800, 100200)   # à 5 km de Saipan Intl : hors du sanctuaire rouge (2,5 km)
zone("combatZone_ChalanKanoa", C, 1500, "Z02 Front — Saipan, plages de Chalan Kanoa", "Front",
     "La ligne de défense côtière des plages ouest de Saipan, devant Chalan Kanoa et Susupe : blindés enterrés, "
     "infanterie mécanisée, artillerie antiaérienne. Détruire les blindés ; défense légère (ZU-23, Shilka, lance-missiles portatifs).",
     g_fake(C, [("-armor, defense 0", "ZTZ96B", 20, 500, ""),
                ("-armor, defense 1", "ZTZ96B", 170, 600, ""),
                ("-infantry, defense 2", "Infantry AK", 280, 400, ""),
                ("-shilka", "ZSU-23-4 Shilka", 90, 300, "")], "Z02"))
C = (185921, 106860)   # Kagman (Obyan, à 1,9 km de Saipan Intl, tombait dans le sanctuaire rouge)
zone("combatZone_Kagman", C, 1500, "Z03 Front — Saipan, artillerie de Kagman", "Front",
     "Le groupement d'artillerie rouge de la péninsule de Kagman, à l'est de Saipan, qui pilonne le détroit : "
     "obusiers PLZ-05 et lance-roquettes. Détruire les pièces ; défense SA-13 et artillerie antiaérienne.",
     g_fake(C, [("-plz05", "PLZ05", 0, 500, ""),
                ("-grad", "Grad-URAL", 120, 600, ""),
                ("-sa13", "Strela-10M3", 240, 400, ""),
                ("-zu23", "Ural-375 ZU-23", 300, 600, "")], "Z03"))

# ── SEAD ─────────────────────────────────────────────────────────────────────
C = (422349, 115380)   # Guguan : sur Farallon de Medinilla, DCS n'offre aucune place libre (sol « piste », sonde du 12/10)
zone("combatZone_Guguan", C, 1500, "Z04 SEAD — Guguan", "SEAD",
     "Le site sol-air que la force rouge a installé sur le volcan de Guguan, entre Sarigan et Alamagan : une batterie "
     "moyenne portée (SA-11) et un SA-15, qui couvrent l'approche des îles du nord.",
     g_fake(C, [("-sa11", "SA-11 Buk LN 9A310M1", 0, 0, ""),
                ("-sa15", "Tor 9A331", 120, 400, "")], "Z04"))
C = (196300, 109000)
zone("combatZone_Marpi", C, 1500, "Z05 SEAD — Saipan, Marpi", "SEAD",
     "Le site sol-air de la pointe nord de Saipan, à Marpi : une batterie moyenne portée tirée au sort (SA-6 ou "
     "HQ-7) et un SA-8, sous la couverture des défenses permanentes de Saipan.",
     g_fake(C, [("-sa6", "Kub 2P25 ln", 0, 0, '#spawngroup="Z05MR" #spawncount=1'),
                ("-hq7", "HQ-7_LN_SP", 90, 200, '#spawngroup="Z05MR" #spawncount=1'),
                ("-sa8", "Osa 9A33 ln", 200, 600, "")], "Z05"))

# ── Convois en mouvement (un groupe natif, route sur route, AAA dans le groupe) ──
C = (194325, 106691)
zone("combatZone_BeachRoad", C, 1000, "Z06 Convoi — Saipan, Beach Road", "Convois",
     "Un convoi logistique descend Beach Road, la route côtière ouest de Saipan, de San Roque vers Garapan et "
     "Susupe. L'arrêter avant le front ; il porte sa propre artillerie antiaérienne (ZU-23).",
     [g_native(C, "Convoi", 0, 0, [{"type": "BTR-82A", "count": 1}, {"type": "KAMAZ Truck", "count": 4},
                                    {"type": "Ural-375 ZU-23", "count": 1}, {"type": "Ural-4320-31", "count": 2}],
               route=[(189900, 101100), (184300, 99900)])])
C = (169800, 91400)   # sur Broadway, à 3,3 km de Tinian Intl : hors du sanctuaire rouge
zone("combatZone_Broadway", C, 600, "Z07 Convoi — Tinian, Broadway", "Convois",
     "Un convoi de carburant remonte Broadway, l'axe nord-sud de Tinian, du nord de l'aéroport vers North Field. Le "
     "détruire avant l'arrivée ; il porte sa propre artillerie antiaérienne.",
     [g_native(C, "Convoi", 0, 0, [{"type": "GAZ-66", "count": 1}, {"type": "ATZ-10", "count": 3},
                                    {"type": "Ural-375 ZU-23", "count": 1}, {"type": "ATZ-5", "count": 1}],
               route=[(172000, 91800), (174300, 92000)])])
C = (193236, 104693)   # Tanapag (Kagman accueille maintenant l'artillerie de Z03)
zone("combatZone_CrossIsland", C, 1000, "Z08 Convoi — Saipan, Cross Island Road", "Convois",
     "Des renforts traversent Saipan d'ouest en est, de Tanapag vers Kagman par Capitol Hill et Cross Island Road. Les arrêter ; "
     "le convoi est escorté par un SA-13.",
     [g_native(C, "Convoi", 0, 0, [{"type": "BTR-82A", "count": 2}, {"type": "ZBD04A", "count": 2},
                                    {"type": "Ural-4320-31", "count": 2}, {"type": "Strela-10M3", "count": 1}],
               route=[(190700, 104400), (187300, 105600), (186200, 106300)])])

# ── Frappes dans la profondeur ───────────────────────────────────────────────
C = (316600, 100300)
zone("combatZone_Anatahan", C, 1500, "Z09 Frappe — Anatahan, missiles côtiers", "Frappes en profondeur",
     "La batterie de missiles antinavires côtiers (HY-2) installée sur Anatahan, qui interdit l'approche nord de "
     "l'archipel aux navires bleus. Détruire les lanceurs et leur radar ; défense SA-15 et Shilka.",
     [g_native(C, "Batterie", 0, 0, [{"type": "hy_launcher", "count": 2}, {"type": "Silkworm_SR", "count": 1}])]
     + g_fake(C, [("-sa15", "Tor 9A331", 200, 500, ""), ("-shilka", "ZSU-23-4 Shilka", 60, 400, "")], "Z09"))
C = (189793, 101024)
zone("combatZone_Garapan", C, 800, "Z10 Frappe — Garapan, état-major", "Frappes en profondeur",
     "L'état-major de la force rouge à Garapan, la ville principale de Saipan : centre de commandement, "
     "antennes et abris. Tout détruire ; défense SA-15, dans la couverture des défenses permanentes de Saipan.",
     g_fake(C, [("-sa15", "Tor 9A331", 300, 500, ""), ("-zu23", "Ural-375 ZU-23", 120, 400, "")], "Z10"),
     statics=s_items(C, [(".Command Center", 0, 100), ("Comms tower M", 80, 250), ("Comms tower M", 200, 200),
                         ("Bunker", 160, 150), ("Bunker", 330, 180)]))
C = (355438, 108145)
zone("combatZone_Sarigan", C, 1200, "Z11 Frappe — Sarigan, station d'écoute", "Frappes en profondeur",
     "La station d'écoute et de relais radio de Sarigan, qui relaie les ordres vers les îles du nord. Détruire "
     "les antennes et le poste ; défense SA-8.",
     g_fake(C, [("-sa8", "Osa 9A33 ln", 90, 300, "")], "Z11"),
     statics=s_items(C, [("Comms tower M", 0, 150), ("Comms tower M", 120, 200), (".Command Center", 240, 100)]))
C = (454467, 114609)
zone("combatZone_Alamagan", C, 1500, "Z12 Frappe — Alamagan, dépôt avancé", "Frappes en profondeur",
     "Le dépôt avancé d'Alamagan, où la force rouge stocke le carburant et les munitions des îles du nord. Tout "
     "détruire ; défense HQ-7 et artillerie antiaérienne.",
     g_fake(C, [("-hq7", "HQ-7_LN_SP", 200, 500, ""), ("-zu23", "Ural-375 ZU-23", 30, 400, "")], "Z12", ),
     statics=s_items(C, [("Fuel tank", 0, 200), ("Fuel tank", 40, 300), ("Fuel tank", 80, 250),
                         ("FARP Ammo Dump Coating", 300, 250), ("FARP Ammo Dump Coating", 330, 350)]),
     side=RED_CN)

# ── Bases aériennes (OCA) ────────────────────────────────────────────────────
C = (174664, 92122)
zone("combatZone_NorthField", C, 2000, "Z13 OCA — Tinian, North Field", "Bases aériennes",
     "North Field, l'ancienne base des B-29 au nord de Tinian, rouverte par la force rouge : chasseurs J-11A et "
     "bombardiers H-6J au parking. Les détruire au sol ; défense HQ-7 et Shilka.",
     g_fake(C, [("-hq7", "HQ-7_LN_SP", 90, 700, ""), ("-shilka", "ZSU-23-4 Shilka", 250, 500, "")], "Z13"),
     statics=s_items(C, [("J-11A", 0, 200), ("J-11A", 0, 300), ("J-11A", 20, 400), ("H-6J", 180, 300),
                         ("H-6J", 200, 450)]),
     side=RED_CN)
C = (512410, 107565)
zone("combatZone_Pagan", C, 2000, "Z14 OCA — Pagan", "Bases aériennes",
     "La piste de Pagan, base arrière de la force rouge à l'extrême nord : J-11A et hélicoptères au parking. Les "
     "détruire au sol ; elle est sous la défense permanente de Pagan (SA-10, HQ-7).",
     g_fake(C, [("-sa15", "Tor 9A331", 300, 600, "")], "Z14"),
     statics=s_items(C, [("J-11A", 60, 250), ("J-11A", 70, 350), ("Mi-8MT", 240, 250), ("Mi-8MT", 250, 350)]))

# ── Antinavire ───────────────────────────────────────────────────────────────
C = (160500, 79000)
zone("combatZone_Amphibie", C, 3000, "Z15 Antinavire — groupe amphibie de Tinian", "Antinavire",
     "Le groupe amphibie rouge mouillé au sud-ouest de Tinian, prêt à débarquer sur Rota : deux bâtiments de "
     "débarquement et une frégate Type 054A. Les couler ; la frégate porte une défense sol-air moyenne portée.",
     [{"name": "Groupe", "position": xy(C), "keep_position": True,
       "units": [{"type": "Type_054A", "count": 1}, {"type": "BDK-775", "count": 2}]}],
     side=RED_CN, category="ship")
C = (330000, 20000)
zone("combatZone_Escadre", C, 5000, "Z16 Antinavire — escadre de surface", "Antinavire",
     "L'escadre de surface rouge en patrouille à l'ouest d'Anatahan : un destroyer Type 052C, un Type 052B et une "
     "frégate Type 054A. Les couler ; le Type 052C porte une défense sol-air de longue portée, à attaquer hors de "
     "son enveloppe.",
     [{"name": "Escadre", "position": xy(C), "keep_position": True, "patrol": True,
       "units": [{"type": "Type_052C", "count": 1}, {"type": "Type_052B", "count": 1}, {"type": "Type_054A", "count": 1}],
       "route": [xy(C), xy((360000, 20000))]}],
     side=RED_CN, category="ship")

if __name__ == "__main__":
    b = Batch()
    for name, c, r, fname, menu, text, side, cat, groups, statics in ZONES:
        if cat == "ship":
            sea(c, name, margin=3000)
        for g in groups:
            for q in g.get("route") or []:
                (sea if cat == "ship" else land)((q["x"], q["y"]), f"{name} route", 50 if cat != "ship" else 3000)
        cz = {"friendly_name": fname, "radio_group_name": menu, "training": False,
              "briefing": f"{text}\n{position_text(c)} {tankers_text(c)}"}
        b.act("create_combat_zone", zone_name=name, position=xy(c), radius=r, groups=groups, **side,
              category=cat, combat_zone=cz)
        for i, (typ, p) in enumerate(statics, 1):
            b.act("add_group", **side, category="static", name=f"Static-{typ.strip('.').split()[0]}-{i}",
                  position=xy(p), units=[{"type": typ}], for_combat_zone=name, keep_position=True)
    b.save("08-zones.json")
