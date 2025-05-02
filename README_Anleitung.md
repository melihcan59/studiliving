# 👥 Team-Arbeitsweise – GitHub-Workflow für Studiliving

Damit wir alle gleichzeitig an „**Studiliving**“ arbeiten können, folgen wir einem festen Ablauf.  
Jede*r arbeitet **in einem eigenen Branch**, damit nichts kaputt geht. Am Ende wird alles sauber zusammengeführt.

---

## ✅ Schritt 1: Projekt von GitHub auf den eigenen Rechner holen

Nur 1x nötig:

```bash
git clone https://github.com/melihcan59/studiliving.git
cd studiliving
```

---

## ✅ Schritt 2: Eigenen Branch erstellen

Bevor du etwas programmierst, erstelle einen Branch für deinen Aufgabenbereich:

```bash
git checkout -b NAME_DEINER_AUFGABE
```

**Beispiele:**
- `backend-auth` → Login / Registrierung
- `backend-wohnungen` → CRUD für Wohnungen
- `frontend-layout` → HTML-Seiten bauen
- `frontend-map` → Kartenanzeige mit Leaflet

---

## ✅ Schritt 3: Arbeiten & regelmäßig speichern

Wenn du etwas fertig hast:

```bash
git add .
git commit -m "Kurzbeschreibung deiner Änderung"
```

Dann den Branch online pushen:

```bash
git push origin NAME_DEINES_BRANCHES
```

---

## ✅ Schritt 4: Merge über GitHub (Pull Request)

Wenn dein Feature fertig ist:

1. Gehe auf GitHub
2. Du siehst „**Compare & Pull Request**“ → draufklicken
3. Schreibe kurz rein, was du gemacht hast
4. Ein anderes Teammitglied klickt „**Merge**“ → Änderung wird in `main` übernommen

---

## ✅ Schritt 5: `main` aktualisieren

Bevor du neue Aufgaben anfängst:

```bash
git checkout main
git pull origin main
```

So hast du immer den neuesten Stand.

---

## 🧠 Warum das Ganze?

- Niemand überschreibt versehentlich fremden Code
- Alle können **gleichzeitig arbeiten**
- Ihr entdeckt Fehler früh
- Der `main`-Branch bleibt **stabil und lauffähig**
