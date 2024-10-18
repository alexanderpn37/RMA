from django.db import models
from django.contrib import messages

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    @classmethod
    def create_or_get_marca(cls, nueva_marca):
        """Creates a new brand or gets it if it already exists"""
        marca, created = cls.objects.get_or_create(nombre=nueva_marca)
        return marca

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_marca_by_id(cls, marca_id):
        return cls.objects.get(id=marca_id)

class Modelo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.marca.nombre} {self.nombre}'

    def clean(self):
        """Validate that the model has a name and is related to a brand."""
        if not self.nombre:
            messages.error(request, 'The model name is required.')
        if not self.marca:
            messages.error(request, 'The model must be related to a brand.')

    @classmethod
    def create_modelo(cls, nombre, marca):
        """Creates a new model and validates the existence of the brand"""
        modelo = cls(nombre=nombre, marca=marca)
        modelo.clean()
        modelo.save()
        return modelo

    @classmethod
    def get_modelo_by_marca(cls, marca):
        return cls.objects.filter(marca=marca)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_modelo_by_id(cls, modelo_id):
        return cls.objects.get(id=modelo_id)