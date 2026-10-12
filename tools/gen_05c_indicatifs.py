"""Lot 05c : indicatifs des ravitailleurs (nom de groupe = indicatif).

add_carrier_group a donné Texaco11 et Arco11 aux S-3B des porte-avions, posés avant les ravitailleurs ;
add_air_group a alors décalé chaque ravitailleur sur la famille suivante (Texaco 1 → Shell11...).
Les S-3B passent en Shell 5 / Shell 6 (famille bleue libre), puis chaque ravitailleur reprend son nom.
"""
import json
import sys

from lib import M, Batch
from mcp import cat  # noqa: F401  (catalogue in-process)


res = cat.run_action("describe_units", {"mission_path": M, "category": "plane", "include_route": False})
unit = {g["name"]: g["units"][0]["name"] for g in res["groups"]}
WANT = [
    ("CSG-74 Stennis S3B-Tanker", "Shell", 5),
    ("CSG-71 Roosevelt S3B-Tanker", "Shell", 6),
    ("Texaco 1", "Texaco", 1), ("Arco 1", "Arco", 1),
    ("Texaco 2", "Texaco", 2), ("Arco 2", "Arco", 2),
]
FAMILY = {"Texaco": 1, "Arco": 2, "Shell": 3}
b = Batch()
for g, word, flight in WANT:
    b.act("set_unit_properties", group_name=g, unit_name=unit[g],
          callsign={"family": FAMILY[word], "flight": flight, "number": 1, "name": word})
b.save("05c-indicatifs.json")
