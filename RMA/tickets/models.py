from django.db import models
from clientes.models import Clientes
from items.models import Modelo
from users.models import User
from django.utils import timezone
from datetime import timedelta

class Ticket(models.Model):
    ESTADOS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Process', 'In Process'),
        ('Completed', 'Completed'),
    ]

    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, null=True, blank=True)
    numero_serie = models.CharField(max_length=100, null=True, blank=True)
    descripcion_problema = models.TextField(null=True, blank=True)
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'tecnico'})
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the Ticket
    def __str__(self):
        return f"Ticket #{self.id} - {self.cliente}"

    @classmethod
    # Creates a new ticket
    def create_ticket(cls, cliente):
        ticket = cls.objects.create(cliente=cliente)
        return ticket
        
    @classmethod
    # Returns the total number of tickets
    def total_tickets(cls):
        return cls.objects.count()

    @classmethod
    # Returns the total number of tickets in 'In Process' status
    def total_en_proceso(cls):
        return cls.objects.filter(estado='In Process').count()

    @classmethod
    # Returns the total number of tickets in 'Pending' status
    def total_pendientes(cls):
        return cls.objects.filter(estado='Pending').count()

    @classmethod
    # Returns the total number of tickets without an assigned technician
    def total_sin_tecnico(cls):
        return cls.objects.filter(tecnico__isnull=True).count()

    @classmethod
    # Returns the total number of tickets completed in the last 30 days
    def total_completados_ultimos_30_dias(cls):
        date_30_days_ago = timezone.now() - timedelta(days=30)
        return cls.objects.filter(
            estado='Completed',
            updated_at__gte=date_30_days_ago
        ).count()
    
    @classmethod
    # Gets the next ticket number
    def get_next_ticket(cls):
        last_ticket = cls.objects.order_by('-id').first()
        if last_ticket:
            return last_ticket.id + 1
        else:
            return 1
        
    @classmethod
    # Retrieves all tickets ordered by creation date
    def get_all(cls):
        tickets = cls.objects.all().order_by('-created_at')
        return tickets
    
    @classmethod
    # Gets the ID of the last ticket
    def get_last_ticket(cls):
        last_ticket = cls.objects.order_by('-id').first()
        return last_ticket.id
