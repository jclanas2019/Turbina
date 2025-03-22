def get_context():
    return {
        "title": "Formulario de Registro",
        "message": "Completa los siguientes campos para registrar un nuevo usuario.",

        "form_data": {
            "nombre": "Juan Pérez",
            "email": "juan.perez@example.com",
            "password": "123456",
            "rol": "editor",
            "genero": "masculino",
            "terminos": True,
            "comentarios": "Me interesa participar en el piloto del sistema."
        },

        # Opcional: podrías incluir errores si haces validación básica
        "errors": {
            # "email": "Correo inválido.",
            # "password": "Debe tener al menos 6 caracteres."
        }
    }
