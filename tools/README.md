# Outils de la mission

Scripts Python qui ont construit la mission et qui produisent ce qu'on ne tape pas à la main : le briefing, les cartes, la mission de test, les contrôles.
Ils importent le code Python de VMCT : par défaut le dépôt voisin `../VEAF-Mission-Creation-Tools` (branche `develop`), ou le dossier désigné par la variable `VMCT_PY` (le dossier `src/python/veaf-tools` d'un autre checkout).
Ils se lancent depuis `tools/`, avec le Python de l'environnement poetry de VMCT :

```powershell
$PY = (poetry -C ..\..\VEAF-Mission-Creation-Tools env info -p) + "\Scripts\python.exe"
& $PY gather.py
```

## Construction (historique, à ne pas rejouer)

Chaque `gen_NN_*.py` écrit un lot d'actions `veaf-mission-mcp` dans `batches/`, que `mcp.py batch batches/<lot>.json` exécute dans le processus.
**Un lot ne se rejoue pas** : `add_group` ne dédoublonne pas, un second passage crée des doublons (les dessins F10, eux, sont refusés par nom).
Les lots `05b`, `05c`, `05d`, `06b`, `08b`, `09b`, `15b` corrigent ce que les premiers passages ont révélé ; `tools/retours-vmct.md` dit pourquoi.

| Script | Lot |
|---|---|
| `geocode_places.py`, `coastlines.py` | Lieux réels (`places.json`) et contours des îles d'OpenStreetMap (`coastlines.json`) : test terre / mer de chaque placement, faute de grille d'altitude VMCT pour cette carte |
| `gen_04_bases.py` | Camp des aérodromes, slots dynamiques |
| `gen_05_soutien.py` | FARP, porte-avions, ravitailleurs, AWACS, escortes, drones ; `gen_05c_indicatifs.py` remet les indicatifs |
| `gen_06_defense.py` | Défense aérienne permanente (`#veafInterpreter`) |
| `gen_07_entrainement.py` | Les 3 familles × 3 niveaux d'entraînement |
| `gen_08_zones.py`, `gen_08b_deplacements.py` | Les 16 vraies zones de combat ; déplacement de 4 d'entre elles hors des sanctuaires rouges |
| `gen_09_qra_cap.py` | QRA et CAP à la demande |
| `gen_10_joueurs.py` | Sanctuaires, arène, slots des ponts, groupes des missions scénarisées |
| `gen_11_config.py` | Blocs ASSETS, SANCTUARY et `combat_missions:` de `mission.yaml` |
| `gen_12_presets.py`, `gen_13_waypoints.py`, `gen_14_slots_dynamiques.py` | `src/presets.yaml`, `src/waypoints.yaml`, `src/dynamic-slot-templates.yaml` |
| `gen_15_identite.py`, `gen_16_dessins.py` | Date, bullseye, briefing DCS ; dessins F10 |
| `inert_targets.py`, `ground_control_roles.py` | Cibles inertes (tir interdit, sans dispersion) ; rôles sans avion à 5 par camp |

## Après tout changement

| Script | Ce qu'il fait |
|---|---|
| `sync_zones.py` | Réécrit le bloc `COMBATZONE` de `mission.yaml` (noms, menus, inclusions, briefings) depuis `gen_07` et `gen_08`, qui en sont la source |
| `gather.py` | Relève dans la mission tout ce que le briefing affiche → `briefing_data.json` |
| `gen_readme.py` | Écrit `README.md` (le briefing des pilotes) et redessine les cartes par `gen_map.py` |
| `gen_map.py` | Carte générale `docs/carte.jpg` et zooms `docs/cartes/` sur fond OpenStreetMap (tuiles en cache dans `tiles/`), copiés dans `src/mission/l10n/DEFAULT/` et déclarés dans la mission |
| `check_portees.py` | Portée de chaque défense et de chaque zone face à ce qu'elle ne doit pas atteindre → `docs/portees.md` ; ligne `VERDICT` |
| `verify.py` | Contrôles des `.miz` construits (noms, slots, soutien, porteurs, images, météo, sécurité) ; ligne `VERDICT` |
| `probe_scenery.py` | En jeu, par dcs-bridge : quels véhicules l'éditeur a posés dans les bois, en ville ou dans l'eau (avant toute activation de zone) ; ligne `VERDICT` |
| `probe_clear.py`, `apply_clear_moves.py` | En jeu : place libre la plus proche de chaque groupe bloqué (anneaux, petite requête Disposition), puis déplacement en restant dans la zone |
| `convoys_on_road.py` | En jeu : pose chaque véhicule des convois sur la route (`land.getClosestPointOnRoads`) |
| `find_farp_spot.py` | En jeu : place de FARP dégagée et plate près d'un point |
| `test_en_jeu.py` | En jeu : active chaque zone, compte ce qui apparaît (niveaux imbriqués), mesure les convois ; ligne `VERDICT` |
| `make_test_mission.py` | Mission de test locale `bridge/bridge-Marianas-OT.miz` (LOCAL_TEST, game master, A-10C II à Andersen, dcs-bridge), puis rebuild serveur |

Ordre : `sync_zones.py`, build serveur (`.\veaf-tools.exe mission build`), `gather.py`, `gen_readme.py`, rebuild serveur (les cartes sont dans le `.miz`), `check_portees.py`, `verify.py`.
