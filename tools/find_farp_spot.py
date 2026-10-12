"""Cherche dans DCS une place de FARP dégagée ET plate près d'un point : centre et 8 points à 40 m avec chacun une place
de 5 m libre à 20 m (petite requête Disposition), sol de terre, et moins de MAX_DROP m de dénivelé entre ces 9 points.

    python find_farp_spot.py X Y [RAYON]     -> les meilleures places, de la plus proche à la plus lointaine
"""
import sys

import probe_scenery as ps

sys.stdout.reconfigure(encoding="utf-8")
MAX_DROP = 3.0
LUA = """local cx, cz, R, step, maxdrop = %d, %d, %d, 50, %f
local out = {}
local function free(x, z)
  if land.getSurfaceType({x = x, y = z}) ~= 1 then return false end
  local p = {x = x, y = land.getHeight({x = x, y = z}), z = z}
  local ok, c = pcall(Disposition.getSimpleZones, p, 20, 5, 10)
  return ok and type(c) == "table" and #c > 0
end
for dx = -R, R, step do for dz = %d, %d, step do
  local x, z = cx + dx, cz + dz
  if dx * dx + dz * dz <= R * R then
    local hmin, hmax, okk = 1e9, -1e9, free(x, z)
    if okk then
      for k = 0, 7 do
        local a = math.pi * k / 4
        local px, pz = x + 40 * math.cos(a), z + 40 * math.sin(a)
        local h = land.getHeight({x = px, y = pz})
        hmin, hmax = math.min(hmin, h), math.max(hmax, h)
        if not free(px, pz) then okk = false; break end
      end
    end
    if okk and hmax - hmin <= maxdrop then
      out[#out + 1] = math.floor(x) .. "," .. math.floor(z) .. "," .. string.format("%%.1f", hmax - hmin)
    end
  end
end end
return "s=" .. table.concat(out, ";")"""


def main():
    x, y = int(sys.argv[1]), int(sys.argv[2])
    r = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    found = []
    for dz0 in range(-r, r + 1, 300):   # par bandes, pour rester sous le délai d'un appel
        res = ps.exec_lua(LUA % (x, y, r, MAX_DROP, dz0, min(dz0 + 250, r)))[2:]
        for s in filter(None, res.split(";")):
            px, pz, drop = s.split(",")
            found.append((int(px), int(pz), float(drop)))
    found.sort(key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
    for px, pz, drop in found[:10]:
        print(f"  ({px}, {pz})  à {((px - x) ** 2 + (pz - y) ** 2) ** .5:.0f} m, dénivelé {drop} m")
    print(f"VERDICT : {len(found)} places dégagées et plates dans {r} m")


if __name__ == "__main__":
    main()
