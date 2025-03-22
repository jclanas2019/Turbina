import os
from app.views import usuarios_data

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

usuarios_router = APIRouter()

templates_dir = os.path.join(os.path.dirname(__file__), "../templates")
templates = Jinja2Templates(directory=templates_dir)

@usuarios_router.get('/usuarios', response_class=HTMLResponse)
async def get_usuarios(request: Request):
    context = usuarios_data.get_context()
    context['request'] = request
    return templates.TemplateResponse('usuarios.html', context=context)

router = usuarios_router
