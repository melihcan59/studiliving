import csv
from database import SessionLocal, Property

db = SessionLocal()

with open("immobilien.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        # Leere oder falsche Keys bereinigen
        row = {k.strip(): v for k, v in row.items()}

        neue_immobilie = Property(
            name=row["Name"],
            bundesland=row["Bundesland"],
            stadt=row["Stadt"],
            strasse=row["Straße"],
            plz=row["PLZ"],
            latitude=float(row["Latitude"]),
            longitude=float(row["Longitude"]),
            gebaeude_id=0,  # oder setze hier falls bekannt
            gebaeudekategorie=row["Gebäudekategorie"],
            kurzbeschreibung=row["Kurzbeschreibung"],
            beschreibung=row["Beschreibung"],
            preis=row["Preis (€)"],
            bild_url=row.get("Bild-URL", ""),
            owner_id=1  # manuell setzen oder aus Session/externer Quelle
        )

        db.add(neue_immobilie)

db.commit()
db.close()
print("✅ Immobilien erfolgreich importiert.")

