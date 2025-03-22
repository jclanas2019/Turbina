def get_context():
    return {
        "title": "Reportes",
        "message": "Visualiza los indicadores clave de cada sección.",

        "reportes_ventas": [
            {"icon": "💰", "titulo": "Ingresos", "valor": "$25.000", "color": "green"},
            {"icon": "📉", "titulo": "Devoluciones", "valor": "$2.300", "color": "red"},
            {"icon": "📊", "titulo": "Crecimiento", "valor": "12%", "color": "blue"},
        ],

        "reportes_clientes": [
            {"icon": "👥", "titulo": "Nuevos Clientes", "valor": "120", "color": "blue"},
            {"icon": "📞", "titulo": "Contactos Activos", "valor": "87", "color": "purple"},
            {"icon": "🔁", "titulo": "Clientes Recurrentes", "valor": "34", "color": "green"},
        ],

        "reportes_productos": [
            {"icon": "📦", "titulo": "Stock Bajo", "valor": "14 ítems", "color": "yellow"},
            {"icon": "🔥", "titulo": "Más Vendidos", "valor": "5 productos", "color": "orange"},
            {"icon": "⭐", "titulo": "Promedio de Reviews", "valor": "4.5 ★", "color": "teal"},
        ]
    }
