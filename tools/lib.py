"""Outils communs aux générateurs de lots (tools/gen_*.py).

Un générateur écrit un fichier de lot dans tools/batches/ ; `python tools/mcp.py batch <lot>` l'exécute
sur le catalogue d'actions de veaf-mission-mcp (code VMCT de develop). Un lot ne s'exécute qu'une fois.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from coastlines import coast_distance, island_of  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
M = ROOT.as_posix()

BLUE = dict(coalition="blue", country_id=2, country_name="USA")
RED = dict(coalition="red", country_id=0, country_name="Russia")       # CTLD veut la Russie dans le camp rouge
RED_CN = dict(coalition="red", country_id=27, country_name="China")   # matériel chinois de la force rouge

# Aérodromes (list_airfields, MarianaIslands)
AIRFIELDS = {
    "Andersen AFB": (10575, 14549),
    "Antonio B. Won Pat Intl": (-24, -78),
    "North West Field": (15471, 6727),
    "Olf Orote": (-5023, -16869),
    "Rota Intl": (75885, 48590),
    "Tinian Intl": (166860, 89957),
    "Saipan Intl": (180035, 101856),
    "Pagan Airstrip": (512410, 107565),
}

PLACES = {k: (v["x"], v["y"]) for k, v in json.loads((ROOT / "tools/places.json").read_text(encoding="utf-8")).items()}

# Bullseye commun : île d'Aguijan, au milieu du détroit qui fait le front (geocode « Aguijan »)
BULLSEYE = (150790, 83347)


def nm(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1852


def km(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1]) / 1000


def off(p, brg, m):
    """Point à `m` mètres de `p`, au relèvement `brg` (degrés vrais, x = nord, y = est)."""
    r = math.radians(brg)
    return (p[0] + m * math.cos(r), p[1] + m * math.sin(r))


def bearing(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360


def bullseye(p):
    """« 123°/45 nm » depuis le bullseye : cap = atan2(Δy, Δx)."""
    return f"{bearing(BULLSEYE, p):03.0f}°/{nm(BULLSEYE, p):.0f} nm"


def xy(p):
    return {"x": round(p[0]), "y": round(p[1])}


def land(p, what, margin=60):
    """Refuse un point en mer ou trop près du rivage (contours OSM, pas le terrain DCS)."""
    isl = island_of(*p)
    if isl is None:
        raise SystemExit(f"EN MER : {what} {p}")
    d = coast_distance(*p)
    if d < margin:
        raise SystemExit(f"TROP PRÈS DU RIVAGE ({d:.0f} m) : {what} {p}")
    return p


def sea(p, what, margin=1000):
    """Refuse un point à terre ou trop près d'une côte (navires)."""
    if island_of(*p) is not None:
        raise SystemExit(f"À TERRE : {what} {p}")
    d = coast_distance(*p)
    if d < margin:
        raise SystemExit(f"TROP PRÈS DE LA CÔTE ({d:.0f} m) : {what} {p}")
    return p


class Batch:
    def __init__(self):
        self.items = []

    def act(self, action, **params):
        self.items.append({"name": action, "params": {"mission_path": M, **params}})

    def save(self, name):
        path = ROOT / "tools/batches" / name
        path.write_text(json.dumps(self.items, indent=1, ensure_ascii=False), encoding="utf-8")
        print(len(self.items), "actions ->", path.relative_to(ROOT))


def cmd_unit(alias_cmd, carrier_type, tag, extra=""):
    """Faux porteur de zone : `#command="<alias ...>"` + balises de tirage + suffixe unique."""
    name = f'#command="{alias_cmd}"'
    if extra:
        name += " " + extra
    return {"type": carrier_type, "name": f"{name} #{tag}"}


def interp_unit(alias_cmd, carrier_type, tag):
    """Porteur permanent : `#veafInterpreter["<alias ...>"]` + suffixe unique."""
    return {"type": carrier_type, "name": f'#veafInterpreter["{alias_cmd}"] #{tag}'}


# Ravitailleurs bleus : extrémités de l'hippodrome, FL, TACAN, MHz, type de ravitaillement (gen_05_soutien.py)
TANKERS = {
    "Texaco 1": (((30000, -70000), (90000, -70000)), 220, "50Y", 290.0, "perche"),
    "Arco 1": (((-30000, -50000), (20000, -50000)), 180, "51Y", 291.0, "panier"),
    "Texaco 2": (((190000, 265000), (250000, 265000)), 240, "52Y", 292.0, "perche"),
    "Arco 2": (((70000, 135000), (130000, 135000)), 200, "53Y", 293.0, "panier"),
}


def seg_nm(p, a, b):
    """Distance (nm) du point p au segment ab : la même mesure que gather.py, pour que F10 et README disent pareil."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy) / 1852


def tankers_text(p):
    """« Ravitailleurs : Arco 1 (panier, TACAN 51Y, 291.0) à 12 nm ; Texaco 1 (...) à 30 nm. » — le plus proche de chaque type,
    mesuré jusqu'à sa piste."""
    out = []
    for kind in ("panier", "perche"):
        n, (ab, fl, tacan, f, k) = min(((n, v) for n, v in TANKERS.items() if v[4] == kind),
                                       key=lambda kv: seg_nm(p, *kv[1][0]))
        out.append(f"{n} ({kind}, TACAN {tacan}, {f:.1f}) à {seg_nm(p, *ab):.0f} nm")
    return "Ravitailleurs : " + " ; ".join(out) + "."


def ddm(p):
    """« N13°19.051' E144°45.729' » (degrés, minutes décimales : ce que saisissent la plupart des avions)."""
    from veaf_libs.coordinates import xy_to_latlon  # noqa: E402
    lat, lon = xy_to_latlon("MarianaIslands", *p)

    def one(v, pos, neg, w):
        h = pos if v >= 0 else neg
        v = abs(v)
        d = int(v)
        return f"{h}{d:0{w}d}°{(v - d) * 60:06.3f}'"
    return f"{one(lat, 'N', 'S', 2)} {one(lon, 'E', 'W', 3)}"


def position_text(p):
    return f"Position : bullseye {bullseye(p)} ({ddm(p)})."


def spot(center, brg, dist, what, margin=80):
    """Point à `dist` m de `center` au relèvement `brg`, ramené sur la terre ferme la plus proche."""
    from coastlines import nearest_land  # noqa: E402
    p = off(center, brg, dist)
    q = nearest_land(p[0], p[1], margin=margin)
    if q is None:
        raise SystemExit(f"pas de terre près de {what} {p}")
    return q
