import pandas as pd
import re
import sqlite3

df = pd.read_csv("paavo_2024.csv", sep=";")

df = df[df["Postal code area"] != "WHOLE COUNTRY"]

osat = df["Postal code area"].str.extract(r"^(\d{5})\s+(.*)\s+\((.*)\)$")
df["postinumero"] = osat[0]
df["alue"] = osat[1]
df["kunta"] = osat[2]

df = df.drop(columns=["Postal code area"])

kuvaukset = {}
uudet_nimet = {}

for sarake in df.columns:
    if sarake in ["postinumero", "alue", "kunta"]:
        continue
    puhdas = sarake.replace("2024 ", "")
    lyhyt = re.sub(r"[^a-z0-9]+", "_", puhdas.lower()).strip("_")
    uudet_nimet[sarake] = lyhyt
    kuvaukset[lyhyt] = puhdas

df = df.rename(columns=uudet_nimet)

data_sarakkeet = [s for s in df.columns if s not in ["postinumero", "alue", "kunta"]]

for s in data_sarakkeet:
    df[s] = pd.to_numeric(df[s], errors="coerce")


yhteys = sqlite3.connect("paavo.db")

df.to_sql("alueet", yhteys, if_exists="replace", index=False)

kuvaus_df = pd.DataFrame(list(kuvaukset.items()), columns=["sarake", "kuvaus"])
kuvaus_df.to_sql("sarakekuvaukset", yhteys, if_exists="replace", index=False)

print(pd.read_sql("SELECT COUNT(*) AS rivit FROM alueet", yhteys))
print(pd.read_sql("SELECT * FROM sarakekuvaukset LIMIT 5", yhteys))

yhteys.close()