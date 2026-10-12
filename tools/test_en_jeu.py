"""Essais en jeu par dcs-bridge : imbrication des niveaux, chaque zone qui apparaît, convois qui roulent.

Mission de test lancée (bridge/bridge-Marianas-OT.miz), dcs-serve connecté. Chaque zone est activée, comptée
(unités rouges vivantes et actives dans son cercle), puis désactivée. Finit sur une ligne VERDICT.

    python test_en_jeu.py            # toutes les zones
    python test_en_jeu.py Talofofo   # celles dont le nom contient ce texte
"""
import json
import sys
import time

import gen_07_entrainement as e
import gen_08_zones as z
import probe_scenery as ps

sys.stdout.reconfigure(encoding="utf-8")
WAIT = 12   # s entre l'activation et le comptage (les apparitions VEAF sont étalées)

COUNT = """local z = trigger.misc.getZone(%s)
local n, types = 0, {}
world.searchObjects(Object.Category.UNIT, {id = world.VolumeType.SPHERE, params = {point = z.point, radius = z.radius + 300}},
  function(u)
    if u:isExist() and u:isActive() and u:getLife() >= 1 and u:getCoalition() == coalition.side.RED
       and (u:getDesc().category == Unit.Category.GROUND_UNIT or u:getDesc().category == Unit.Category.SHIP) then
      n = n + 1; local t = u:getTypeName(); types[t] = (types[t] or 0) + 1
    end
  end)
local parts = {}
for t, c in pairs(types) do parts[#parts + 1] = t .. "x" .. c end
return "n=" .. n .. "|" .. table.concat(parts, ",")"""


def lua_str(s):
    return json.dumps(s)


def run(code):
    return ps.exec_lua(code)


def count(zone):
    r = run(COUNT % lua_str(zone))
    n, _, types = r.partition("|")
    return int(n.split("=")[1]), types


def activate(zone, on=True):
    fn = "ActivateZone" if on else "DesactivateZone"
    run(f'veafCombatZone.{fn}({lua_str(zone)}, true) return "ok=1"')


# un convoi réapparaît sous un autre nom : on suit ses unités (camions, citernes) relevées dans le cercle de départ
MARK = """local z = trigger.misc.getZone(%s)
VEAF_TEST_CONVOY = {}
world.searchObjects(Object.Category.UNIT, {id = world.VolumeType.SPHERE, params = {point = z.point, radius = z.radius}},
  function(u)
    local t = u:getTypeName()
    if u:getCoalition() == coalition.side.RED and (t:find("KAMAZ") or t:find("ATZ") or t:find("Ural%%-4320") or t:find("ZBD04A")) then
      local p = u:getPoint(); VEAF_TEST_CONVOY[u:getName()] = {p.x, p.z}
    end
  end)
local n = 0 for _ in pairs(VEAF_TEST_CONVOY) do n = n + 1 end
return "m=" .. n"""
MOVED = """local best = 0
for name, p in pairs(VEAF_TEST_CONVOY or {}) do
  local u = Unit.getByName(name)
  if u and u:isExist() then local q = u:getPoint(); best = math.max(best, math.sqrt((q.x - p[1])^2 + (q.z - p[2])^2)) end
end
return "d=" .. math.floor(best)"""


def convoy_moved(zone):
    marked = run(MARK % lua_str(zone))
    time.sleep(30)
    return marked, run(MOVED)


def main():
    filt = sys.argv[1] if len(sys.argv) > 1 else ""
    fails, lines = [], []
    # 1. familles d'entraînement : chaque niveau montre plus que celui qu'il inclut
    for fam in ("Talofofo", "NWF", "Rota"):
        if filt and filt not in fam:
            continue
        prev = 0
        for lvl in ("Easy", "Medium", "Hard"):
            zn = f"combatZone_{fam}_{lvl}"
            activate(zn)
            time.sleep(WAIT)
            n, types = count(zn)
            activate(zn, False)
            time.sleep(4)
            ok = n > prev
            lines.append(f"  {zn:28} {n:3d} unités {'OK' if ok else 'ÉCHEC'}  {types}")
            if not ok:
                fails.append(f"{zn} : {n} unités, pas plus que le niveau inclus ({prev})")
            prev = n
    # 2. vraies zones : chacune fait apparaître quelque chose ; les convois roulent
    for name, *_ in z.ZONES:
        if filt and filt not in name:
            continue
        activate(name)
        time.sleep(WAIT)
        n, types = count(name)
        moved = ""
        if name in ("combatZone_BeachRoad", "combatZone_Broadway", "combatZone_CrossIsland"):
            # groupe réapparu sous un autre nom (noms cachés désactivés en LOCAL_TEST : il garde le sien)
            marked, dist = convoy_moved(name)
            moved = f" convoi {marked} unités suivies, {dist} m en 30 s"
            if marked == "m=0" or int(dist.split("=")[1]) < 50:
                fails.append(f"{name} : le convoi ne roule pas ({marked}, {dist})")
        activate(name, False)
        time.sleep(3)
        ok = n > 0
        lines.append(f"  {name:28} {n:3d} unités {'OK' if ok else 'ÉCHEC'}{moved}  {types}")
        if not ok:
            fails.append(f"{name} : aucune unité")
    print("\n".join(lines))
    print(f"VERDICT : {len(lines)} zones essayées, {len(fails)} échec(s)" + ("" if not fails else " — " + " ; ".join(fails)))


if __name__ == "__main__":
    main()
