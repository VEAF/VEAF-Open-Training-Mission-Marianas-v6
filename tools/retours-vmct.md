# Retours pour VMCT — construction de l'OT Mariannes v6 (11/10/2026)

Tenu au fil de la construction (prompt `new-open-training-mission.fr.md`, veaf-tools 6.29.0, MCP sur `develop`).
Chaque entrée : quoi, où, comment je l'ai vu, ce que j'ai fait à la place.

1. **Pas de grille d'altitude pour MarianaIslands : aucun contrôle terre / mer.**
   `terrain_elevation` répond `available: false`, et `add_farp` avertit « surface not checked: no elevation grid for MarianaIslands ».
   Sur un théâtre fait d'îles, c'est le contrôle qui compte le plus : un groupe posé à 200 m du rivage peut être dans l'eau.
   Contourné par `tools/coastlines.py` : contours des îles téléchargés une fois depuis OpenStreetMap (Nominatim, objets `place=island`), puis test point-dans-polygone avant chaque placement (`lib.land` / `lib.sea`).
   OSM n'est pas le terrain de DCS : la grille (`veaf-tools dcs terrain-sweep MarianaIslands`) reste à balayer en jeu.
2. **`add_carrier_group` donne aux S-3B les indicatifs Texaco11 et Arco11.**
   Posés avant les ravitailleurs, ils ont pris les deux premières familles ; `add_air_group` a ensuite décalé chaque ravitailleur sur la famille suivante (« Texaco 1 » → Shell11, « Arco 1 » → Texaco21, « Texaco 2 » → Arco21, « Arco 2 » → Shell21), avec un avertissement par groupe.
   Corrigé par `set_unit_properties` (lot `05c-indicatifs.json`) : S-3B en Shell 5 / Shell 6, puis chaque ravitailleur sur son nom.
   L'action pourrait réserver une famille au S-3B qui ne soit pas celle qu'un ravitailleur nommé « Texaco 1 » réclamera.
3. **`add_air_group` n'accepte pas `loadout_from`**, alors que `create_qra` et `create_cap_mission` l'acceptent.
   Le lot 05 s'est arrêté à la première escorte rouge (`unknown parameter(s) loadout_from`) ; suite relancée à part (`05b-soutien-suite.json`) avec des `pylons`.
4. **Le modèle « J-11A Template Red » du catalogue livré (`dynamic-slot-templates.yaml`) n'a aucun emport**, et le J-11A n'a pas d'emport DCS nommé (`list_payloads`).
   Il n'y a donc aucune source d'emport J-11A dans les outils.
   Pris dans les modèles `veafSpawn-J-11A - …` de la v5 (`tools/loadouts-v5.json`).
5. **`geocode` rend le centre de l'île pour « Umatac, Guam » et « Hagåtña, Guam », et une rivière pour « Inarajan, Guam »**, sans le signaler (`osm_type` island / river).
   Les points de `tools/places.json` sont relus avant usage ; aucun de ces trois n'est utilisé.
6. **`terrain_elevation` prend `theatre`, toutes les autres actions `mission_path`.** Le premier appel échoue ; mineur.
7. **`create_qra` sur un théâtre sans données de parking : un aérodrome nommé est refusé, alors que sans aérodrome l'action se rabat sur un départ en vol.** Retiré du lot VMCT : c'est voulu (le code dit « a start or an airfield asked for is refused rather than quietly put in the air »).
   Avec `airfield: "Saipan Intl"` dans un groupe : `no parking data captured for theatre 'MarianaIslands'`, et le lot s'arrête. Sans `airfield`, la même action accepte et avertit « air start, not the runway ». La description annonce le repli ; il ne vaut que sans aérodrome explicite.
   Contourné en retirant `airfield` : les 12 groupes de QRA démarrent en vol au centre de leur cercle.
   Plus largement, MarianaIslands n'a pas de données de parking (limitation `no-parking-data-outside-three-theatres`) : aucune QRA ne décolle de sa piste.
8. **Un groupe de QRA créé avec `task: "CAP"` atterrit au lieu de défendre sa zone, sans erreur.**
   `create_qra` écrit sur l'unique point la tâche automatique `EngageTargets` de la tâche CAP (comme l'éditeur). Le build lit alors la route comme « qui engage par elle-même » (`builder.aircraft_route_engages_air`) et la laisse telle quelle, au lieu de donner au groupe le rôle `zone_defense`. Résultat : un seul point, pas d'orbite, donc atterrissage au terrain le plus proche (limitation `aircraft-at-the-end-of-its-route-lands`).
   Vu dans le journal du build : 12 lignes « engage les aéronefs par sa propre route : elle est suivie telle quelle ».
   Contourné par `edit_route clear_tasks` (lot `09b-qra-sans-tache.json`). `create_qra` devrait refuser `task` ou ne pas écrire cette tâche automatique, puisque sa propre description dit « no task on purpose ».
9. **`describe_mission` n'accepte qu'un `.miz`, pas un dossier de mission**, alors que le catalogue lui passe `mission_path` comme aux autres actions (`PermissionError` en ouvrant le dossier comme un zip). `describe_units` lit le dossier, mais s'arrête à 50 groupes sans filtre (`truncated`) : il faut filtrer par nom.
10. **Le catalogue livré de slots dynamiques (`dynamic-slot-templates.yaml`) contient trois mods : A-4E-C, OV-10A Bronco, T-45.** Leurs types sont absents de la base d'unités DCS (`list_unit_types`). Le prompt exige « aucun mod exigé », et la consigne « retire ceux d'une autre époque » ne les attrape pas. Retirés ici (`tools/gen_14_slots_dynamiques.py`). L'OT Syrie v6 les a gardés (A-4E-C, OV-10A, T-45 dans son catalogue).
11. **Aucune action ne règle ROE ni dispersion d'un groupe au sol.** Les cibles inertes des niveaux faciles (tir interdit, pas de dispersion) sont réglées par `tools/inert_targets.py`, qui réécrit la tâche du premier point dans la table de la mission (même méthode que `statics_to_groups.py` de GermanyCW et Syrie).
12. **Rôles sans avion toujours à 0** (FIX-OPEN-TRAINING-CAUCASUS-FINDINGS ticket 01, ouvert) : `tools/ground_control_roles.py` les met à 5 par camp et rend les véhicules pilotables.
13. ~~Une variante « réelle » sortie sans un nuage, sans un mot au build~~ — **retiré, c'était mon outil.** VMCT avertit bien (`weather.converter.metar_fetch_failed` ou `metar_fetch_empty`) et vole alors le ciel par défaut (base 2 000 m, sans nuage) ; mon `make_test_mission.py` jetait la sortie du build qui suivait. Il la garde maintenant dans `.veaf-backups/build-serveur.log`, et `verify.py` échoue quand deux variantes sont identiques.
14. **`describe_units` ne rend pas l'identifiant d'un groupe** (il a, lui, un paramètre `limit` : la coupure à 50 groupes n'est qu'un défaut), dont `edit_route add_task attack_group` a besoin (`group_id`). Lu dans la table de la mission (`gen_10b_corrections.py`).
