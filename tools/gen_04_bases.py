"""Lot 04 : camp des aérodromes et slots dynamiques.

Bleu avec slots : Andersen (base mère), Won Pat, Olf Orote. North West Field est bleu sans slots : c'est
le champ de tir attaque. Rouge avec slots : Saipan (base principale), Tinian (base avancée). Pagan est
rouge sans slots (piste courte, cible OCA lointaine). Rota reste neutre : île évacuée, champ de tir SEAD.
"""
from lib import Batch

b = Batch()
for name, side, dyn in [
    ("Andersen AFB", "blue", True),
    ("Antonio B. Won Pat Intl", "blue", True),
    ("Olf Orote", "blue", True),
    ("North West Field", "blue", False),
    ("Saipan Intl", "red", True),
    ("Tinian Intl", "red", True),
    ("Pagan Airstrip", "red", False),
]:
    b.act("set_airbase_coalition", name=name, coalition=side, dynamic_spawn=dyn)
b.save("04-bases.json")
