from django.urls import path
from . import views

urlpatterns = [
    # Esta es la URL que manejará el inicio de sesión
    path('login/', views.login_view, name='login'),
    
    # URL para cerrar sesión
    path('logout/', views.logout_view, name='logout'),
]