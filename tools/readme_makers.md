## Pour les créateurs de mission

Construite de zéro le 11/10/2026 avec VEAF Mission Creation Tools (`veaf-tools` 6.29.0) et le serveur MCP `veaf-mission-mcp`, d'après le prompt Open Training de VMCT, en s'inspirant de l'Open Training Mariannes v5 (`VEAF-Open-Training-Mission-Marianas`) sans la recopier : front Guam / Saipan-Tinian, champ de tir de North West Field, zone hélicoptères au sud de Guam, porte-avions, arène et esprit repris ; Rota rendue neutre (champ de tir SEAD), mission moderne seulement (plus d'appareils WW2 ni de mods), les 400 slots classiques de la v5 remplacés par des slots dynamiques (restent en slots classiques les ponts des porte-avions et l'arène).

### Construire

```powershell
# outils et scripts VEAF installés par l'updater (veaf-tools.exe + published/, hors dépôt)
.\veaf-tools.exe mission validate

# configuration serveur : sécurité active, logs info, 16 variantes météo dans missions/
.\veaf-tools.exe mission build

# essais sur un poste : sécurité coupée, logs debug, noms de groupes lisibles, pas de variantes
.\veaf-tools.exe mission build --profile LOCAL_TEST
```

Après un build `LOCAL_TEST`, refaire un build serveur avant de committer : le profil réécrit `src/scripts/veaf-config.lua`.

Mission de test locale (game master par camp, A-10C II en slot classique au sol moteur chaud à Andersen, pont dcs-bridge) : `tools/make_test_mission.py` → `bridge/bridge-Marianas-OT.miz`. Les slots dynamiques ne marchent qu'en multijoueur.

### Fichiers

| Fichier | Rôle |
|---|---|
| `mission.yaml` | Identité, sécurité, profil `LOCAL_TEST`, modules, zones (niveaux imbriqués par `includes:`), QRA, CAP, missions scénarisées, actifs, sanctuaires |
| `src/mission/` | La mission DCS éclatée (groupes, zones de déclenchement, aérodromes, dessins F10, briefing) |
| `src/presets.yaml` | Plan radio bleu et rouge ; canaux d'aérodromes aux fréquences que DCS donne aux tours |
| `src/versions.yaml` | Variantes météo et heure (METAR réel de PGUA, dégagé, épars, pluie) |
| `src/waypoints.yaml` | Points de navigation injectés dans les appareils joueurs |
| `src/warehouses.yaml` | Bases qui offrent des slots (`exclude_airports` pour les autres), carburant et munitions illimités |
| `src/dynamic-slot-templates.yaml` | Appareils proposés en slots dynamiques : modernes seulement, sans mods |
| `ctld-config.yaml` | CTLD 2.2.0 ; `jtacLaserCodeMax` abaissé pour les codes imposés des drones |
| `docs/carte.jpg`, `docs/cartes/` | La carte de ce briefing et ses zooms (fond OpenStreetMap) ; les mêmes images sont dans `src/mission/l10n/DEFAULT/` pour le briefing DCS, listées côté bleu et neutre seulement |
| `docs/portees.md` | Tableau des portées : chaque défense et chaque zone face à ce qu'elle ne doit pas atteindre |
| `tools/` | Scripts qui ont construit la mission (lots `gen_*`), et ceux qui produisent briefing, cartes et contrôles (voir `tools/README.md`) |

### Régénérer ce document

Ce README est **généré depuis la mission**. Après tout changement, depuis le dossier `tools/`, avec le Python de l'environnement poetry de VMCT :

```powershell
python sync_zones.py      # bloc COMBATZONE de mission.yaml (noms, menus, briefings) depuis gen_07 et gen_08
python gather.py          # mission -> tools/briefing_data.json
python gen_readme.py      # ce README, et les cartes (gen_map.py)
python check_portees.py   # tableau docs/portees.md (ligne VERDICT)
python verify.py          # contrôles des .miz construits (ligne VERDICT)
```

### Limites connues

- **Aucun contrôle du terrain de DCS** : VMCT n'a pas de grille d'altitude ni de données de parking pour la carte Mariannes. Les placements à terre et en mer sont vérifiés contre les contours des îles d'OpenStreetMap (`tools/coastlines.py`), pas contre DCS. À vérifier en jeu : véhicules dans l'eau, les bois ou les bâtiments, routes des convois, dessins F10, aspect du ciel.
- **Les QRA décollent en vol**, au centre de leur cercle : sans données de parking, elles ne peuvent pas partir de leur piste.
- Les portées utilisées pour le contrôle des défenses sont le `threat_range_m` de la base d'unités DCS livrée avec VMCT.
- Les missions scénarisées n'ont pas de condition de réussite ou d'échec (le YAML ne sait pas en porter).
- Codes laser des drones : comme sur l'OT Syrie, `jtacLaserCodeMax: 1686` et des Reaper en bas de plage (1511, 1512), sur la fréquence que CTLD en déduit (35.55 et 35.6 FM).
- Le briefing DCS ne montre les cartes qu'aux camps bleu et neutre (un pilote rouge identifié par DCS peut n'en avoir aucune) : sinon un pilote dont DCS ignore le camp les verrait deux fois.
