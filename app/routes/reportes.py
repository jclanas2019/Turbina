from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.views import reportes_data
from app.core.auth import verificar_login
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/reportes", response_class=HTMLResponse)
async def reportes_view(request: Request):
    redirect = await verificar_login(request)
    if redirect:
        return redirect

    context = reportes_data.get_context()
    context["request"] = request
    context["usuario"] = request.cookies.get("usuario")
    return templates.TemplateResponse("reportes.html", context)
