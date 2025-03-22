def get_context():
    return {
        "title": "Panel de Ventas",
        "message": "Resumen de las ventas más recientes y su evolución.",
        "resumen": [
            {"icon": "💰", "title": "Total Ventas", "value": "$98.000", "color": "green"},
            {"icon": "🛒", "title": "Órdenes", "value": "320", "color": "blue"},
            {"icon": "📈", "title": "Promedio", "value": "$306", "color": "teal"},
            {"icon": "📦", "title": "Productos", "value": "87", "color": "orange"},
        ],
        "ventas": [
            {"id": 101, "cliente": "Juan Pérez", "producto": "Laptop", "monto": 850, "estado": "Pagado", "color": "green"},
            {"id": 102, "cliente": "Ana Díaz", "producto": "Teclado", "monto": 45, "estado": "Pendiente", "color": "yellow"},
            {"id": 103, "cliente": "Carlos Ruiz", "producto": "Monitor", "monto": 220, "estado": "Cancelado", "color": "red"},
        ]
    }
