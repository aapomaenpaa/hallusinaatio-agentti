import sqlite3

TIETOKANTA = "paavo.db"

def aja_sql(kysely):
    try:
        yhteys = sqlite3.connect(f"file:{TIETOKANTA}?mode=ro", uri=True)
        kursori = yhteys.execute(kysely)
        sarakkeet = [k[0] for k in kursori.description]
        rivit = kursori.fetchmany(50)
        yhteys.close()
        return str(sarakkeet) + "\n" + "\n".join(str(r) for r in rivit)
    except Exception as e:
        return f"SQL-virhe: {e}"

def kuvaa_sarakkeet():
    yhteys = sqlite3.connect(f"file:{TIETOKANTA}?mode=ro", uri=True)
    rivit = yhteys.execute("SELECT sarake, kuvaus FROM sarakekuvaukset").fetchall()
    yhteys.close()

    teksti = "Taulu: alueet (yksi rivi per postinumeroalue, vuosi 2024)\n"
    teksti += "postinumero: viisinumeroinen postinumero tekstinä\n"
    teksti += "alue: postinumeroalueen nimi\n"
    teksti += "kunta: kunta, jossa alue sijaitsee\n"
    for sarake, kuvaus in rivit:
        if kuvaus:
            teksti += f"{sarake}: {kuvaus}\n"
        else:
            teksti += f"{sarake}\n"