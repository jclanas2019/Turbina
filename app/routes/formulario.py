from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.views import formulario_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/formulario")
async def get_formulario(request: Request):
    context = formulario_data.get_context()
    context["request"] = request
    return templates.TemplateResponse("formulario.html", context)


@router.post("/formulario")
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
    # Aquí puedes hacer validaciones o guardar en base de datos
    print("✅ Formulario recibido:", {
        "nombre": nombre,
        "email": email,
        "password": password,
        "rol": rol,
        "genero": genero,
        "terminos": terminos,
        "comentarios": comentarios
    })

    # Redirige al mismo formulario con mensaje de éxito (podrías renderizar otra vista si prefieres)
    response = RedirectResponse(url="/formulario", status_code=303)
    return response
