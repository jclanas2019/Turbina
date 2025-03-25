from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.views.dashboard_data import get_dashboard_context
from app.core.auth import verificar_login
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    redirect = await verificar_login(request)
    if redirect:
        return redirect

    context = get_dashboard_context()
    context["request"] = request
    context["usuario"] = request.cookies.get("usuario")
    return templates.TemplateResponse("dashboard.html", context)
