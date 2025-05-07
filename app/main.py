# main.py
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database import SessionLocal, User
from auth import get_db, hash_password, verify_password
import uvicorn
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: SessionLocal = Depends(get_db)):
    hashed = hash_password(password)
    user = User(username=username, email=email, password=hashed, role="user")
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/login")
def login_user(username: str = Form(...), password: str = Form(...), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        return RedirectResponse("/home", status_code=303)
    return HTMLResponse("Login fehlgeschlagen", status_code=401)

@app.get("/home", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    # 🧪 Ersetze hier später durch den echten eingeloggten User
    user = db.query(User).filter(User.username == "admin").first()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": user
    })


@app.get("/admin", response_class=HTMLResponse)
def admin_users(request: Request, db: Session = Depends(get_db)):
    # Simulierter Login-Nutzer (du kannst später Session/JWT nutzen)
    current_user = db.query(User).filter(User.username == "admin").first()

    if not current_user or current_user.role != "admin":
        return HTMLResponse("<h3>Kein Zugriff! Nur für Admins.</h3>", status_code=403)

    users = db.query(User).all()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "users": users
    })



@app.get("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/edit/{user_id}", response_class=HTMLResponse)
def edit_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.post("/edit/{user_id}")
def update_user(
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).get(user_id)
    if user:
        user.username = username
        user.email = email
        user.role = role
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

from database import SessionLocal
from auth import hash_password

def create_admin():
    db = SessionLocal()
    username = "admin"
    email = "admin@example.com"
    password = "admin123"
    hashed = hash_password(password)

    existing = db.query(User).filter(User.username == username).first()
    if not existing:
        admin = User(username=username, email=email, password=hashed, role="admin")
        db.add(admin)
        db.commit()
        print("✅ Admin wurde erstellt!")
    else:
        print("⚠️ Admin existiert bereits.")
    db.close()

create_admin()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)



