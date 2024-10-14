from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Clientes
from django.contrib import messages

def clientes_list_view(request):
    clientes_list = Clientes.get_all()
    paginator = Paginator(clientes_list, 20)  # Muestra 20 clientes por página
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'clientes_list.html', {'page_obj': page_obj})

def delete_cliente_view(request, cliente_id):
    Clientes.delete_cliente(cliente_id)
    messages.success(request, "Cliente eliminado exitosamente.")
    return redirect('clientes_list')

def edit_cliente_view(request, cliente_id):
    cliente = Clientes.objects.get(id=cliente_id)

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
        messages.success(request, "Cliente actualizado exitosamente.")
        return redirect('clientes_list')

    return render(request, 'edit_cliente.html', {'cliente': cliente})
