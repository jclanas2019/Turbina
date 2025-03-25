import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.database import Base, engine, SessionLocal
from app.models.usuario import Usuario
from passlib.hash import bcrypt

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if db.query(Usuario).first() is None:
    usuarios = [
        {"username": "admin", "password": "admin123", "rol": "admin"},
        {"username": "usuario", "password": "clave123", "rol": "usuario"}
    ]
    for u in usuarios:
        user = Usuario(
            username=u["username"],
            hashed_password=bcrypt.hash(u["password"]),
            rol=u["rol"]
        )
        db.add(user)
    db.commit()

db.close()
