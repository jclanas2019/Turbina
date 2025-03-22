document.addEventListener("DOMContentLoaded", function() {
    // Gráfico de ventas
    const ctx = document.getElementById('salesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
            datasets: [{
                label: 'Ventas',
                data: [120, 190, 300, 500, 200, 300],
                borderColor: 'blue',
                fill: false
            }]
        }
    });

    // Calendario FullCalendar
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: [
            { title: 'Reunión con equipo', start: '2024-04-10' },
            { title: 'Entrega de proyecto', start: '2024-04-15' },
            { title: 'Mantenimiento Servidor', start: '2024-04-20' }
        ]
    });
    calendar.render();
});
