from django.shortcuts import render, redirect, get_object_or_404
from clientes.models import Clientes
from items.models import Marca, Modelo
from users.models import User
from .models import Ticket
from django.contrib import messages
from users.models import User

def verificar_cliente_view(request):
    if request.method == 'POST':
        criterio = request.POST.get('criterio_busqueda')
        if criterio:
            cliente = Clientes.get_client_by_any_field(criterio)
            if cliente:
                # Client found, create ticket associated with the client
                return redirect('ingresar_marca', cliente_rif=cliente.rif)
            else:
                # Client not found, redirect to create new client
                return redirect('crear_cliente_desde_ticket')
        else:
            messages.error(request, "Please enter RIF, Email, or Phone to search for the client.")
    return render(request, 'verificar_cliente.html')

def ingresar_marca_view(request, cliente_rif):
    
    if request.method == 'POST':
        marca_id = request.POST.get('marca')
        if marca_id:
            # Save the brand in the session
            request.session['marca_id'] = marca_id
            return redirect('ingresar_equipo', cliente_rif=cliente_rif)
        else:
            messages.error(request, "Please select a brand.")
    else:
        marcas = Marca.get_all()  
    return render(request, 'ingresar_marca.html', {'marcas': marcas})


def ingresar_equipo_view(request, cliente_rif):
    
    marca_id = request.session.get('marca_id')
    if not marca_id:
        return redirect('ingresar_marca', cliente_rif=cliente_rif)
    marca = Marca.get_marca_by_id(marca_id)

    if request.method == 'POST':
        modelo_id = request.POST.get('modelo')
        numero_serie = request.POST.get('numero_serie')
        descripcion_problema = request.POST.get('descripcion_problema')

        if not modelo_id or not numero_serie or not descripcion_problema:
            messages.error(request, "All fields are required.")
            modelos = Modelo.get_modelo_by_marca(marca_id)
            return render(request, 'ingresar_equipo.html', {'marca': marca, 'modelos': modelos})

        modelo = Modelo.get_modelo_by_id(modelo_id)

        # Update the ticket with the remaining information
        ticket = Ticket(
            cliente=Clientes.get_clientes_by_rif(cliente_rif),
            modelo=modelo,
            numero_serie=numero_serie,
            descripcion_problema=descripcion_problema,
        )
        # Pending what's in gp that gives you a hint about saving a dictionary in the session
        ticket.save()

        # Clear the session
        request.session.pop('marca_id', None)
        messages.success(request, f"Ticket #{ticket.id} created successfully.")
        return redirect('detalle_ticket', ticket_id=ticket.get_last_ticket())
    modelos = Modelo.get_modelo_by_marca(marca=marca)
    return render(request, 'ingresar_equipo.html', {'marca': marca, 'modelos': modelos})

def detalle_ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'detalle_ticket.html', {'ticket': ticket})

def asignar_tecnico_view(request, ticket_id):
    # Verify if the user is authenticated
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Verify if the user has permission to access this view
    user_role = request.session.get('role')
    user_status = request.session.get('status')
    if user_role not in ['admin', 'tecnico'] or user_status != 1:
        return redirect('no_permission')

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        tecnico_id = request.POST.get('tecnico')
        estado = request.POST.get('estado')

        if tecnico_id:
            tecnico = User.get_user_by_id(tecnico_id)
            ticket.tecnico = tecnico
        if estado:
            ticket.estado = estado

        ticket.save()
        messages.success(request, "Ticket updated successfully.")
        return redirect('detalle_ticket', ticket_id=ticket.id)
    else:
        tecnicos = User.get_techs()
        estados = ['Pending', 'In Process', 'Completed']
    return render(request, 'asignar_tecnico.html', {'ticket': ticket, 'tecnicos': tecnicos, 'estados': estados})


def tickets_list_view(request):
    # Verify if the user is authenticated
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Get the user and pass it to the context
    user = User.get_by_id(id=user_id)

    tickets = Ticket.get_all()
    return render(request, 'tickets_list.html', {'tickets': tickets, 'user': user})
