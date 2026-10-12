# Essais en jeu — 12/10/2026

Mission de test `bridge/bridge-Marianas-OT.miz` (profil LOCAL_TEST), DCS en solo, `dcs-serve` du dépôt VEAF-dcs-bridge, sondes par `/api/exec`.

## Terrain (`tools/probe_scenery.py`, avant toute activation de zone)

| | Avant | Après |
|---|---|---|
| Véhicules dans les arbres ou les bâtiments | 57 / 97 | 4 / 98 |
| Véhicules dans l'eau | 1 | 0 |
| Statiques dans l'eau | 0 / 27 | 0 / 27 |

- 51 groupes déplacés vers la place libre la plus proche (`probe_clear.py`, `apply_clear_moves.py` ; médiane 100 m), tous restés dans leur zone.
- Convois posés sur la route, véhicules à 25 m au moins les uns des autres (`convoys_on_road.py`).
- Z04 SEAD déplacée de Farallon de Medinilla (sol « piste » dans DCS, aucune place libre à 1,5 km) à Guguan.
- FARP Merizo : il était dans la jungle et sur une pente (capture de David) ; déplacé de 1,2 km sur la seule place plate et dégagée trouvée (`find_farp_spot.py`, dénivelé 2,5 m sur 80 m).
- Restent jugés « bloqués » : deux véhicules de convoi sur la chaussée en ville (Cross Island), deux faux porteurs d'alias (Anatahan, Tinian Est) à 25 m d'une place libre ; VEAF pose leurs unités.
- Non jugés : les 11 batteries permanentes (`#veafInterpreter`), vivantes dès le départ — la sonde compte les véhicules comme des obstacles.

## Zones (`tools/test_en_jeu.py`)

| Zone | Unités | |
|---|---|---|
| H1 / H2 / H3 Talofofo | 7 / 10 / 16 | chaque niveau s'ajoute au précédent |
| A1 / A2 / A3 North West Field | 10 / 16 / 25 | idem |
| S1 / S2 / S3 Rota | 10 / 15 / 16 | idem ; SA-6 ou SA-11 tiré au sort à chaque activation |
| Les 13 zones terrestres | 2 à 22 | toutes apparaissent |
| Z06 / Z07 / Z08 convois | | roulent : 110, 131 et 46 m en 30 s (Z08 démarre en ville) |
| Z15 / Z16 antinavire | 3 / 3 navires | apparaissent |

CAP « MiG-29 — Tinian » lancée par le menu : apparaît en vol au FL210, environ 200 m/s, et patrouille.

À noter : l'alias `-armor` (niveaux 3 et 4 du camp rouge moderne de VEAF) tire aussi des T-55, Chieftain, VAB Mephisto, ZSU-57 et des unités CurrentHill (T-64BV), intégrées à DCS : choix de VEAF, pas un défaut de la mission.

## Pas encore essayé

QRA (il faut un intrus bleu dans le cercle), missions scénarisées, sanctuaires (il faut des joueurs), drones laser, appontage, dessins F10 et ciel.
