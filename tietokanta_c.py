import sqlite3
import random
import pandas as pd

yhteys = sqlite3.connect("paavo.db")
df = pd.read_sql("SELECT * FROM alueet", yhteys)
yhteys.close()

avaimet = ["postinumero", "alue", "kunta"]
data_sarakkeet = [s for s in df.columns if s not in avaimet]

random.seed(42)
sekoitetut = data_sarakkeet.copy()
random.shuffle(sekoitetut)

KOODIT = {s: f"s{i + 1:02d}" for i, s in enumerate(sekoitetut)}

df = df.rename(columns=KOODIT)
df = df[avaimet + sorted(KOODIT.values())]

yhteys_c = sqlite3.connect("paavo_c.db")
df.to_sql("alueet", yhteys_c, if_exists="replace", index=False)

kuvaukset_c = pd.DataFrame({"sarake": sorted(KOODIT.values()), "kuvaus": ""})
kuvaukset_c.to_sql("sarakekuvaukset", yhteys_c, if_exists="replace", index=False)

pd.Series(KOODIT, name="koodi").to_csv("koodiavain_c.csv", index_label="alkuperainen")

print(pd.read_sql("SELECT * FROM alueet LIMIT 2", yhteys_c))
yhteys_c.close()