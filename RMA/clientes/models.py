
from django.db.models import Q
from django.db import models

class Clientes(models.Model):
    rif = models.CharField(max_length=50)
    razon_social = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_clientes_by_rif(cls, rif):
        return cls.objects.filter(rif=rif).first()
    
    @classmethod
    def get_clientes_by_email(cls, email):
        return cls.objects.filter(email=email)

    @classmethod
    def get_all(cls):
        return cls.objects.all().order_by('-updated_at') 

    @classmethod 
    def delete_cliente(cls, clientes_id):
        cliente = cls.objects.get(id=clientes_id)
        cliente.delete()
        return True

    @classmethod
    def update_cliente(cls, clientes_id, data):
        cliente = cls.objects.get(id=clientes_id)
        cliente.rif = data['rif']
        cliente.razon_social = data['razon_social']
        cliente.first_name = data['first_name']
        cliente.last_name = data['last_name']
        cliente.email = data['email']
        cliente.telefono = data['telefono']
        cliente.direccion = data['direccion']
        cliente.save()
        return True

    @classmethod
    def create_cliente(cls, data):
        cliente = cls(
            rif=data['rif'],
            razon_social=data['razon_social'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            telefono=data['telefono'],
            direccion=data['direccion']
        )
        cliente.save()
        return cliente
    @classmethod
    def total_clientes(cls):
        return cls.objects.count()
    
    @classmethod
    def get_client_by_any_field(cls, criterio):
        return Clientes.objects.filter(
                Q(rif=criterio) | Q(email=criterio) | Q(telefono=criterio)
            ).first()
    
    @classmethod
    def get_cliente_by_id(cls, id):
        return cls.objects.get(id=id)