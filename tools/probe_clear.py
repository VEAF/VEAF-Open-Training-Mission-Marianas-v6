"""Trouve, dans DCS, la place libre la plus proche de chaque groupe au sol que probe_scenery.py juge bloqué ou à l'eau.

La recherche se fait en anneaux autour de la position de l'éditeur (25 m de pas, 24 directions, jusqu'à MAX_R), et
chaque candidat est jugé par la seule requête fiable de Disposition (limitation disposition-getsimplezones-is-a-lottery) :
au moins une place de 5 m libre à 20 m, sur un sol de terre (1) ou de route (4), sans unité vivante à 25 m.
Un convoi cherche une route (sol 4) : son départ doit être sur la route qu'il va suivre.

Usage (mission de test lancée, dcs-serve connecté, AUCUNE zone activée) :
    python probe_clear.py               -> tools/clear_moves.json : {groupe: [x, y, distance]} ; affiche les échecs
Le déplacement lui-même est fait par apply_clear_moves.py, qui vérifie que chaque groupe reste dans sa zone.
"""
import json
import sys

from paths import ROOT, TOOLS  # noqa: F401
import probe_scenery as ps
from veaf_mission_mcp.mission_folder import load_folder_mission

sys.stdout.reconfigure(encoding="utf-8")
MAX_R = 1500
LUA = """local pts = %s
local out = {}
local function occupied(p)
  local found = false
  world.searchObjects(Object.Category.UNIT, {id = world.VolumeType.SPHERE, params = {point = p, radius = 25}},
    function() found = true; return false end)
  return found
end
local function good(x, z, road)
  local s = land.getSurfaceType({x = x, y = z})
  if road then if s ~= 4 then return false end
  elseif s ~= 1 and s ~= 4 then return false end
  local p = {x = x, y = land.getHeight({x = x, y = z}), z = z}
  if occupied(p) then return false end
  local ok, c = pcall(Disposition.getSimpleZones, p, 20, 5, 10)
  return ok and type(c) == "table" and #c > 0
end
for _, q in ipairs(pts) do
  local found = nil
  if good(q.x, q.z, q.road) then found = {q.x, q.z, 0} end
  local r = 25
  while not found and r <= %d do
    for k = 0, 23 do
      local a = 2 * math.pi * k / 24
      local x, z = q.x + r * math.cos(a), q.z + r * math.sin(a)
      if good(x, z, q.road) then found = {math.floor(x), math.floor(z), r}; break end
    end
    r = r + 25
  end
  out[#out + 1] = q.n .. "=" .. (found and (found[1] .. "," .. found[2] .. "," .. found[3]) or "none")
end
return table.concat(out, ";")"""


def seq(v):
    return list(v.values()) if isinstance(v, dict) else list(v or [])


def main():
    vehicles, _ = ps.collect()
    verdict = {}
    for code in ps.chunks(vehicles):
        verdict.update(kv.split("=") for kv in ps.exec_lua(code).split(";"))
    bad = sorted({g for n, g, _x, _z in vehicles if verdict.get(str(n)) in ("blocked", "water", "shallow")})
    m = load_folder_mission(ROOT).mission_content
    anchor = {}
    for co in m["coalition"].values():
        for c in seq(co.get("country")):
            for g in seq((c.get("vehicle") or {}).get("group")):
                if g["name"] in bad:
                    u = seq(g["units"])[0]
                    anchor[g["name"]] = (round(u["x"]), round(u["y"]), "-Convoi" in g["name"])
    moves, fails = {}, []
    names = sorted(anchor)
    for i in range(0, len(names), 6):
        part = names[i:i + 6]
        tbl = "{" + ",".join("{n=%s,x=%d,z=%d,road=%s}" % (json.dumps(n), *anchor[n][:2], "true" if anchor[n][2] else "false")
                             for n in part) + "}"
        for kv in ps.exec_lua(LUA % (tbl, MAX_R)).split(";"):
            n, v = kv.rsplit("=", 1)
            if v == "none":
                fails.append(n)
            else:
                x, z, r = map(int, v.split(","))
                moves[n] = [x, z, r]
    json.dump(moves, open(TOOLS / "clear_moves.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for n in fails:
        print(f"  aucune place libre à {MAX_R} m : {n}")
    print(f"VERDICT : {len(bad)} groupes à déplacer, {len(moves)} places trouvées (distance médiane "
          f"{sorted(v[2] for v in moves.values())[len(moves) // 2] if moves else 0} m), {len(fails)} sans place")


if __name__ == "__main__":
    main()
