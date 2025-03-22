import datetime

def get_dashboard_context():
    today = datetime.date.today()

    return {
        "stats": [
            {"icon": "💰", "title": "Ganancias", "value": "$1,232", "color": "primary"},
            {"icon": "📈", "title": "Ventas", "value": "764", "color": "success"},
            {"icon": "🚀", "title": "Progreso", "value": "34%", "color": "warning"},
            {"icon": "⚠", "title": "Alertas", "value": "12", "color": "danger"},
        ],
        "orders": [
            {"id": "54331", "user": "Steve Horton", "amount": "45.00", "status": "Pagado", "color": "success"},
            {"id": "54332", "user": "Lucy Doe", "amount": "38.00", "status": "Enviado", "color": "info"},
            {"id": "54333", "user": "Mike Lowrey", "amount": "127.00", "status": "Pendiente", "color": "warning"},
            {"id": "54334", "user": "Anna Smith", "amount": "98.00", "status": "Cancelado", "color": "danger"},
        ],
        "tasks": [
            {"label": "Revisar Reportes", "status": "danger"},
            {"label": "Actualizar servidores", "status": "warning"},
            {"label": "Rediseño del logo", "status": "primary"},
        ],
        "calendar_events": [
            {"title": "Reunión con equipo", "start": "2024-04-10"},
            {"title": "Entrega de proyecto", "start": "2024-04-15"},
            {"title": "Mantenimiento Servidor", "start": "2024-04-20"},
        ],
        "workflow_steps": [
            {"title": "📌 Inicio", "desc": "Definir objetivos y alcance", "color": "info"},
            {"title": "⚙️ Proceso", "desc": "Desarrollo y pruebas", "color": "warning"},
            {"title": "✅ Finalización", "desc": "Entrega y validación", "color": "success"},
        ]
    }
