import os
import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, User, Property
from auth import get_db, hash_password, verify_password
from fastapi.responses import RedirectResponse


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="geheimespasswort123")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

# ------------- AUTHENTIFIZIERUNG -------------
@app.post("/register")
def register_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...),
                  db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Benutzername oder E-Mail existiert bereits")

    hashed = hash_password(password)
    user = User(username=username, email=email, password=hashed, role="user")
    db.add(user)
    db.commit()

    # Automatisch einloggen
    request.session["user"] = {"id": user.id, "username": user.username, "role": user.role}

    # Weiterleitung zur Startseite
    return RedirectResponse(url="/static/index.html", status_code=303)


@app.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        request.session["user"] = {"id": user.id, "username": user.username, "role": user.role}
        return RedirectResponse(url="/static/index.html", status_code=303)
    raise HTTPException(status_code=401, detail="Login fehlgeschlagen")


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logout erfolgreich"}

# ------------- PROFIL -------------
@app.get("/profil")
def profil_page(request: Request, db: Session = Depends(get_db)):
    user_session = request.session.get("user")
    if not user_session:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    user = db.query(User).get(user_session["id"])
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "typ": user.typ,
        "alter": user.alter,
        "stadt": user.stadt,
        "plz": user.plz,
        "land": user.land,
        "ueber_mich": user.ueber_mich
    }

@app.post("/profil/update")
def update_profil(request: Request, typ: str = Form(...), alter: int = Form(...), stadt: str = Form(...), plz: str = Form(...), land: str = Form(...), ueber_mich: str = Form(...), db: Session = Depends(get_db)):
    user_session = request.session.get("user")
    if not user_session:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    user = db.query(User).get(user_session["id"])
    user.typ = typ
    user.alter = alter
    user.stadt = stadt
    user.plz = plz
    user.land = land
    user.ueber_mich = ueber_mich
    db.commit()
    return {"message": "Profil aktualisiert"}

# ------------- IMMOBILIEN CRUD -------------
@app.post("/properties/create")
def create_property(request: Request, name: str = Form(...), bundesland: str = Form(...), stadt: str = Form(...), strasse: str = Form(...), plz: str = Form(...), latitude: float = Form(...), longitude: float = Form(...), gebaeude_id: int = Form(...), gebaeudekategorie: str = Form(...), kurzbeschreibung: str = Form(...), beschreibung: str = Form(...), preis: str = Form(...), bild_url: str = Form(...), db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    new_prop = Property(
        name=name, bundesland=bundesland, stadt=stadt, strasse=strasse, plz=plz,
        latitude=latitude, longitude=longitude, gebaeude_id=gebaeude_id,
        gebaeudekategorie=gebaeudekategorie, kurzbeschreibung=kurzbeschreibung,
        beschreibung=beschreibung, preis=preis, bild_url=bild_url,
        owner_id=user["id"]
    )
    db.add(new_prop)
    db.commit()
    return {"message": "Immobilie erstellt"}

@app.get("/properties")
def list_properties(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    if user["role"] == "admin":
        properties = db.query(Property).all()
    else:
        properties = db.query(Property).filter(Property.owner_id == user["id"]).all()
    return properties

@app.get("/properties/public")
def public_market(db: Session = Depends(get_db)):
    return db.query(Property).all()

@app.put("/properties/{id}")
def update_property(id: int, request: Request, db: Session = Depends(get_db), name: str = Form(...)):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    prop = db.query(Property).filter(Property.id == id, Property.owner_id == user["id"]).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    prop.name = name
    db.commit()
    return {"message": "Immobilie aktualisiert"}

@app.delete("/properties/{id}")
def delete_property(id: int, request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    prop = db.query(Property).filter(Property.id == id, Property.owner_id == user["id"]).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    db.delete(prop)
    db.commit()
    return {"message": "Immobilie gelöscht"}

# ------------- ADMIN FUNKTIONEN -------------
@app.get("/users")
def get_users(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Kein Zugriff")
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="geheimespasswort123")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

# ------------- AUTHENTIFIZIERUNG -------------
@app.post("/register")
def register_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...),
                  db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Benutzername oder E-Mail existiert bereits")

    hashed = hash_password(password)
    user = User(username=username, email=email, password=hashed, role="user")
    db.add(user)
    db.commit()

    # Automatisch einloggen
    request.session["user"] = {"id": user.id, "username": user.username, "role": user.role}

    # Weiterleitung zur Startseite
    return RedirectResponse(url="/static/index.html", status_code=303)


@app.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        request.session["user"] = {"id": user.id, "username": user.username, "role": user.role}
        return RedirectResponse(url="/static/index.html", status_code=303)
    raise HTTPException(status_code=401, detail="Login fehlgeschlagen")


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logout erfolgreich"}

# ------------- PROFIL -------------
@app.get("/profil")
def profil_page(request: Request, db: Session = Depends(get_db)):
    user_session = request.session.get("user")
    if not user_session:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    user = db.query(User).get(user_session["id"])
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "typ": user.typ,
        "alter": user.alter,
        "stadt": user.stadt,
        "plz": user.plz,
        "land": user.land,
        "ueber_mich": user.ueber_mich
    }

@app.post("/profil/update")
def update_profil(request: Request, typ: str = Form(...), alter: int = Form(...), stadt: str = Form(...), plz: str = Form(...), land: str = Form(...), ueber_mich: str = Form(...), db: Session = Depends(get_db)):
    user_session = request.session.get("user")
    if not user_session:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    user = db.query(User).get(user_session["id"])
    user.typ = typ
    user.alter = alter
    user.stadt = stadt
    user.plz = plz
    user.land = land
    user.ueber_mich = ueber_mich
    db.commit()
    return {"message": "Profil aktualisiert"}

# ------------- IMMOBILIEN CRUD -------------

@app.post("/properties/create")
def create_property(
    request: Request,
    name: str = Form(...),
    bundesland: str = Form(...),
    stadt: str = Form(...),
    strasse: str = Form(...),
    plz: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    gebaeude_id: int = Form(...),
    gebaeudekategorie: str = Form(...),
    kurzbeschreibung: str = Form(...),
    beschreibung: str = Form(...),
    preis: str = Form(...),
    bild_url: str = Form(...),
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")

    new_prop = Property(
        name=name,
        bundesland=bundesland,
        stadt=stadt,
        strasse=strasse,
        plz=plz,
        latitude=latitude,
        longitude=longitude,
        gebaeude_id=gebaeude_id,
        gebaeudekategorie=gebaeudekategorie,
        kurzbeschreibung=kurzbeschreibung,
        beschreibung=beschreibung,
        preis=preis,
        bild_url=bild_url,
        owner_id=user["id"]
    )
    db.add(new_prop)
    db.commit()

    return RedirectResponse(url="/static/success.html", status_code=303)

@app.get("/properties")
def list_properties(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    if user["role"] == "admin":
        properties = db.query(Property).all()
    else:
        properties = db.query(Property).filter(Property.owner_id == user["id"]).all()
    return properties

@app.get("/properties/public")
def public_market(db: Session = Depends(get_db)):
    return db.query(Property).all()

@app.post("/properties/update/{id}")
def update_property(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(...),
    bundesland: str = Form(...),
    stadt: str = Form(...),
    strasse: str = Form(...),
    plz: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    gebaeude_id: int = Form(...),
    gebaeudekategorie: str = Form(...),
    kurzbeschreibung: str = Form(...),
    beschreibung: str = Form(...),
    preis: str = Form(...),
    bild_url: str = Form(...)
):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")

    prop = db.query(Property).filter(Property.id == id, Property.owner_id == user["id"]).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Nicht gefunden")

    # Alle Felder aktualisieren
    prop.name = name
    prop.bundesland = bundesland
    prop.stadt = stadt
    prop.strasse = strasse
    prop.plz = plz
    prop.latitude = latitude
    prop.longitude = longitude
    prop.gebaeude_id = gebaeude_id
    prop.gebaeudekategorie = gebaeudekategorie
    prop.kurzbeschreibung = kurzbeschreibung
    prop.beschreibung = beschreibung
    prop.preis = preis
    prop.bild_url = bild_url

    db.commit()
    return RedirectResponse(url="/static/property_updated.html", status_code=303)



@app.delete("/properties/{id}")
def delete_property(id: int, request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    prop = db.query(Property).filter(Property.id == id, Property.owner_id == user["id"]).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Nicht gefunden")
    db.delete(prop)
    db.commit()
    return {"message": "Immobilie gelöscht"}

# ------------- ADMIN FUNKTIONEN -------------
@app.get("/users")
def get_users(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Kein Zugriff")
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
def root():
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
