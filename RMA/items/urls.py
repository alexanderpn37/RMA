# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.modelos_list_view, name='modelos_list'),
    path('edit/<int:modelo_id>/', views.edit_modelo_view, name='edit_modelo'),
    path('delete/<int:modelo_id>/', views.delete_modelo_view, name='delete_modelo'),
    path('crear/', views.create_modelo_view, name='create_modelo'),
]
