"""Lot 06 : défense aérienne permanente des bases et des arrières (#veafInterpreter).

Porteur = le lanceur que génère l'alias (l'éditeur montre son cercle de portée), nom unique.
Portées DCS (list_unit_types, threat_range_m) : Patriot 100 km, Hawk 45 km, SA-10 120 km, SA-11 50 km,
Tor 12 km, HQ-7 15 km, Avenger 4,5 km. Le SA-10 rouge est à Pagan, pas à Saipan : à Marpi il couvrait
le Tarawa (91 km) et les pistes des ravitailleurs de l'est. Le contrôle des distances est check_portees.py.
"""
from lib import BLUE, RED, RED_CN, Batch, interp_unit, land, xy

# (camp, nom de groupe, position, alias, type du porteur, cap)
SITES = [
    # ── Bleu : Andersen (base mère) ──
    (BLUE, "AD Andersen Patriot", (9300, 12600), "-patriot", "Patriot ln", 30),
    (BLUE, "AD Andersen Hawk", (12300, 17000), "-hawk", "Hawk ln", 30),
    (BLUE, "AD Andersen Avenger 1", (10000, 16200), "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Andersen Avenger 2", (11400, 12500), "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "EWR Mont Santa Rosa", (5517, 12642), "-blue_ewr", "FPS-117 Dome", 0),
    # ── Bleu : Won Pat, Orote, FARP Merizo ──
    (BLUE, "AD Won Pat Hawk", (1800, 1900), "-hawk", "Hawk ln", 60),
    (BLUE, "AD Won Pat Avenger", (-1200, -1300), "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Orote NASAMS", (-4624, -15835), "-nasams", "NASAMS_LN_C", 60),
    (BLUE, "AD Orote Avenger", (-5200, -17900), "-avenger_squad", "M1097 Avenger", 0),
    (BLUE, "AD Merizo Stinger", (-23355, -12200), "-stinger", "Soldier stinger", 0),   # lot 19b
    # ── Rouge : Saipan ──
    (RED, "AD Saipan SA-11", (183300, 103300), "-sa11", "SA-11 Buk LN 9A310M1", 200),
    (RED, "AD Saipan SA-15 sud", (179300, 102900), "-sa15", "Tor 9A331", 0),
    (RED, "AD Saipan SA-15 nord", (190500, 104300), "-sa15", "Tor 9A331", 0),
    (RED_CN, "AD Saipan HQ-7", (181000, 100700), "-hq7", "HQ-7_LN_SP", 200),
    (RED, "EWR Mont Tapochau", (187468, 103469), "-ewr", "55G6 EWR", 0),
    # ── Rouge : Tinian ──
    (RED, "AD Tinian SA-11", (169500, 91700), "-sa11", "SA-11 Buk LN 9A310M1", 200),
    (RED, "AD Tinian SA-15", (165600, 89300), "-sa15", "Tor 9A331", 0),
    # ── Rouge : Pagan (arrière) et guet ──
    (RED, "AD Pagan SA-10", (514800, 108500), "-sa10", "S-300PS 5P85C ln", 180),
    (RED_CN, "AD Pagan HQ-7", (511400, 107173), "-hq7", "HQ-7_LN_SP", 180),
    (RED, "EWR Anatahan", (316360, 97326), "-ewr", "55G6 EWR", 0),
]

if __name__ == "__main__":
    b = Batch()
    for side, name, p, alias, carrier, hdg in SITES:
        land(p, name, margin=150)
        tag = name.replace("AD ", "").replace("EWR ", "EWR-").replace(" ", "-")
        b.act("add_group", **side, category="vehicle", name=name, position=xy(p), keep_position=True,
              units=[interp_unit(f"{alias}, hdg {hdg}", carrier, tag)])
    b.save("06-defense.json")
