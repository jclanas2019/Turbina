import os
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from app.core.auth import verificar_login
from app.views import formulario_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/formulario", response_class=HTMLResponse)
async def get_formulario(request: Request):
    redirect = await verificar_login(request)
    if redirect:
        return redirect

    context = formulario_data.get_context()
    context["request"] = request
    context["usuario"] = request.cookies.get("usuario")
    return templates.TemplateResponse("formulario.html", context)

@router.post("/formulario", response_class=HTMLResponse)
async def post_formulario(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    rol: str = Form(...),
    genero: str = Form(...),
    terminos: bool = Form(False),
    comentarios: str = Form("")
):
    redirect = await verificar_login(request)
    if redirect:
        return redirect

    print("✅ Formulario recibido:", {
        "nombre": nombre,
        "email": email,
        "password": password,
        "rol": rol,
        "genero": genero,
        "terminos": terminos,
        "comentarios": comentarios
    })

    response = RedirectResponse(url="/formulario", status_code=303)
    return response
