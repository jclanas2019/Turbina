from app.core.database import SessionLocal
from app.models.report import Report

def get_context():
    db = SessionLocal()
    reportes = db.query(Report).all()
    db.close()

    print(f"[DEBUG] Total reportes: {len(reportes)}")  # Verifica en consola

    ventas, clientes, productos = [], [], []

    for r in reportes:
        item = {
            "icon": r.icon,
            "titulo": r.titulo,
            "valor": r.valor,
            "color": r.color
        }
        if r.categoria.lower() == "ventas":
            ventas.append(item)
        elif r.categoria.lower() == "clientes":
            clientes.append(item)
        elif r.categoria.lower() == "productos":
            productos.append(item)

    print(f"[DEBUG] Ventas: {len(ventas)} | Clientes: {len(clientes)} | Productos: {len(productos)}")

    return {
        "title": "Reportes",
        "message": "Visualiza los indicadores clave de cada sección.",
        "reportes_ventas": ventas,
        "reportes_clientes": clientes,
        "reportes_productos": productos,
    }
