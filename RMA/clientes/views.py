from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Clientes
from tickets.models import Ticket
from django.core.paginator import Paginator

def clientes_list_view(request):
    if request.session.get('user_id') is None:
        return redirect('login')
    else:
        # Order clients by 'id' or another field, e.g., 'first_name'
        clientes_list = Clientes.get_all() 
        paginator = Paginator(clientes_list, 20)  # Shows 20 clients per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'clientes_list.html', {'page_obj': page_obj})

def delete_cliente_view(request, cliente_id):
    Clientes.delete_cliente(cliente_id)
    messages.success(request, "Client successfully deleted.")
    return redirect('clientes_list')

def edit_cliente_view(request, cliente_id):
    cliente = Clientes.get_cliente_by_id(id=cliente_id)

    if request.method == 'POST':
        data = {
            'rif': request.POST['rif'],
            'razon_social': request.POST['razon_social'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'telefono': request.POST['telefono'],
            'direccion': request.POST['direccion'],
        }
        Clientes.update_cliente(cliente_id, data)
        messages.success(request, "Client successfully updated.")
        return redirect('clientes_list')

    return render(request, 'edit_cliente.html', {'cliente': cliente})

def create_cliente_view(request):
    if request.method == 'POST':
        data = {
            'rif': request.POST['rif'],
            'razon_social': request.POST['razon_social'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'telefono': request.POST['telefono'],
            'direccion': request.POST['direccion']
        }

        # Custom RIF validation
        rif = data['rif']
        if not valid_rif(rif):
            messages.error(request, "The RIF must start with 'V', 'E', 'J', or 'G', followed by at least 7 digits, without special characters.")
            return render(request, 'create_cliente.html', {'data': data})

        # Attempt to create the client
        Clientes.create_cliente(data)
        messages.success(request, "Client successfully created.")
        return redirect('clientes_list')

    return render(request, 'create_cliente.html')

def create_cliente_desde_ticket_view(request):
    if request.method == 'POST':
        data = {
            'rif': request.POST['rif'],
            'razon_social': request.POST['razon_social'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'telefono': request.POST['telefono'],
            'direccion': request.POST['direccion']
        }

        # Custom RIF validation
        rif = data['rif']
        if not valid_rif(rif):
            messages.error(request, "The RIF must start with 'V', 'E', 'J', or 'G', followed by at least 7 digits, without special characters.")
            return render(request, 'create_cliente.html', {'data': data})
        # Attempt to create the client
        cliente = Clientes.create_cliente(data)
        messages.success(request, "Client successfully created.")
        # Create a ticket associated with the new client
        ticket_id = Ticket.get_next_ticket()
        return redirect('ingresar_marca', cliente_rif=rif)
    else:
        return render(request, 'create_cliente.html', {'data': {}, 'from_ticket': True})

# RIF validation function
def valid_rif(rif):
    import re
    pattern = r'^[VEJG]{1}\d{7,}$'  # Pattern: letter followed by at least 7 digits
    return re.match(pattern, rif)