# Hallusinaatio-agentti

**Ilman datan kuvauksia tekoälyagentin oikeiden vastausten osuus putosi 98 %:sta 22 %:iin. Yhtä usein se antoi varman mutta väärän vastauksen.**

> **English summary.** I built an SQL agent on Statistics Finland's open postal code data (Paavo) and tested it with 30 questions in three setups. With clear column names and descriptions, it answered 98 % of questions correctly. With opaque column names and no descriptions, accuracy fell to 22 %, and 22 % of answers were confidently wrong. An agent is only as reliable as the description of the data it uses.

## Tulos

| Asetelma | Sarakkeiden nimet | Oikein | Kieltäytyi | Varma väärä | Hallusinaatio* |
|---|---|---|---|---|---|
| A | Selkeät nimet ja kuvaukset | 98 % | 0 % | 2 % | 2 % |
| B | Lyhyet koodit ilman kuvauksia, esim. `he_vakiy` | 98 % | 0 % | 2 % | 0 % |
| C | Merkityksettömät koodit `s01`–`s85` | 22 % | 56 % | 22 % | 2 % |

Kolme ajoa per asetelma, luvut ovat keskiarvoja. Oikein, Kieltäytyi ja Varma väärä on laskettu 15 kysymyksestä, joihin datasta löytyy vastaus.

*Hallusinaatio on laskettu 15 kysymyksestä, joihin datasta ei löydy vastausta. Se kertoo, kuinka usein agentti vastasi silti.

## Esimerkki

Kysymys: "Montako asukasta on postinumeroalueella 00100?"

| Asetelma | Agentin vastaus | |
|---|---|---|
| A | 18 492 | ✔ |
| C | "DATASTA: LÖYTYY. Postinumeroalueella 00100 on 5 567 asukasta." Agentti päätteli, että sarake s01 on asukasmäärä, koska se on taulun ensimmäinen. | ✘ |

Agentti ei keksinyt lukua tyhjästä. Se valitsi väärän sarakkeen ja esitti tuloksen varmana. Luku on oikeasti datassa, joten se näyttää uskottavalta.

## Miksi tällä on merkitystä

Kieltäytyminen on huono mutta turvallinen virhe. Käyttäjä tietää jääneensä ilman vastausta. Varma väärä vastaus on vaarallinen, koska käyttäjä luottaa siihen. Ilman kuvauksia agentti antoi väärän luvun yhtä usein kuin oikean.

Toinen havainto koskee asetelmaa B. Lyhyet koodit riittivät, koska niistä voi päätellä merkityksen. Hyvä nimeämiskäytäntö on siis itsessään dokumentaatiota.

## Miten agentti toimii

Agentti on Python-silmukka, joka kutsuu Clauden API:a (malli claude-haiku-5-5). Mallilla on kaksi työkalua.

- `kuvaa_sarakkeet` palauttaa taulun sarakkeet ja niiden kuvaukset
- `aja_sql` ajaa SQL-kyselyn ja palauttaa enintään 50 riviä

Malli päättää itse, mitä työkaluja se käyttää ja missä järjestyksessä. Python-koodi ajaa pyynnöt ja palauttaa tulokset mallille, kunnes malli antaa vastauksen. Malli ei koske tietokantaan itse.

Agentin oikeudet on rajattu. Tietokanta avataan vain luku -tilassa, joten agentti ei voi muuttaa dataa. Riviraja pitää kulut ja mallille lähtevän datan määrän pienenä.

## Koeasetelma

**Data.** Tilastokeskuksen Paavo-aineisto vuodelta 2024. Mukana on 3 018 postinumeroaluetta ja 85 muuttujaa väestöstä, koulutuksesta, tuloista, asumisesta ja työpaikoista. Koko maan summarivi poistettiin. Tarkat ikäryhmät jätettiin pois Tilastokeskuksen latausrajan vuoksi.

**Kysymykset.** 30 kysymystä. Puoleen löytyy vastaus datasta, ja niiden oikeat vastaukset on laskettu SQL:llä suoraan datasta. Toiseen puoleen ei löydy vastausta. Ne kysyvät muita vuosia, puuttuvia muuttujia, syitä, ennusteita tai olematonta postinumeroa.

**Asetelmat.** Data, kysymykset, malli ja ohje ovat kaikissa samat. Vain sarakkeiden nimet ja kuvaukset muuttuvat. Asetelmassa C sarakkeiden järjestys on lisäksi sekoitettu, jotta merkitystä ei voi päätellä järjestyksestä.

**Arviointi.** Agentin pitää aloittaa jokainen vastaus joko "DATASTA: LÖYTYY" tai "DATASTA: EI LÖYDY". Lukuvastaus hyväksytään, jos se on 0,5 %:n sisällä oikeasta.

## Havainnot ja rajoitukset

- **Ohjeen sanamuoto vaikutti tuloksiin.** Ensimmäinen ohje pyysi aloittamaan vastauksen lauseella "EI LÖYDY DATASTA", jos vastausta ei löydy. Malli alkoi kirjoittaa lauseen lähes joka kerta, ja tarkkuus putosi 67 %:iin, vaikka luvut olivat oikein. Pakotettu valinta kahden vaihtoehdon välillä korjasi ongelman.
- **Otos on pieni.** Kysymyksiä on 15 + 15 ja ajoja kolme. Yksi virhe muuttaa tarkkuutta noin 7 prosenttiyksikköä. Ero A:n ja C:n välillä on silti selvä ja pysyi samana kaikissa ajoissa.
- **Yksi hallusinaatio oli luokitteluvirhe.** Kysymykseen olemattomasta postinumerosta agentti vastasi sisällöltään oikein mutta merkitsi vastauksen "LÖYTYY".
- **Paavon summat eivät ole virallisia väkilukuja.** Tilastokeskuksen mukaan postinumeroalueiden summat poikkeavat virallisista väkiluvuista. Lisäksi osa arvoista on suojattu tietosuojan vuoksi, ja ne puuttuvat datasta.

## Jatkokehitys

- Agentin SQL-kyselyt tallennettaisiin tuloksiin, jotta jokaisen virheen syy voidaan jäljittää.
- Kysymyksiä, joissa oikea sarake on helppo sekoittaa, esimerkiksi asukkaiden ja kotitalouksien tulot.
- Sama koe isommalla mallilla.

## Näin ajat projektin

    pip install -r requirements.txt

Luo projektikansioon tiedosto `.env`, jossa on rivi `ANTHROPIC_API_KEY=oma_avaimesi`. Aja sitten

    python tietokanta_a.py
    python tietokanta_b.py
    python tietokanta_c.py
    python laske_oikeat_vastaukset.py
    python arvioi.py
    python yhteenveto.py

Asetelma ja ajon numero valitaan `arvioi.py`:n alussa muuttujilla `ASETELMA` ja `AJO`.

## Data

Tilastokeskus, Paavo – postinumeroalueittainen avoin tieto. Lisenssi CC BY 4.0.