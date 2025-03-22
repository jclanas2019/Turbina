from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Ruta GET para mostrar login
@router.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

# Ruta POST para procesar login
@router.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    remember: bool = Form(False)
):
    # ⚠️ Simulación de validación de credenciales
    if username == "admin" and password == "1234":
        response = RedirectResponse(url="/", status_code=303)
        # Aquí podrías setear cookies o sesiones reales
        return response

    # Si falla, muestra el login con mensaje de error
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Credenciales incorrectas. Inténtalo nuevamente."
    })
