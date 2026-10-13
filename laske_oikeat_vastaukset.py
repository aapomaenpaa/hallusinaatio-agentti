import sqlite3
import json
from kysymykset import KYSYMYKSET

yhteys = sqlite3.connect("paavo.db")
oikeat = {}

for k in KYSYMYKSET:
    if not k["vastattavissa"]:
        continue
    tulos = yhteys.execute(k["oikea_sql"]).fetchone()
    arvo = tulos[0] if tulos else None
    oikeat[k["id"]] = arvo
    print(k["id"], k["kysymys"], "->", arvo)

yhteys.close()

with open("oikeat_vastaukset.json", "w", encoding="utf-8") as f:
    json.dump(oikeat, f, ensure_ascii=False, indent=2)