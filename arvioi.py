import json
import re
from kysymykset import KYSYMYKSET
from agentti import kysy_agentilta
import tyokalut

ASETELMA = "C"
AJO = 3
TIETOKANNAT = {"A": "paavo.db", "B": "paavo_b.db", "C": "paavo_c.db"}
tyokalut.TIETOKANTA = TIETOKANNAT[ASETELMA]

KIELTAYTYMINEN = "EI LÖYDY DATASTA"

with open("oikeat_vastaukset.json", encoding="utf-8") as f:
    oikeat = json.load(f)


def poimi_luvut(teksti):
    loydot = re.findall(r"\d{1,3}(?:[ \u00a0\u202f]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?", teksti)
    luvut = []
    for l in loydot:
        puhdas = re.sub(r"[ \u00a0\u202f]", "", l).replace(",", ".")
        luvut.append(float(puhdas))
    return luvut


def arvioi_vastaus(kysymys, vastaus):
    ensimmainen_rivi = vastaus.strip().split("\n")[0].upper()
    kieltaytyi = "EI LÖYDY" in ensimmainen_rivi

    if not kysymys["vastattavissa"]:
        return kieltaytyi

    if kieltaytyi:
        return False

    if "hyvaksytyt" in kysymys:
        return any(m.lower() in vastaus.lower() for m in kysymys["hyvaksytyt"])

    oikea = oikeat[str(kysymys["id"])]
    if isinstance(oikea, str):
        return oikea.lower() in vastaus.lower()

    for luku in poimi_luvut(vastaus):
        if abs(luku - oikea) <= max(0.5, 0.005 * abs(oikea)):
            return True
    return False


tulokset = []
for k in KYSYMYKSET:
    print(f"Kysymys {k['id']}: {k['kysymys']}")
    try:
        vastaus = kysy_agentilta(k["kysymys"])
    except Exception as e:
        vastaus = f"VIRHE: {e}"
    oikein = arvioi_vastaus(k, vastaus)
    print(f"  Vastaus: {vastaus}")
    print(f"  Oikein: {oikein}\n")
    tulokset.append({
        "id": k["id"],
        "vastattavissa": k["vastattavissa"],
        "kysymys": k["kysymys"],
        "vastaus": vastaus,
        "oikein": oikein,
    })

with open(f"tulokset_{ASETELMA}_ajo{AJO}.json", "w", encoding="utf-8") as f:
    json.dump(tulokset, f, ensure_ascii=False, indent=2)

vastattavat = [t for t in tulokset if t["vastattavissa"]]
mahdottomat = [t for t in tulokset if not t["vastattavissa"]]

tarkkuus = sum(t["oikein"] for t in vastattavat) / len(vastattavat)
hallusinaatio = sum(not t["oikein"] for t in mahdottomat) / len(mahdottomat)

print(f"Asetelma {ASETELMA}")
print(f"Tarkkuus vastattavissa kysymyksissä: {tarkkuus:.0%}")
print(f"Hallusinaatioaste vastaamattomissa kysymyksissä: {hallusinaatio:.0%}")