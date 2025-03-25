from fastapi import Request
from fastapi.responses import RedirectResponse

async def verificar_login(request: Request):
    if not request.cookies.get("usuario"):
        return RedirectResponse(url="/login", status_code=302)
    return None
