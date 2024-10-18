from django.shortcuts import render, redirect
from tickets.models import Ticket
from clientes.models import Clientes

def dashboard_view(request):
    # Verificar si el usuario está autenticado
    if 'user_id' not in request.session:
        return redirect('login')

    # Obtener las estadísticas utilizando los métodos del modelo
    total_clientes = Clientes.total_clientes()
    total_tickets = Ticket.total_tickets()
    tickets_en_proceso = Ticket.total_en_proceso()
    tickets_pendientes = Ticket.total_pendientes()
    tickets_sin_tecnico = Ticket.total_sin_tecnico()
    tickets_completados_30_dias = Ticket.total_completados_ultimos_30_dias()

    context = {
        'total_clientes': total_clientes,
        'total_tickets': total_tickets,
        'tickets_en_proceso': tickets_en_proceso,
        'tickets_pendientes': tickets_pendientes,
        'tickets_sin_tecnico': tickets_sin_tecnico,
        'tickets_completados_30_dias': tickets_completados_30_dias,
    }

    return render(request, 'dashboard.html', context)