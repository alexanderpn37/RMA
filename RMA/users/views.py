from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Verificar si el usuario existe por el email
        user = User.get_by_email(email)
        print(user)
        if user and user.check_password(password):
            
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect('dashboard_view')# Redirige al dashboard o a la página deseada
        else:
            messages.error(request, "Email o contraseña incorrectos")
            return redirect('login')

    return render(request, 'login.html')
def logout_view(request):
    if 'user_id' in request.session:
        request.session.flush()  # Elimina toda la información de la sesión
        messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')  # Redirige a la página de login

def register_view(request):
    if request.method == 'POST':
        data = {
            'email': request.POST['email'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'password': request.POST['password'],
            'password_confirmation': request.POST['password_confirmation']
        }
        
        # Validar datos antes de proceder
        if not User.validate(data, request):
            return redirect('register')
        
        # Crear un nuevo usuario
        hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        
        # Crear instancia de User
        new_user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=hashed_password
        )
        new_user.save()  # Guarda el objeto de User en la base de datos
        
        messages.success(request, "User registered successfully!")
        return redirect('login')  # Redirigir después de la creación
        
    return render(request, 'register.html')