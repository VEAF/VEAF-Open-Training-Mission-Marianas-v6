---------------------------------------------------------------------------------------------------------------------------------------------
-- Généré par veaf-tools build depuis mission.yaml
-- Ne pas éditer manuellement.
-- Relancez 'veaf-tools build' ou 'veaf-tools generate-config' pour régénérer.
---------------------------------------------------------------------------------------------------------------------------------------------

-- ── Mission identity ─────────────────────────────────────────────────────────
veaf.config.MISSION_NAME = "VEAF_OpenTraining_Marianas_ICAO_PGUA"
veaf.config.era = veaf.ERA.MODERN
veaf.silenceAtcOnAllAirbases()
veaf.HideNamesFromSpawnedGroups = true

veaf.config.language = "fr"

-- ── Airfield channels of the mission's radio plan (src/presets.yaml, `bases`) ──────
if veafAirbases then
    veafAirbases.MissionChannels = {
        [2] = { alias = "Base-Saipan Intl", title = "Saipan Intl", uhf = 256.9, vhf = 125.7, fm = 38.45 },
        [3] = { alias = "Base-Tinian Intl", title = "Tinian Intl", uhf = 250.05, vhf = 123.65, fm = 38.5 },
        [4] = { alias = "Base-Antonio B. Won Pat Intl", title = "Antonio B. Won Pat Intl", uhf = 340.2, vhf = 118.1, fm = 38.55 },
        [6] = { alias = "Base-Andersen AFB", title = "Andersen AFB / 54X", uhf = 250.1, vhf = 126.2, fm = 38.6 },
    }
end

-- ── Global log level ─────────────────────────────────────────────────────────
veaf.ForcedLogLevel = "info"

-- ── CTLD 2 ───────────────────────────────────────────────────────────────────
-- Configuration lives in ctld-config.yaml (edit it with ctld-tools); this only starts it.
veaf.config.manage_airbase_logistics = true
veaf.config.airbase_logistics_radius = 1500
veaf.config.airbase_occupation_radius = 2000
veaf.config.airbase_logistics_tick = 30
-- One module's initialisation error must not take the others down (FIX-DEMO-MISSION-FINDINGS 02).
local function veafGuardedInit(name, initialize)
    local ok, err = xpcall(initialize, function(e)
        if debug and debug.traceback then
            return debug.traceback(tostring(e), 2)
        end
        return tostring(e)
    end)
    if not ok then
        veaf.loggers.get(veaf.Id):error("%s init failed: %s", name, err)
    end
end

veafGuardedInit("CTLD", function()
if ctld then
    veaf.ctld_initialize()
end
end)

-- ── Module configuration + initialization ────────────────────────────────────

-- ── Core ──

veafGuardedInit("SECURITY", function()
if veafSecurity then
    veafSecurity.initialize()
end
end)

veafGuardedInit("RADIO", function()
if veafRadio then
    veafRadio.initialize(true)
end
end)

veafGuardedInit("SHORTCUTS", function()
if veafShortcuts then
    veafShortcuts.initialize()
end
end)

veafGuardedInit("NAMEDPOINTS", function()
if veafNamedPoints then
    veafNamedPoints.initialize({})
end
end)

veafGuardedInit("SPAWN", function()
if veafSpawn then
    veafSpawn.initialize()
end
end)

-- ── Combat ──

veafGuardedInit("CARRIER", function()
if veafCarrierOperations then
    veafCarrierOperations.initialize(true)
end
end)

veafGuardedInit("CASMISSION", function()
if veafCasMission then
    veafCasMission.initialize()
end
end)

veafGuardedInit("TRANSPORTMISSION", function()
if veafTransportMission then
    veafTransportMission.initialize()
end
end)

veafGuardedInit("COMBATMISSION", function()
if veafCombatMission then
    veafCombatMission.addCapMission("CAP-Tinian-MiG29", "CAP rouge MiG-29 (Fox 1) — Tinian — FL220", "Deux MiG-29S armés de R-27R et R-73 patrouillent au-dessus de Tinian et d'Aguijan, au FL220. Emport : R-73*4,R-27R*2.", false, true)
    veafCombatMission.addCapMission("CAP-Saipan-J11", "CAP rouge J-11A (Fox 3) — Saipan — FL250", "Deux J-11A armés de R-77 et R-73 patrouillent à l'est de Saipan, au FL250.", false, true)
    veafCombatMission.addCapMission("CAP-Anatahan-MiG31", "CAP rouge MiG-31 (intercepteur haut et rapide) — Anatahan — FL400", "Deux MiG-31 patrouillent haut et vite entre Anatahan et Sarigan, au FL400. Emport : R-40R*2,R-33*4.", false, true)
    veafCombatMission.addCapMission("Raid-Saipan-Tu22", "Raid rouge Tu-22M3 à intercepter — nord de Saipan — FL250", "Deux Tu-22M3 chargés de bombes tournent au nord de Saipan, au FL250, prêts à frapper Guam : les intercepter. Emport : FAB-250*69.", false, true)
    veafCombatMission.addCapMission("CAP-Guam-F16", "CAP bleue F-16 (Fox 3) — nord de Guam — FL220", "Deux F-16C patrouillent au nord de Guam, entre North West Field et le détroit de Rota, au FL220. Emport : AIM-120C*4, AIM-9M*2, Fuel.", false, true)
    veafCombatMission.addCapMission("CAP-Tarawa-F15", "CAP bleue F-15 (Fox 3) — Tarawa — FL250", "Deux F-15C couvrent le groupe amphibie du Tarawa, à l'est de Rota, au FL250. Emport : AIM-9*4,AIM-120*4,Fuel.", false, true)
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Defense-Andersen")
        :setFriendlyName("Défense — raid sur Andersen")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Deux Su-30 armés de missiles antiradar ouvrent la route à deux Tu-22M3 escortés de J-11A, partis de Tinian vers Andersen. Abattez les bombardiers avant le largage. Échec si la base est bombardée (constaté par vous : la mission ne le vérifie pas).]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("SEAD")
            :setGroups({"SC-Defense-Andersen-SEAD"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Bombardiers")
            :setGroups({"SC-Defense-Andersen-Tu22"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Defense-Andersen-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Interception-VIP")
        :setFriendlyName("Interception — transport VIP de Saipan à Pagan")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Un IL-76 emmène l'état-major de la force rouge de Saipan vers Pagan, escorté par deux J-11A. Interceptez-le avant Pagan : la fin de la route est sous le SA-10 de Pagan.]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Transport")
            :setGroups({"SC-Intercept-VIP-Il76"})
            :setScalable(false)
        )
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Escorte")
            :setGroups({"SC-Intercept-VIP-Escort"})
            :setScalable(true)
        )
    )
    veafCombatMission.AddMissionsWithSkillAndScale(
        VeafCombatMission:new()
        :setName("Protection-Overlord")
        :setFriendlyName("Protection — raid de J-11A sur Overlord 1")
        :setSecured(false)
        :setRadioMenuEnabled(true)
        :setBriefing([[Quatre J-11A arrivent de la mer, au nord-est de Saipan, pour abattre l'AWACS Overlord 1 sur son orbite, à l'est de Saipan. Interceptez-les avant qu'ils ne l'atteignent ; son escorte de F-15C ne suffira pas.]])
        :addElement(
            VeafCombatMissionElement:new()
            :setName("Raid")
            :setGroups({"SC-Protect-Overlord-J11"})
            :setScalable(true)
        )
    )
    veafCombatMission.initialize()
end
end)

veafGuardedInit("COMBATZONE", function()
if veafCombatZone then
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Talofofo_Easy")
        :setFriendlyName("H1 Hélico Talofofo — facile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères dans les collines de Talofofo, au sud-est de Guam, à 5 nm du FARP Merizo : cibles inertes (chars, blindés et camions immobiles, tir interdit).
Position : bullseye 207°/103 nm (N13°19.051' E144°45.729'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 25 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 44 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Talofofo_Medium")
        :setFriendlyName("H2 Hélico Talofofo — moyen")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères de Talofofo : de l'artillerie antiaérienne légère (ZU-23, parfois un Shilka) en plus des cibles du niveau facile.
Position : bullseye 207°/103 nm (N13°19.051' E144°45.729'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 25 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 44 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Talofofo_Hard")
        :setFriendlyName("H3 Hélico Talofofo — difficile")
        :setRadioGroupName("Entraînement hélicoptères")
        :setBriefing([[Champ de tir hélicoptères de Talofofo, avec une défense courte portée réaliste : un SA-13 et une équipe de lance-missiles portatifs SA-18, à guidage infrarouge.
Position : bullseye 207°/103 nm (N13°19.051' E144°45.729'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 25 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 44 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_NWF_Easy")
        :setFriendlyName("A1 Attaque North West Field — facile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir air-sol de North West Field, à 5 nm à l'ouest d'Andersen : blindés et camions immobiles en tir interdit, dépôt de carburant et poste de commandement.
Position : bullseye 210°/84 nm (N13°37.367' E144°50.825'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 30 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 42 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_NWF_Medium")
        :setFriendlyName("A2 Attaque North West Field — moyen")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir de North West Field : une compagnie blindée active et de l'artillerie antiaérienne légère en plus des cibles du niveau facile.
Position : bullseye 210°/84 nm (N13°37.367' E144°50.825'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 30 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 42 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_NWF_Hard")
        :setFriendlyName("A3 Attaque North West Field — difficile")
        :setRadioGroupName("Entraînement attaque")
        :setBriefing([[Champ de tir de North West Field : un second groupe blindé et une défense courte portée à guidage infrarouge (SA-13 ou SA-9), avec un Shilka. Pas de radar à longue portée : Andersen est à 5 nm.
Position : bullseye 210°/84 nm (N13°37.367' E144°50.825'). Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 30 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 42 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Rota_Easy")
        :setFriendlyName("S1 SEAD Rota — facile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD de Rota (île évacuée, plateau de Sabana) : une batterie sol-air moyenne portée, SA-6 ou SA-11 tirée au sort, avec son canon antiaérien de protection rapprochée.
Position : bullseye 207°/47 nm (N14°09.152' E145°12.203'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 49 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 62 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Rota_Medium")
        :setFriendlyName("S2 SEAD Rota — moyen")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD de Rota : la batterie moyenne portée est protégée par une défense courte portée (SA-15, SA-8).
Position : bullseye 207°/47 nm (N14°09.152' E145°12.203'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 49 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 62 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Rota_Hard")
        :setFriendlyName("S3 SEAD Rota — difficile")
        :setRadioGroupName("Entraînement SEAD")
        :setBriefing([[Site SEAD de Rota en réseau Skynet : un radar d'alerte avancée guide les batteries, qui restent éteintes jusqu'au dernier moment.
Position : bullseye 207°/47 nm (N14°09.152' E145°12.203'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 49 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 62 nm.]])
        :setTraining(true)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_TinianEst")
        :setFriendlyName("Z01 Front — Tinian, plages de l'est")
        :setRadioGroupName("Front")
        :setBriefing([[Le bataillon rouge qui tient la côte est de Tinian (Unai Dankulo) : blindés en position, infanterie et artillerie antiaérienne. Détruire les blindés ; défense de bataillon : artillerie antiaérienne, parfois des missiles courte portée à guidage infrarouge.
Position : bullseye 030°/12 nm (N15°01.670' E145°39.675'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 31 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 93 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_ChalanKanoa")
        :setFriendlyName("Z02 Front — Saipan, plages de Chalan Kanoa")
        :setRadioGroupName("Front")
        :setBriefing([[La ligne de défense côtière des plages ouest de Saipan, devant Chalan Kanoa et Susupe : blindés enterrés, infanterie mécanisée, artillerie antiaérienne. Détruire les blindés ; défense légère (ZU-23, Shilka, lance-missiles portatifs).
Position : bullseye 026°/20 nm (N15°09.715' E145°42.808'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 35 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 89 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Kagman")
        :setFriendlyName("Z03 Front — Saipan, artillerie de Kagman")
        :setRadioGroupName("Front")
        :setBriefing([[Le groupement d'artillerie rouge de la péninsule de Kagman, à l'est de Saipan, qui pilonne le détroit : obusiers PLZ-05 et lance-roquettes. Détruire les pièces ; défense SA-13 et artillerie antiaérienne.
Position : bullseye 034°/23 nm (N15°10.343' E145°46.523'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 34 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 85 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Guguan")
        :setFriendlyName("Z04 SEAD — Guguan")
        :setRadioGroupName("SEAD")
        :setBriefing([[Le site sol-air que la force rouge a installé sur le volcan de Guguan, entre Sarigan et Alamagan : une batterie moyenne portée (SA-11) et un SA-15, qui couvrent l'approche des îles du nord.
Position : bullseye 007°/148 nm (N17°18.584' E145°50.535'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 158 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 123 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Marpi")
        :setFriendlyName("Z05 SEAD — Saipan, Marpi")
        :setRadioGroupName("SEAD")
        :setBriefing([[Le site sol-air de la pointe nord de Saipan, à Marpi : une batterie moyenne portée tirée au sort (SA-6 ou HQ-7) et un SA-8, sous la couverture des défenses permanentes de Saipan.
Position : bullseye 029°/28 nm (N15°15.979' E145°47.686'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 38 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 84 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_BeachRoad")
        :setFriendlyName("Z06 Convoi — Saipan, Beach Road")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi logistique descend Beach Road, la route côtière ouest de Saipan, de San Roque vers Garapan et Susupe. L'arrêter avant le front ; il porte sa propre artillerie antiaérienne (ZU-23).
Position : bullseye 028°/27 nm (N15°14.901' E145°46.402'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 38 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 85 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Broadway")
        :setFriendlyName("Z07 Convoi — Tinian, Broadway")
        :setRadioGroupName("Convois")
        :setBriefing([[Un convoi de carburant remonte Broadway, l'axe nord-sud de Tinian, du nord de l'aéroport vers North Field. Le détruire avant l'arrivée ; il porte sa propre artillerie antiaérienne.
Position : bullseye 023°/11 nm (N15°01.551' E145°37.946'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 32 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 94 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_CrossIsland")
        :setFriendlyName("Z08 Convoi — Saipan, Cross Island Road")
        :setRadioGroupName("Convois")
        :setBriefing([[Des renforts traversent Saipan d'ouest en est, de Tanapag vers Kagman par Capitol Hill et Cross Island Road. Les arrêter ; le convoi est escorté par un SA-13.
Position : bullseye 027°/26 nm (N15°14.304' E145°45.290'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 38 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 87 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Anatahan")
        :setFriendlyName("Z09 Frappe — Anatahan, missiles côtiers")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[La batterie de missiles antinavires côtiers (HY-2) installée sur Anatahan, qui interdit l'approche nord de l'archipel aux navires bleus. Détruire les lanceurs et leur radar ; défense SA-15 et Shilka.
Position : bullseye 006°/90 nm (N16°21.190' E145°42.412'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 102 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 96 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Garapan")
        :setFriendlyName("Z10 Frappe — Garapan, état-major")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[L'état-major de la force rouge à Garapan, la ville principale de Saipan : centre de commandement, antennes et abris. Tout détruire ; défense SA-15, dans la couverture des défenses permanentes de Saipan.
Position : bullseye 024°/23 nm (N15°12.425' E145°43.251'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 37 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 89 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Sarigan")
        :setFriendlyName("Z11 Frappe — Sarigan, station d'écoute")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[La station d'écoute et de relais radio de Sarigan, qui relaie les ordres vers les îles du nord. Détruire les antennes et le poste ; défense SA-8.
Position : bullseye 007°/111 nm (N16°42.277' E145°46.686'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 123 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 102 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Alamagan")
        :setFriendlyName("Z12 Frappe — Alamagan, dépôt avancé")
        :setRadioGroupName("Frappes en profondeur")
        :setBriefing([[Le dépôt avancé d'Alamagan, où la force rouge stocke le carburant et les munitions des îles du nord. Tout détruire ; défense HQ-7 et artillerie antiaérienne.
Position : bullseye 006°/165 nm (N17°35.997' E145°49.989'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 176 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 137 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_NorthField")
        :setFriendlyName("Z13 OCA — Tinian, North Field")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[North Field, l'ancienne base des B-29 au nord de Tinian, rouverte par la force rouge : chasseurs J-11A et bombardiers H-6J au parking. Les détruire au sol ; défense HQ-7 et Shilka.
Position : bullseye 020°/14 nm (N15°04.191' E145°38.332'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 33 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 94 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Pagan")
        :setFriendlyName("Z14 OCA — Pagan")
        :setRadioGroupName("Bases aériennes")
        :setBriefing([[La piste de Pagan, base arrière de la force rouge à l'extrême nord : J-11A et hélicoptères au parking. Les détruire au sol ; elle est sous la défense permanente de Pagan (SA-10, HQ-7).
Position : bullseye 004°/196 nm (N18°07.389' E145°45.789'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 207 nm ; Texaco 2 (perche, TACAN 52Y, 292.0) à 165 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Amphibie")
        :setFriendlyName("Z15 Antinavire — groupe amphibie de Tinian")
        :setRadioGroupName("Antinavire")
        :setBriefing([[Le groupe amphibie rouge mouillé au sud-ouest de Tinian, prêt à débarquer sur Rota : deux bâtiments de débarquement et une frégate Type 054A. Les couler ; la frégate porte une défense sol-air moyenne portée.
Position : bullseye 336°/6 nm (N14°56.464' E145°31.062'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 34 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 89 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.AddZone(
        VeafCombatZone:new()
        :setMissionEditorZoneName("combatZone_Escadre")
        :setFriendlyName("Z16 Antinavire — escadre de surface")
        :setRadioGroupName("Antinavire")
        :setBriefing([[L'escadre de surface rouge en patrouille à l'ouest d'Anatahan : un destroyer Type 052C, un Type 052B et une frégate Type 054A. Les couler ; le Type 052C porte une défense sol-air de longue portée, à attaquer hors de son enveloppe.
Position : bullseye 341°/103 nm (N16°28.096' E144°57.245'). Ravitailleurs : Arco 2 (panier, TACAN 53Y, 293.0) à 125 nm ; Texaco 1 (perche, TACAN 50Y, 290.0) à 138 nm.]])
        :setTraining(false)
        :initialize()
    )
    veafCombatZone.GetZone("combatZone_Talofofo_Medium"):addZoneElementsFromZoneNamed("combatZone_Talofofo_Easy")
    veafCombatZone.GetZone("combatZone_Talofofo_Hard"):addZoneElementsFromZoneNamed("combatZone_Talofofo_Medium")
    veafCombatZone.GetZone("combatZone_Talofofo_Hard"):addZoneElementsFromZoneNamed("combatZone_Talofofo_Easy")
    veafCombatZone.GetZone("combatZone_NWF_Medium"):addZoneElementsFromZoneNamed("combatZone_NWF_Easy")
    veafCombatZone.GetZone("combatZone_NWF_Hard"):addZoneElementsFromZoneNamed("combatZone_NWF_Medium")
    veafCombatZone.GetZone("combatZone_NWF_Hard"):addZoneElementsFromZoneNamed("combatZone_NWF_Easy")
    veafCombatZone.GetZone("combatZone_Rota_Medium"):addZoneElementsFromZoneNamed("combatZone_Rota_Easy")
    veafCombatZone.GetZone("combatZone_Rota_Hard"):addZoneElementsFromZoneNamed("combatZone_Rota_Medium")
    veafCombatZone.GetZone("combatZone_Rota_Hard"):addZoneElementsFromZoneNamed("combatZone_Rota_Easy")
    veafCombatZone.initialize()
end
end)

veafGuardedInit("QRA", function()
if veafQraManager then
    veafQraManager.initialize()
    local QRA_Saipan = VeafQRA:new()
        :setName("QRA Saipan")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Saipan")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-Saipan-MiG29", "QRA-Saipan-J11"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-Saipan-Su30", "QRA-Saipan-Su27"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Saipan Intl")
        :start()
    local QRA_Pagan = VeafQRA:new()
        :setName("QRA Pagan")
        :setCoalition(coalition.side.RED)
        :addEnnemyCoalition(coalition.side.BLUE)
        :setTriggerZone("QRA-Pagan")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-Pagan-MiG29", "QRA-Pagan-J11"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-Pagan-MiG31", "QRA-Pagan-Su30"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Pagan Airstrip")
        :start()
    local QRA_Guam = VeafQRA:new()
        :setName("QRA Guam")
        :setCoalition(coalition.side.BLUE)
        :addEnnemyCoalition(coalition.side.RED)
        :setTriggerZone("QRA-Guam")
        :setRandomGroupsToDeployByEnemyQuantity(1, {"QRA-Guam-F16", "QRA-Guam-F15"}, 1)
        :setRandomGroupsToDeployByEnemyQuantity(3, {"QRA-Guam-F15x4", "QRA-Guam-F14"}, 1)
        :setDelayBeforeRearming(600)
        :setDelayBeforeActivating(90)
        :setAirportLink("Andersen AFB")
        :start()
end
end)

-- ── Features ──

veafGuardedInit("GRASS", function()
if veafGrass then
    veafGrass.initialize()
end
end)

veafGuardedInit("ASSETS", function()
if veafAssets then
    veafAssets.Assets = {
        {sort = 1, name = "Magic 1", description = "Magic 1 (E-3A) — AWACS ouest", information = "U282.0 — FL300 — orbite à l'ouest de Guam et Rota", linked = "Magic 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 2, name = "Overlord 1", description = "Overlord 1 (E-3A) — AWACS est", information = "U283.0 — FL310 — orbite à l'est de Saipan", linked = "Overlord 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 3, name = "Texaco 1", description = "Texaco 1 (KC-135, perche) — ouest", information = "TACAN 50Y TX1 — U290.0 — FL220 — piste à l'ouest de Rota", linked = "Texaco 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 4, name = "Arco 1", description = "Arco 1 (KC-135 MPRS, panier) — ouest", information = "TACAN 51Y AR1 — U291.0 — FL180 — piste à l'ouest de Guam", linked = "Arco 1 - Escort", coalition = coalition.side.BLUE},
        {sort = 5, name = "Texaco 2", description = "Texaco 2 (KC-135, perche) — est", information = "TACAN 52Y TX2 — U292.0 — FL240 — piste à l'est de Farallon de Medinilla", linked = "Texaco 2 - Escort", coalition = coalition.side.BLUE},
        {sort = 6, name = "Arco 2", description = "Arco 2 (KC-135 MPRS, panier) — détroit", information = "TACAN 53Y AR2 — U293.0 — FL200 — piste au nord-est de Rota, près du Tarawa", linked = "Arco 2 - Escort", coalition = coalition.side.BLUE},
        {sort = 7, name = "CSG-74 Stennis", description = "CVN-74 Stennis", information = "TACAN 74X STN — ICLS 11 — Link 4 336.0 — ACLS — U305.0", coalition = coalition.side.BLUE},
        {sort = 8, name = "CSG-71 Roosevelt", description = "CVN-71 Roosevelt", information = "TACAN 71X RSV — ICLS 12 — Link 4 337.0 — ACLS — U306.0", coalition = coalition.side.BLUE},
        {sort = 9, name = "ARG-1 Tarawa", description = "LHA-1 Tarawa", information = "TACAN 73X TRW — ICLS 13 — U307.0", coalition = coalition.side.BLUE},
        {sort = 10, name = "CSG-74 Stennis S3B-Tanker", description = "Shell 5 — S-3B du Stennis (ravitailleur embarqué)", information = "TACAN 55Y S74 — U295.0", coalition = coalition.side.BLUE},
        {sort = 11, name = "CSG-71 Roosevelt S3B-Tanker", description = "Shell 6 — S-3B du Roosevelt (ravitailleur embarqué)", information = "TACAN 56Y S71 — U296.0", coalition = coalition.side.BLUE},
        {sort = 12, name = "Darkstar 1", description = "Darkstar 1 (E-3A) — AWACS bleu de l'arène", information = "U285.0 — FL300", coalition = coalition.side.BLUE},
        {sort = 13, name = "Wizard 1", description = "Wizard 1 (KJ-2000) — AWACS rouge", information = "U284.0 — FL300 — orbite entre Anatahan et Sarigan", linked = "Wizard 1 - Escort", coalition = coalition.side.RED},
        {sort = 14, name = "Shell 1", description = "Shell 1 (IL-78M) — ravitailleur rouge", information = "U294.0 — FL200 — orbite au nord-ouest de Saipan", linked = "Shell 1 - Escort", coalition = coalition.side.RED},
        {sort = 15, name = "Focus 1", description = "Focus 1 (A-50) — AWACS rouge de l'arène", information = "U286.0 — FL300", coalition = coalition.side.RED},
        {sort = 16, name = "Reaper 1", description = "Reaper 1 (drone laser) — North West Field", information = "Laser 1511 — FM 35.55. 3 000 m sol au-dessus du champ de tir attaque (zone A).", jtac = 1511, freq = "35.55", mod = "FM", coalition = coalition.side.BLUE},
        {sort = 17, name = "Reaper 2", description = "Reaper 2 (drone laser) — Talofofo", information = "Laser 1512 — FM 35.6. 3 000 m sol au-dessus du champ de tir hélicoptères (zone H).", jtac = 1512, freq = "35.6", mod = "FM", coalition = coalition.side.BLUE},
    }
    veafAssets.initialize()
end
end)

veafGuardedInit("MOVE", function()
if veafMove then
    veafMove.initialize()
end
end)

veafGuardedInit("SANCTUARY", function()
if veafSanctuary then
    veafSanctuary.initialize()
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Guam")
        if zone then
            zone:setName("Sanctuaire Guam")
                :setCoalition(coalition.side.BLUE)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Rota")
        if zone then
            zone:setName("Sanctuaire Rota")
                :setCoalition(coalition.side.BLUE)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Saipan")
        if zone then
            zone:setName("Sanctuaire Saipan")
                :setCoalition(coalition.side.RED)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
    do
        local zone = veafSanctuary.addZoneFromTriggerZone("SANCT-Tinian")
        if zone then
            zone:setName("Sanctuaire Tinian")
                :setCoalition(coalition.side.RED)
                :setDelayWarning(0)
                :setDelayInstant(60)
                :setProtectFromMissiles(true)
        end
    end
end
end)

veafGuardedInit("WEATHER", function()
if veafWeather then
    veafWeather.initialize()
end
end)

veafGuardedInit("REMOTE", function()
if veafRemote then
    veafRemote.initialize()
end
end)

veafGuardedInit("AIRBASES", function()
if veafAirbases then
    veafAirbases.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("MARKERS", function()
if veafMarkers then
    veafMarkers.initialize()
end
end)

veafGuardedInit("TIME", function()
if veafTime then
    veafTime.initialize()
end
end)

veafGuardedInit("UNITS", function()
if veafUnits then
    veafUnits.initialize()
end
end)

veafGuardedInit("CACHE", function()
if veafCacheManager then
    veafCacheManager.initialize()
end
end)

veafGuardedInit("EVENTS", function()
if veafEventHandler then
    veafEventHandler.initialize()
end
end)

-- ── Core ──

veafGuardedInit("GROUNDAI", function()
if veafGroundAI then
    veafGroundAI.initialize()
end
end)

-- ── Infrastructure ──

veafGuardedInit("COMMANDS", function()
if veafCommands then
    veafCommands.initialize()
end
end)

-- ── Features ──

veafGuardedInit("INTERPRETER", function()
if veafInterpreter then
    veafInterpreter.initialize()
end
end)

-- ── Community scripts disabled (VEAF leaves their globals alone) ──────────────
veaf.setConfig("tum", "enable", false)

-- ── Skynet-IADS ──────────────────────────────────────────────────────────────
veafGuardedInit("SKYNET", function()
if veafSkynet then
    veafSkynet.SpotterNetwork = true
    veafSkynet.SpotterView = "off"
    veafSkynet.initialize(false, false, false, false)
end
end)

-- ── CSAR configuration ───────────────────────────────────────────────────────
-- Note: CSAR.lua must be loaded by mission-script.lua before this block.
veafGuardedInit("CSAR", function()
if csar then
    csar.initialize()
end
end)
