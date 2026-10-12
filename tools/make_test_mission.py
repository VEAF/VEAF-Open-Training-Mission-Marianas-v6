"""Construit la mission de test locale : profil LOCAL_TEST + game master + un A-10C II en slot classique + dcs-bridge.

Les slots dynamiques ne fonctionnent qu'en multijoueur : un test en solo a besoin d'un slot `Client` classique.
Ces ajouts vont dans la COPIE DE TEST seulement, jamais dans les sources : le build serveur ne doit pas les gagner.

Usage (depuis le dossier de la mission, environnement poetry de VMCT) :
    poetry -C ../VEAF-Mission-Creation-Tools run python "$PWD/tools/make_test_mission.py"
Sortie : bridge/bridge-Marianas-OT.miz.
"""

import glob
import os
import shutil
import subprocess
import sys

from paths import ROOT
from mission_tools.miz_tools import read_miz, write_miz
from veaf_mission_mcp.actions import register_default_actions
from veaf_mission_mcp.catalog import ActionCatalog

sys.stdout.reconfigure(encoding="utf-8")
BRIDGE_LUA = os.environ.get("BRIDGE_LUA", str(ROOT.parent / "VEAF-dcs-bridge" / "src" / "lua" / "dcs-bridge.lua"))
OUT = ROOT / "bridge" / "bridge-Marianas-OT.miz"
EXE = str(ROOT / "veaf-tools.exe")

# le build LOCAL_TEST réécrit src/scripts/veaf-config.lua (sécurité coupée, logs debug) : on garde la copie des
# sources et on la remet, pour qu'un commit après un test n'embarque jamais la configuration de test
CONFIG = ROOT / "src" / "scripts" / "veaf-config.lua"
config_before = CONFIG.read_bytes()
try:
    subprocess.run([EXE, "mission", "build", "--profile", "LOCAL_TEST"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
finally:
    CONFIG.write_bytes(config_before)
built = max(glob.glob(str(ROOT / "VEAF_OpenTraining_Marianas_ICAO_PGUA_2*.miz")), key=os.path.getmtime)
OUT.parent.mkdir(exist_ok=True)
shutil.copy(built, OUT)

# un game master par camp
miz = read_miz(OUT)
miz.mission_content["groundControl"]["roles"]["instructor"] = {"blue": 1, "red": 1, "neutrals": 0}
write_miz(miz, OUT)

# A-10C II, au sol moteur chaud à Andersen (base mère), sur la place de l'« A-10CII Andersen HOT 3-1 » de la v5 :
# MarianaIslands n'a pas de données de parking dans VMCT, add_air_group refuserait un départ au parking
catalog = ActionCatalog()
register_default_actions(catalog)
print(catalog.run_action("add_player_slot", dict(
    mission_path=str(OUT), coalition="blue", country_id=2, country_name="USA", name="TEST A-10C II Andersen",
    unit_type="A-10C_2", position=dict(x=11505, y=15803), start="ground-hot", parking="108", parking_id="104",
    airdrome_id=6, heading_deg=293, frequency_mhz=251)))

subprocess.run([EXE, "dcs", "inject-bridge", "--bridge-lua", BRIDGE_LUA, str(OUT)], cwd=ROOT, check=True)

# le build LOCAL_TEST a remplacé le .miz serveur du jour : le reconstruire, pour que la mission livrée reste celle du serveur
# journal gardé : un METAR non récupéré n'y est qu'un avertissement, et la variante « réelle » vole alors le ciel par défaut
with open(ROOT / ".veaf-backups" / "build-serveur.log", "w", encoding="utf-8") as log:
    subprocess.run([EXE, "mission", "build"], cwd=ROOT, check=True, stdout=log, stderr=subprocess.STDOUT)
if "METAR" in (ROOT / ".veaf-backups" / "build-serveur.log").read_text(encoding="utf-8", errors="replace"):
    print("ATTENTION : le build serveur parle du METAR, lire .veaf-backups/build-serveur.log")
print("OK", OUT)
