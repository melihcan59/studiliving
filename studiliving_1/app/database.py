from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")

    # Neue Felder
    typ = Column(String, default="student")
    alter = Column(Integer, nullable=True)
    stadt = Column(String, nullable=True)
    plz = Column(String, nullable=True)
    land = Column(String, nullable=True)
    ueber_mich = Column(String, nullable=True)

    # Beziehung zu Immobilien
    properties = relationship("Property", back_populates="owner")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    titel = Column(String)
    strasse = Column(String)
    plz = Column(String)
    stadt = Column(String)
    bundesland = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    kaltmiete = Column(Float)
    warmmiete = Column(Float)
    wohnflaeche = Column(Float)
    zimmer = Column(Integer)
    schlafzimmer = Column(Integer)
    badezimmer = Column(Integer)
    bezugsfrei_ab = Column(String)
    etage = Column(String)
    typ = Column(String)  # z. B. "Erdgeschosswohnung"
    ausstattung = Column(String)  # z. B. "Balkon, Einbauküche"
    garage = Column(String)  # z. B. "Tiefgarage, Außenstellplatz"
    internet = Column(String)  # z. B. "Verfügbar"
    kurzbeschreibung = Column(String)
    beschreibung = Column(String)
    bild_url = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="properties")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
