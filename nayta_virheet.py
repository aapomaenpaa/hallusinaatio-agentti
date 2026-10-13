import json

with open("tulokset_C_ajo1.json", encoding="utf-8") as f:
    tulokset = json.load(f)

for t in tulokset:
    if not t["oikein"]:
        print(f"Kysymys {t['id']}: {t['kysymys']}")
        print(f"  Vastaus: {t['vastaus']}\n")