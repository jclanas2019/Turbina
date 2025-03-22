import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import dashboard
from app.routes import usuarios
from app.routes import ventas
from app.routes import reportes
from app.routes import formulario
from app.routes import login

app = FastAPI()

# Directorio estático
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Rutas incluidas
app.include_router(dashboard.router)
app.include_router(usuarios.router)
app.include_router(ventas.router)
app.include_router(reportes.router)
app.include_router(formulario.router)
app.include_router(login.router)

# API de eventos del calendario
@app.get("/api/events")
def calendar_events():
    import datetime
    today = datetime.date.today()
    return [
        {"title": "Reunión con equipo", "start": str(today)},
        {"title": "Entrega de proyecto", "start": str(today + datetime.timedelta(days=5))},
        {"title": "Mantenimiento Servidor", "start": str(today + datetime.timedelta(days=10))}
    ]
