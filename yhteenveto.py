import json
import glob

def kieltaytyi(t):
    return "EI LÖYDY" in t["vastaus"].strip().split("\n")[0].upper()


def mittarit(tiedosto):
    with open(tiedosto, encoding="utf-8") as f:
        tulokset = json.load(f)

    vastattavat = [t for t in tulokset if t["vastattavissa"]]
    mahdottomat = [t for t in tulokset if not t["vastattavissa"]]

    oikein = sum(t["oikein"] for t in vastattavat)
    turha_kielto = sum(kieltaytyi(t) for t in vastattavat)
    varma_vaara = sum(not t["oikein"] and not kieltaytyi(t) for t in vastattavat)
    hallusinaatio = sum(not t["oikein"] for t in mahdottomat)

    n = len(vastattavat)
    m = len(mahdottomat)
    return oikein / n, turha_kielto / n, varma_vaara / n, hallusinaatio / m


print(f"{'Asetelma':<10}{'Ajoja':>6}{'Oikein':>20}{'Kieltäytyi':>20}{'Varma väärä':>20}{'Hallusinaatio':>20}")

for asetelma in ["A", "B", "C"]:
    tiedostot = sorted(glob.glob(f"tulokset_{asetelma}_ajo*.json"))
    kaikki = [mittarit(t) for t in tiedostot]

    rivi = f"{asetelma:<10}{len(tiedostot):>6}"
    for i in range(4):
        arvot = [m[i] for m in kaikki]
        keskiarvo = sum(arvot) / len(arvot)
        teksti = f"{keskiarvo:.0%} ({min(arvot):.0%}–{max(arvot):.0%})"
        rivi += f"{teksti:>20}"
    print(rivi)