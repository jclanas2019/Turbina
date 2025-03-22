from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.views.dashboard_data import get_dashboard_context
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    context = get_dashboard_context()
    context["request"] = request
    return templates.TemplateResponse("dashboard.html", context)
