"""Contours des îles (OpenStreetMap, Nominatim) en x/y DCS → tools/coastlines.json, et test terre/mer.

La carte MarianaIslands n'a pas de grille d'altitude dans VMCT (`terrain_elevation` : available false),
donc aucun outil ne dit si un point est à terre. Ce module le fait d'après les contours OSM :
`on_land(x, y)` et `coast_distance(x, y)`. OSM n'est pas le terrain de DCS : à revérifier en jeu.

python tools/coastlines.py         # télécharge les contours manquants (1 requête/s, User-Agent identifié)
"""
import json
import math
import sys
import time
import urllib.parse
import urllib.request

from paths import ROOT

ISLANDS = ["Guam", "Rota", "Aguijan", "Tinian", "Saipan", "Farallon de Medinilla", "Anatahan", "Sarigan",
           "Guguan", "Alamagan", "Pagan", "Agrihan", "Cocos Island, Guam", "Cabras Island, Guam"]
PATH = ROOT / "tools" / "coastlines.json"
UA = "VEAF-Open-Training-Marianas-v6 mission builder (https://github.com/VEAF)"


def _fetch():
    from veaf_libs.coordinates import latlon_to_xy
    data = json.loads(PATH.read_text(encoding="utf-8")) if PATH.exists() else {}
    for name in ISLANDS:
        if name in data:
            continue
        q = urllib.parse.urlencode({"q": name + ("" if "Guam" in name else " island, Northern Mariana Islands"),
                                    "format": "jsonv2", "polygon_geojson": 1, "limit": 10})
        req = urllib.request.Request("https://nominatim.openstreetmap.org/search?" + q, headers={"User-Agent": UA})
        res = json.load(urllib.request.urlopen(req, timeout=30))
        time.sleep(1.1)
        # l'île elle-même (place=island/islet), pas la commune ni le territoire qui portent le même nom
        geo = next((r["geojson"] for r in res if r.get("category") == "place" and r.get("type") in ("island", "islet")
                    and r["geojson"]["type"] in ("Polygon", "MultiPolygon")), None)
        if not geo:
            print("pas de polygone pour", name, [r.get("type") for r in res])
            continue
        polys = [geo["coordinates"]] if geo["type"] == "Polygon" else geo["coordinates"]
        rings = []
        for poly in polys:
            ring = poly[0]
            rings.append([[round(c) for c in latlon_to_xy("MarianaIslands", lat, lon)] for lon, lat in ring])
        data[name] = rings
        print(name, len(rings), "anneau(x),", sum(len(r) for r in rings), "points")
    PATH.write_text(json.dumps(data), encoding="utf-8")


_RINGS = None


def _rings():
    global _RINGS
    if _RINGS is None:
        _RINGS = [(n, r) for n, rs in json.loads(PATH.read_text(encoding="utf-8")).items() for r in rs]
    return _RINGS


def _inside(x, y, ring):
    c = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def island_of(x, y):
    """Nom de l'île qui contient le point, ou None (mer)."""
    for n, r in _rings():
        if _inside(x, y, r):
            return n
    return None


def on_land(x, y):
    return island_of(x, y) is not None


def coast_distance(x, y):
    """Distance (m) au trait de côte le plus proche."""
    best = math.inf
    for _, r in _rings():
        for (ax, ay), (bx, by) in zip(r, r[1:]):
            dx, dy = bx - ax, by - ay
            t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy or 1)))
            best = min(best, math.hypot(x - ax - t * dx, y - ay - t * dy))
    return best


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    _fetch()


def nearest_land(x, y, margin=150, step=100, max_r=5000):
    """Le point à terre le plus proche de (x, y), à `margin` m au moins du rivage (anneaux croissants)."""
    if on_land(x, y) and coast_distance(x, y) >= margin:
        return (x, y)
    r = step
    while r <= max_r:
        n = max(8, int(2 * math.pi * r / step))
        for i in range(n):
            a = 2 * math.pi * i / n
            p = (x + r * math.cos(a), y + r * math.sin(a))
            if on_land(*p) and coast_distance(*p) >= margin:
                return (round(p[0]), round(p[1]))
        r += step
    return None
