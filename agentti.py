import anthropic
from dotenv import load_dotenv
from tyokalut import aja_sql, kuvaa_sarakkeet

load_dotenv()
client = anthropic.Anthropic()

TYOKALUT = [
    {
        "name": "kuvaa_sarakkeet",
        "description": "Palauttaa listan taulun alueet sarakkeista ja niiden kuvaukset. Käytä tätä ennen kuin kirjoitat SQL-kyselyn.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "aja_sql",
        "description": "Ajaa SQLite-kyselyn tietokantaan ja palauttaa enintään 50 riviä. Vain lukeminen on sallittu.",
        "input_schema": {
            "type": "object",
            "properties": {
                "kysely": {"type": "string", "description": "SQL SELECT -kysely"}
            },
            "required": ["kysely"],
        },
    },
]

JARJESTELMAOHJE = (
    "Vastaat kysymyksiin Suomen postinumeroalueista käyttämällä tietokantaa. "
    "Hae vastaukset aina tietokannasta. Vastaa lyhyesti suomeksi. "
    "Aloita vastauksesi aina omalla rivillään joko 'DATASTA: LÖYTYY' tai 'DATASTA: EI LÖYDY'. "
    "Valitse EI LÖYDY vain, jos kysymykseen ei voi vastata suoraan tietokannan tiedoilla, "
    "esimerkiksi syy-kysymykset, ennusteet tai muut vuodet kuin 2024. "
    "Kirjoita sen jälkeen vastaus tai kerro, mitä data aiheesta näyttää."
)

def aja_tyokalu(nimi, syote):
    if nimi == "kuvaa_sarakkeet":
        return kuvaa_sarakkeet()
    if nimi == "aja_sql":
        return aja_sql(syote["kysely"])
    return f"Tuntematon työkalu: {nimi}"


def kysy_agentilta(kysymys, max_kierrokset=10):
    viestit = [{"role": "user", "content": kysymys}]

    for kierros in range(max_kierrokset):
        vastaus = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=2000,
            system=JARJESTELMAOHJE,
            tools=TYOKALUT,
            messages=viestit,
        )
        viestit.append({"role": "assistant", "content": vastaus.content})

        if vastaus.stop_reason != "tool_use":
            for block in vastaus.content:
                if block.type == "text":
                    return block.text
            return ""

        tulokset = []
        for block in vastaus.content:
            if block.type == "tool_use":
                print(f"  -> {block.name}: {block.input}")
                tulos = aja_tyokalu(block.name, block.input)
                tulokset.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": tulos,
                })
        viestit.append({"role": "user", "content": tulokset})

    return "Kierrosraja täyttyi."