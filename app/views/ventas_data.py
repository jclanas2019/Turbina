from app.core.database import SessionLocal, Base, engine
from app.models.venta import Venta

Base.metadata.create_all(bind=engine)

def get_context():
    db = SessionLocal()
    ventas = db.query(Venta).all()
    db.close()

    resumen = [
        {"icon": "🧾", "title": "Total Ventas", "value": f"${sum(v.monto for v in ventas):,.0f}", "color": "green"},
        {"icon": "👤", "title": "Clientes", "value": f"{len(set(v.cliente for v in ventas))}", "color": "blue"},
        {"icon": "📦", "title": "Productos", "value": f"{len(set(v.producto for v in ventas))}", "color": "yellow"},
        {"icon": "📊", "title": "Pendientes", "value": f"{sum(1 for v in ventas if v.estado.lower() == 'pendiente')}", "color": "red"},
    ]

    return {
        "title": "Ventas",
        "message": "Revisa el estado y resumen de las ventas registradas.",
        "resumen": resumen,
        "ventas": ventas,
    }
