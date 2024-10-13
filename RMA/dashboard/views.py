from django.shortcuts import render, redirect
from django.contrib import messages

def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        # El usuario no está autenticado
        messages.error(request, "Must be loged in.")
        return redirect('login')
    else:
        # El usuario está autenticado
        # Aquí puedes agregar la lógica adicional que necesites
        return render(request, 'dashboard.html')
