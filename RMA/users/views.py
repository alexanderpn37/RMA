from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Check if the user exists by email
        user = User.get_by_email(email)
        
        if user and user.check_password(password) and user.status == 1:
            # Set session variables
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['status'] = user.status
            request.session['role'] = user.role
            return redirect('dashboard_view')  # Redirect to the dashboard or desired page
        else:
            if user and user.status != 1:
                messages.error(request, "User is inactive.")
            else:
                messages.error(request, "Incorrect email or password.")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    if 'user_id' in request.session:
        request.session.flush()  # Remove all session data
        messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to login page

def register_view(request):
    if request.method == 'POST':
        data = {
            'email': request.POST['email'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'password': request.POST['password'],
            'password_confirmation': request.POST['password_confirmation']
        }
        
        # Validate the data before proceeding
        if not User.validate(data, request):
            return redirect('register')
        # Create a new user
        hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        
        # Create a new instance of User
        new_user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=hashed_password
        )
        new_user.save()  # Save the User object to the database
        
        messages.success(request, "User registered successfully!")
        return redirect('login')  # Redirect after creation
        
    return render(request, 'register.html')

def users_list_view(request):
    # Check if the user has an active status in the session and is an admin
    if request.session.get('status') != 1 or request.session.get('role') != 'admin':
        messages.error(request, "You don't have permission to access this page.")
        print(request.session.get('status'))
        print(request.session.get('role'))
        return redirect('login')

    users = User.get_all()  # Retrieve all users
    return render(request, 'user_list.html', {'users': users})

# View to update a user's status
def update_user_status_view(request, user_id, status):
    if request.session.get('status') != 1 or request.session.get('role') != 'admin':
        messages.error(request, "You don't have permission to change the user's status.")
        return redirect('users_list')

    user = User.get_by_id(user_id)
    user.status = status
    user.save()
    messages.success(request, "User status updated.")
    return redirect('users_list')

# View to delete a user
def delete_user_view(request, user_id):
    if request.session.get('status') != 1 or request.session.get('role') != 'admin':
        messages.error(request, "You don't have permission to delete users.")
        return redirect('users_list')

    User.delete_user(user_id)
    messages.success(request, "User successfully deleted.")
    return redirect('users_list')

# View to edit a user
def edit_user_view(request, user_id):
    if request.session.get('status') != 1 or request.session.get('role') != 'admin':
        messages.error(request, "You don't have permission to edit users.")
        return redirect('users_list')

    user = User.get_by_id(user_id)
    if request.method == 'POST':
        # Update user information
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.role = request.POST['role']
        user.save()
        messages.success(request, "User successfully updated.")
        return redirect('users_list')

    return render(request, 'edit_user.html', {'user': user})
