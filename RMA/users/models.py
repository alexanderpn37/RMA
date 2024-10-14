import bcrypt
from django.contrib import messages
from django.db import models
from datetime import datetime
import re


class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=100, default="admin")
    created_at = models.DateTimeField(auto_now_add=True)  # Establece la fecha al crear el registro
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1) #status , 1 is for active, 0 for inactive and 2 is for pending users



    # Método para verificar la contraseña durante el login
    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    @classmethod
    def create_user(cls, data):
        # Verifica si el email ya existe en la base de datos
        existing_user = cls.get_by_email(data['email'])
        if existing_user:
            print("Email already exists.")
            return None  # Devuelve None o podrías lanzar una excepción

        # Si el email no existe, procede a crear el nuevo usuario
        hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        newuser = cls.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_pw
        )
        print(newuser.id)
        return newuser.id2
    
    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def get_all(cls):
        return cls.objects.all()
    
    @classmethod
    def update_password(cls, user_id, new_password):
        # Encrypt new password
        hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        user = cls.objects.get(id=user_id)
        user.password = hashed_pw
        user.updated_at = datetime.now()
        user.save()
    
    @classmethod
    def delete_user(cls, user_id):
        user = cls.objects.get(id=user_id)
        user.delete()
        return True
    
    @classmethod
    def get_by_email(cls, email):
        return cls.objects.filter(email=email).first()
    
    @classmethod
    def validate(cls, data, request):
        # Valida que el email tenga un formato válido
        if not cls.validate_email(data['email']):
            messages.error(request, "Invalid email format.")
            return False
        if data['password'] != data['password_confirmation']:
            messages.error(request, "Password do not match")
            return False
        return True
    @classmethod
    def validate_email(cls, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    
    

