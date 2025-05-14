import pandas as pd
from sqlalchemy import create_engine

# Datei evtl. umbenennen in 'datensatz.csv'
df = pd.read_csv("Datensatz.csv")
engine = create_engine("sqlite:///immobilien.db")
df.to_sql("immobilien", engine, index=False, if_exists="replace")

print("✅ Datenbank erfolgreich erstellt.")

