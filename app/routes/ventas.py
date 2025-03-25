from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.views import ventas_data
from app.core.auth import verificar_login  # protección
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/ventas", response_class=HTMLResponse)
async def ventas_view(request: Request):
    redirect = await verificar_login(request)
    if redirect:
        return redirect

    context = ventas_data.get_context()
    context["request"] = request
    context["usuario"] = request.cookies.get("usuario")
    return templates.TemplateResponse("ventas.html", context)
