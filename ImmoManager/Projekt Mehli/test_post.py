import requests

payload = {
    "Name": "Testhaus",
    "Beschreibung": "Tolles Testhaus",
    "Straße": "Teststraße 1",
    "Stadt": "Teststadt",
    "Bundesland": "",
    "PLZ": "00000",
    "Gebäudekategorie": "Haus",
    "Preis": 123456,
    "Koordinaten": "0,0",
    "BildURL": "https://via.placeholder.com/400x300"
}

res = requests.post("http://127.0.0.1:5000/api/immobilien", json=payload)
print(res.status_code)
print(res.json())
