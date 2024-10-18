from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.users_list_view, name='users_list'),
    path('edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('update_status/<int:user_id>/<int:status>/', views.update_user_status_view, name='update_user_status'),
    path('no-permission/', views.no_permission_view, name='no_permission'),
]