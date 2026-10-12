"""Géocode une fois les lieux réels dont la mission a besoin → tools/places.json (x/y DCS).

Relancer ajoute seulement les lieux absents. Chaque point est à relire : l'outil peut tomber sur un
homonyme.
"""
import json
import sys

from paths import ROOT  # noqa: F401  (met aussi le code VMCT sur sys.path)
from veaf_mission_mcp.actions import register_default_actions
from veaf_mission_mcp.catalog import ActionCatalog

sys.stdout.reconfigure(encoding="utf-8")
PLACES = [
    "Merizo, Guam", "Umatac, Guam", "Inarajan, Guam", "Mount Lamlam", "Ritidian Point", "Mount Santa Rosa, Guam",
    "Hagåtña, Guam", "Dededo, Guam", "Barrigada, Guam", "Talofofo, Guam", "Apra Harbor",
    "Sinapalo, Rota", "Songsong, Rota", "Sabana, Rota", "Sasanhaya Bay",
    "San Jose, Tinian", "North Field, Tinian", "Tinian Harbor", "Unai Chulu", "Unai Dankulo",
    "Garapan", "Susupe", "Chalan Kanoa", "Mount Tapochau", "Banzai Cliff", "Tanapag", "Obyan Beach",
    "Agingan Point", "Kagman", "Marpi Point", "San Roque, Saipan", "Koblerville",
    "Aguijan", "Farallon de Medinilla", "Anatahan", "Sarigan", "Alamagan", "Pagan", "Guguan", "Agrihan",
]
out_path = ROOT / "tools" / "places.json"
places = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
cat = ActionCatalog()
register_default_actions(cat)
for q in PLACES:
    if q in places:
        continue
    r = cat.run_action("geocode", {"mission_path": str(ROOT), "query": q})
    if not r.get("found"):
        print("INTROUVABLE", q)
        continue
    places[q] = {"x": round(r["xy"]["x"]), "y": round(r["xy"]["y"]), "osm": r.get("osm_type"), "name": r["display_name"][:90]}
    print(f"{q:28} {places[q]['x']:>8} {places[q]['y']:>8}  {places[q]['osm']:<12} {places[q]['name']}")
out_path.write_text(json.dumps(places, indent=1, ensure_ascii=False), encoding="utf-8")
