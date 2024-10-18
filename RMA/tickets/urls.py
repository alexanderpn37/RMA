# tickets/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.tickets_list_view, name='tickets_list'),
    path('verificar-cliente/', views.verificar_cliente_view, name='verificar_cliente'),
    path('ingresar-marca/<str:cliente_rif>/', views.ingresar_marca_view, name='ingresar_marca'),
    path('ingresar-equipo/<str:cliente_rif>/', views.ingresar_equipo_view, name='ingresar_equipo'),
    path('detalle-ticket/<int:ticket_id>/', views.detalle_ticket_view, name='detalle_ticket'),
    path('asignar-tecnico/<int:ticket_id>/', views.asignar_tecnico_view, name='asignar_tecnico'),
]
