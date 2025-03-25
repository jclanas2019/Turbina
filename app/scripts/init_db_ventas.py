import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.database import Base, engine, SessionLocal
from app.models.venta import Venta

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(Venta).first() is None:
    ventas = [
        {"cliente": "Juan Pérez", "producto": "Laptop", "monto": 1200.00, "estado": "Pagado", "color": "green"},
        {"cliente": "Ana Gómez", "producto": "Mouse", "monto": 25.50, "estado": "Pendiente", "color": "yellow"},
        {"cliente": "Carlos Ruiz", "producto": "Teclado", "monto": 45.00, "estado": "Pagado", "color": "green"},
        {"cliente": "Sofía Díaz", "producto": "Monitor", "monto": 300.00, "estado": "Pendiente", "color": "red"},
        {"cliente": "Lucía Torres", "producto": "Silla", "monto": 150.00, "estado": "Pagado", "color": "blue"},
    ]
    for v in ventas:
        venta = Venta(**v)
        db.add(venta)
    db.commit()

db.close()
