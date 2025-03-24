# scripts/init_db.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.database import Base, engine, SessionLocal
from app.models.report import Report
from app.views.reportes_data import get_context as datos_estaticos

from faker import Faker
import random

fake = Faker()

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# --- Datos estáticos si está vacío ---
if db.query(Report).first() is None:
    contexto = datos_estaticos()
    for categoria in ["reportes_ventas", "reportes_clientes", "reportes_productos"]:
        for r in contexto[categoria]:
            nuevo = Report(
                categoria=categoria.replace("reportes_", "").capitalize(),
                icon=r["icon"],
                titulo=r["titulo"],
                valor=r["valor"],
                color=r["color"]
            )
            db.add(nuevo)

# --- Datos dinámicos adicionales con Faker ---
categorias = {
    "Ventas": "💵",
    "Clientes": "👤",
    "Productos": "📦"
}

colores = ["red", "green", "blue", "yellow", "orange", "purple", "teal"]

for categoria, icono in categorias.items():
    for _ in range(10):  # 10 registros por categoría
        titulo = fake.bs().capitalize()
        valor = fake.pricetag() if categoria == "Ventas" else fake.random_element(elements=("15%", "80 unidades", "5 items", "★★★☆☆"))
        resumen = f"{fake.word().capitalize()} {fake.color_name()} {fake.word()}"
        nuevo = Report(
            categoria=categoria,
            icon=icono,
            titulo=titulo,
            valor=valor,
            color=random.choice(colores)
        )
        db.add(nuevo)

db.commit()
db.close()
