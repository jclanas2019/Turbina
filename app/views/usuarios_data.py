from typing import List, Dict

# Simulación de base de datos en memoria
_usuarios_db = [
    {"id": 1, "nombre": "Juan Pérez", "email": "juan.perez@example.com"},
    {"id": 2, "nombre": "María Gómez", "email": "maria.gomez@example.com"},
    {"id": 3, "nombre": "Pedro López", "email": "pedro.lopez@example.com"},
]

def get_context() -> Dict:
    """
    Devuelve un diccionario de contexto para la vista de usuarios.
    """
    context = {
        "type": "crud",
        "title": "Gestión de Usuarios",
        "message": "Bienvenido al sistema de gestión de usuarios.",
        "usuarios": _usuarios_db
    }
    return context

def get_items() -> List[Dict]:
    """
    Devuelve una lista de todos los usuarios.
    """
    return _usuarios_db

def get_item(usuario_id: int) -> Dict:
    """
    Devuelve un usuario por su ID.
    """
    return next((u for u in _usuarios_db if u["id"] == usuario_id), None)

def create_item(usuario: Dict) -> Dict:
    """
    Crea un nuevo usuario.
    """
    nuevo_id = max([u["id"] for u in _usuarios_db], default=0) + 1
    nuevo_usuario = {"id": nuevo_id, **usuario}
    _usuarios_db.append(nuevo_usuario)
    return nuevo_usuario

def update_item(usuario_id: int, nuevos_datos: Dict) -> Dict:
    """
    Actualiza un usuario existente.
    """
    usuario = get_item(usuario_id)
    if usuario:
        usuario.update(nuevos_datos)
    return usuario

def delete_item(usuario_id: int) -> bool:
    """
    Elimina un usuario existente por ID.
    """
    global _usuarios_db
    original_len = len(_usuarios_db)
    _usuarios_db = [u for u in _usuarios_db if u["id"] != usuario_id]
    return len(_usuarios_db) < original_len
