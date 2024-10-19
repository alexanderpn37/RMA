from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Modelo, Marca

# View to list all models
def modelos_list_view(request):
    modelos = Modelo.get_all()
    return render(request, 'modelos_list.html', {'modelos': modelos})

# View to create a new model
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Marca, Modelo

def create_modelo_view(request, cliente_rif=None):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        marca_id = request.POST.get('marca')
        nueva_marca = request.POST.get('nueva_marca')

        # Validate that the model name is required
        if not nombre:
            messages.error(request, "The model name is required.")
            return redirect('create_modelo')

        # Validate that at least a brand is selected or a new one is provided
        if not marca_id and not nueva_marca:
            messages.error(request, "You must either select an existing brand or add a new one.")
            return redirect('create_modelo')

        # If no brand is selected, but a new one is provided, confirm it
        if not marca_id and nueva_marca:
            confirmation = request.POST.get('confirm_new_brand')
            if not confirmation:
                messages.warning(
                    request, 
                    f"Are you sure you want to add the new brand '{nueva_marca}'? Please confirm."
                )
                return render(request, 'create_modelo.html', {
                    'marcas': Marca.get_all(),
                    'nombre': nombre,
                    'nueva_marca': nueva_marca,
                    'cliente_rif': cliente_rif,  # Pass cliente_rif to the template
                })

        # If an existing brand was selected or the new one has been confirmed, proceed with model creation
        if marca_id:
            marca = Marca.get_marca_by_id(marca_id)
        else:
            # Create the new brand using the model method
            marca = Marca.create_or_get_marca(nueva_marca)

        # Create the model using the model method
        Modelo.create_modelo(nombre=nombre, marca=marca)

        messages.success(request, 'Model successfully created.')

        # Redirect based on whether cliente_rif is provided
        if cliente_rif:
            if request.method == 'POST':
                return redirect('ingresar_marca', cliente_rif=cliente_rif)
            else:
                return redirect('create_modelo_from_ticket', cliente_rif=cliente_rif)
        else:
            return redirect('modelos_list')

    # If it's a GET request, display the form
    marcas = Marca.get_all()
    return render(request, 'create_modelo.html', {
        'marcas': marcas,
        'cliente_rif': cliente_rif,  # Pass cliente_rif to the template
    })


# View to edit an existing model
def edit_modelo_view(request, modelo_id):
    try:
        modelo = Modelo.get_modelo_by_id(modelo_id)
    except Modelo.DoesNotExist:
        messages.error(request, "Model not found.")
        return redirect('modelos_list')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        marca_id = request.POST.get('marca')

        # Validate if the brand exists
        try:
            marca = Marca.get_marca_by_id(marca_id)
        except Marca.DoesNotExist:
            messages.error(request, "Brand not found.")
            return redirect('edit_modelo', modelo_id=modelo_id)

        # Update model
        modelo.nombre = nombre
        modelo.marca = marca
        modelo.clean()
        modelo.save()
        messages.success(request, "Model successfully updated.")
        return redirect('modelos_list')

    marcas = Marca.get_all()
    return render(request, 'edit_modelo.html', {'modelo': modelo, 'marcas': marcas})

# View to delete a model
def delete_modelo_view(request, modelo_id):
    try:
        modelo = Modelo.get_modelo_by_id(modelo_id)
        modelo.delete()
        messages.success(request, "Model successfully deleted.")
    except Modelo.DoesNotExist:
        messages.error(request, "Model not found.")
    
    return redirect('modelos_list')

