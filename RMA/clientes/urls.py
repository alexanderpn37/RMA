from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes_list_view, name='clientes_list'),
    path('crear/', views.create_cliente_view, name='create_cliente'),
    path('crear-desde-ticket/', views.create_cliente_desde_ticket_view, name='crear_cliente_desde_ticket'),
    path('delete/<int:cliente_id>/', views.delete_cliente_view, name='delete_cliente'),
    path('edit/<int:cliente_id>/', views.edit_cliente_view, name='edit_cliente'),
]
