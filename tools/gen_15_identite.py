"""Lot 15 : date, bullseye commun et briefing DCS de la mission."""
from lib import BULLSEYE, Batch, xy

SITUATION = """VEAF Open Training — Mariannes (moderne, mars 2026).
Une force rouge sino-russe a pris les Mariannes du Nord, de Tinian et Saipan jusqu'à Pagan ; les États-Unis tiennent Guam. Rota, évacuée, sert de champ de tir entre les deux. Le front est le détroit entre Rota et Tinian ; bullseye commun : l'île d'Aguijan.

BASES BLEUES (slots dynamiques) : Andersen AFB (U250.1 / V126.2, TACAN 54X), Won Pat (U340.2 / V118.1), Olf Orote (pas de tour dans DCS), FARP Merizo (FM 40.0).
PORTE-AVIONS : Stennis U305.0, TACAN 74X, ICLS 11, Link 4 336.0 ; Roosevelt U306.0, 71X, ICLS 12, Link 4 337.0 ; Tarawa U307.0, 73X, ICLS 13.
SOUTIEN : AWACS Magic 1 U282.0 (ouest) et Overlord 1 U283.0 (est). Ravitailleurs ouest : Texaco 1 (perche) 50Y U290.0 FL220, Arco 1 (panier) 51Y U291.0 FL180 ; est : Texaco 2 (perche) 52Y U292.0 FL240, Arco 2 (panier) 53Y U293.0 FL200 ; S-3B Shell 5 (55Y U295.0) et Shell 6 (56Y U296.0). Drones laser : Reaper 1 (code 1511, FM 35.55) sur North West Field, Reaper 2 (1512, FM 35.6) sur Talofofo.

ENTRAÎNEMENT (menu F10 VEAF, zones) : H Talofofo (hélicoptères), A North West Field (attaque), S Rota (SEAD), trois niveaux chacun.
COMBAT : 16 zones (front, SEAD, convois, frappes, bases aériennes, antinavire), chacune avec son briefing dans le menu. Missions à la demande : CAP rouges et bleues, défense d'Andersen, interception d'un transport VIP, protection d'Overlord 1.
QRA rouges : Saipan/Tinian (25 nm) et Pagan (30 nm) ; QRA bleue : Guam (30 nm). Décollage 90 s après l'entrée du premier intrus ; elles ignorent les hélicoptères.
JOUEURS CONTRE JOUEURS : libre hors des sanctuaires. Sanctuaires bleus : Guam (33 km) et le champ de tir de Rota (12 km) ; rouges : 2,5 km autour des pistes de Saipan et de Tinian. Un intrus y est détruit après 60 s ; un missile tiré sur un défenseur est détruit. Arène à l'ouest, slots en vol Fox 1 et Fox 3.

Plan radio, cartes et détail de chaque zone : voir les images du briefing et le README de la mission.

METAR : ${METAR}"""

BLUE_TASK = ("Reprendre l'initiative depuis Guam : s'entraîner sur les champs de tir H, A et S, puis frapper les zones de "
             "combat des Mariannes du Nord. Andersen est la base mère ; le Tarawa, à l'est de Rota, est le pont le plus "
             "proche du front.")
RED_TASK = ("Tenir les Mariannes du Nord. Bases rouges avec slots : Saipan (U256.9 / V125.7) et Tinian (U250.05 / V123.65). "
            "AWACS Wizard 1 U284.0, ravitailleur Shell 1 (IL-78) U294.0 FL200. Arène : AWACS Focus 1 U286.0.")

if __name__ == "__main__":
    b = Batch()
    b.act("set_mission_date", date="2026-03-15", start_time="09:00")
    for side in ("blue", "red"):
        b.act("set_bullseye", coalition=side, position=xy(BULLSEYE))
    b.act("set_briefing", sortie="VEAF Open Training — Mariannes", situation=SITUATION, blue_task=BLUE_TASK,
          red_task=RED_TASK)
    b.save("15-identite.json")
