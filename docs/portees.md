# Portées des défenses — contrôle de tools/check_portees.py

Portée = `threat_range_m` du lanceur dans la base d'unités DCS (cercles de l'éditeur). Distance = au plus proche de ce que l'arme ne doit pas atteindre (base adverse avec slots ; pour une zone, aussi les pistes des ravitailleurs bleus et les zones d'entraînement des autres familles).

| Type | Groupe ou zone | Arme | Portée (km) | Cible la plus proche | Distance (km) | |
|---|---|---|---|---|---|---|
| permanent | AD Andersen Avenger 1 | M1097 Avenger | 4.5 | Tinian Intl | 173.4 | ✅ |
| permanent | AD Andersen Avenger 2 | M1097 Avenger | 4.5 | Tinian Intl | 173.8 | ✅ |
| permanent | AD Andersen Hawk | Hawk ln | 45.0 | Tinian Intl | 170.9 | ✅ |
| permanent | AD Andersen Patriot | Patriot ln | 100.0 | Tinian Intl | 175.5 | ✅ |
| permanent | AD Merizo Stinger | Soldier stinger | 4.5 | Tinian Intl | 215.9 | ✅ |
| permanent | AD Orote Avenger | M1097 Avenger | 4.5 | Tinian Intl | 203.0 | ✅ |
| permanent | AD Orote NASAMS | NASAMS_LN_C | 15.0 | Tinian Intl | 201.5 | ✅ |
| permanent | AD Pagan HQ-7 | HQ-7_LN_SP | 15.0 | CSG-74 Stennis (route) | 436.6 | ✅ |
| permanent | AD Pagan SA-10 | S-300PS 5P85C ln | 120.0 | CSG-74 Stennis (route) | 440.2 | ✅ |
| permanent | AD Saipan HQ-7 | HQ-7_LN_SP | 15.0 | ARG-1 Tarawa (route) | 121.3 | ✅ |
| permanent | AD Saipan SA-11 | SA-11 Buk LN 9A310M1 | 50.0 | ARG-1 Tarawa (route) | 123.6 | ✅ |
| permanent | AD Saipan SA-15 nord | Tor 9A331 | 12.0 | ARG-1 Tarawa (route) | 130.6 | ✅ |
| permanent | AD Saipan SA-15 sud | Tor 9A331 | 12.0 | ARG-1 Tarawa (route) | 119.4 | ✅ |
| permanent | AD Tinian SA-11 | SA-11 Buk LN 9A310M1 | 50.0 | ARG-1 Tarawa (route) | 110.7 | ✅ |
| permanent | AD Tinian SA-15 | Tor 9A331 | 12.0 | ARG-1 Tarawa (route) | 107.6 | ✅ |
| permanent | AD Won Pat Avenger | M1097 Avenger | 4.5 | Tinian Intl | 191.2 | ✅ |
| permanent | AD Won Pat Hawk | Hawk ln | 45.0 | Tinian Intl | 187.1 | ✅ |
| permanent | ARG-1 Tarawa | LHA_Tarawa | 20.0 | Tinian Intl | 108.7 | ✅ |
| permanent | ARG-1 Tarawa | USS_Arleigh_Burke_IIa | 100.0 | Tinian Intl | 108.7 | ✅ |
| permanent | CSG-71 Roosevelt | CVN_71 | 25.0 | Tinian Intl | 236.9 | ✅ |
| permanent | CSG-71 Roosevelt | TICONDEROG | 100.0 | Tinian Intl | 236.9 | ✅ |
| permanent | CSG-71 Roosevelt | USS_Arleigh_Burke_IIa | 100.0 | Tinian Intl | 236.9 | ✅ |
| permanent | CSG-74 Stennis | Stennis | 25.0 | Tinian Intl | 202.9 | ✅ |
| permanent | CSG-74 Stennis | TICONDEROG | 100.0 | Tinian Intl | 202.9 | ✅ |
| permanent | CSG-74 Stennis | USS_Arleigh_Burke_IIa | 100.0 | Tinian Intl | 202.9 | ✅ |
| zone | combatZone_Alamagan | HQ-7_LN_SP | 15.0 | piste Texaco 2 | 253.5 | ✅ |
| zone | combatZone_Alamagan | Ural-375 ZU-23 | 2.5 | piste Texaco 2 | 254.0 | ✅ |
| zone | combatZone_Amphibie | BDK-775 | 6.0 | piste Arco 2 | 64.1 | ✅ |
| zone | combatZone_Amphibie | Type_054A | 45.0 | piste Arco 2 | 63.8 | ✅ |
| zone | combatZone_Anatahan | Tor 9A331 | 12.0 | piste Texaco 2 | 177.6 | ✅ |
| zone | combatZone_Anatahan | ZSU-23-4 Shilka | 2.5 | piste Texaco 2 | 177.5 | ✅ |
| zone | combatZone_BeachRoad | Ural-375 ZU-23 | 2.5 | piste Arco 2 | 70.3 | ✅ |
| zone | combatZone_Broadway | Ural-375 ZU-23 | 2.5 | piste Arco 2 | 58.2 | ✅ |
| zone | combatZone_ChalanKanoa | SA-18 Igla manpad | 5.2 | piste Arco 2 | 65.2 | ✅ |
| zone | combatZone_ChalanKanoa | Strela-10M3 | 5.0 | piste Arco 2 | 64.3 | ✅ |
| zone | combatZone_ChalanKanoa | ZSU-23-4 Shilka | 2.5 | piste Arco 2 | 64.7 | ✅ |
| zone | combatZone_CrossIsland | Strela-10M3 | 5.0 | piste Arco 2 | 70.3 | ✅ |
| zone | combatZone_Escadre | Type_052B | 30.0 | piste Arco 2 | 231.2 | ✅ |
| zone | combatZone_Escadre | Type_052C | 150.0 | piste Arco 2 | 230.7 | ✅ |
| zone | combatZone_Escadre | Type_054A | 45.0 | piste Arco 2 | 231.7 | ✅ |
| zone | combatZone_Garapan | Tor 9A331 | 12.0 | piste Arco 2 | 69.2 | ✅ |
| zone | combatZone_Garapan | Ural-375 ZU-23 | 2.5 | piste Arco 2 | 68.4 | ✅ |
| zone | combatZone_Guguan | SA-11 Buk LN 9A310M1 | 50.0 | piste Texaco 2 | 228.2 | ✅ |
| zone | combatZone_Guguan | Tor 9A331 | 12.0 | piste Texaco 2 | 227.8 | ✅ |
| zone | combatZone_Kagman | Strela-10M3 | 5.0 | piste Arco 2 | 62.6 | ✅ |
| zone | combatZone_Kagman | Ural-375 ZU-23 | 2.5 | piste Arco 2 | 63.1 | ✅ |
| zone | combatZone_Marpi | HQ-7_LN_SP | 15.0 | piste Arco 2 | 71.1 | ✅ |
| zone | combatZone_Marpi | Kub 2P25 ln | 25.0 | piste Arco 2 | 71.2 | ✅ |
| zone | combatZone_Marpi | Osa 9A33 ln | 10.3 | piste Arco 2 | 70.8 | ✅ |
| zone | combatZone_NWF_Hard | Strela-1 9P31 | 4.2 | Andersen AFB | 11.0 | ✅ |
| zone | combatZone_NWF_Hard | Strela-10M3 | 5.0 | Andersen AFB | 10.1 | ✅ |
| zone | combatZone_NWF_Hard | ZSU-23-4 Shilka | 2.5 | Andersen AFB | 10.6 | ✅ |
| zone | combatZone_NWF_Medium | Strela-10M3 | 5.0 | Andersen AFB | 10.4 | ✅ |
| zone | combatZone_NWF_Medium | Ural-375 ZU-23 | 2.5 | Andersen AFB | 9.4 | ✅ |
| zone | combatZone_NorthField | HQ-7_LN_SP | 15.0 | piste Arco 2 | 61.4 | ✅ |
| zone | combatZone_NorthField | ZSU-23-4 Shilka | 2.5 | piste Arco 2 | 62.3 | ✅ |
| zone | combatZone_Pagan | Tor 9A331 | 12.0 | piste Texaco 2 | 306.5 | ✅ |
| zone | combatZone_Rota_Easy | Kub 2P25 ln | 25.0 | ARG-1 Tarawa (route) | 66.9 | ✅ |
| zone | combatZone_Rota_Easy | SA-11 Buk LN 9A310M1 | 50.0 | ARG-1 Tarawa (route) | 66.6 | ✅ |
| zone | combatZone_Rota_Medium | Osa 9A33 ln | 10.3 | ARG-1 Tarawa (route) | 66.2 | ✅ |
| zone | combatZone_Rota_Medium | Tor 9A331 | 12.0 | ARG-1 Tarawa (route) | 66.1 | ✅ |
| zone | combatZone_Sarigan | Osa 9A33 ln | 10.3 | piste Texaco 2 | 188.7 | ✅ |
| zone | combatZone_Talofofo_Hard | SA-18 Igla manpad | 5.2 | FARP Merizo | 8.5 | ✅ |
| zone | combatZone_Talofofo_Hard | Strela-10M3 | 5.0 | FARP Merizo | 9.1 | ✅ |
| zone | combatZone_Talofofo_Medium | Ural-375 ZU-23 | 2.5 | FARP Merizo | 8.4 | ✅ |
| zone | combatZone_Talofofo_Medium | ZSU-23-4 Shilka | 2.5 | FARP Merizo | 8.8 | ✅ |
| zone | combatZone_TinianEst | SA-18 Igla manpad | 5.2 | piste Arco 2 | 57.3 | ✅ |
| zone | combatZone_TinianEst | Strela-10M3 | 5.0 | piste Arco 2 | 55.7 | ✅ |
| zone | combatZone_TinianEst | Ural-375 ZU-23 | 2.5 | piste Arco 2 | 57.2 | ✅ |
