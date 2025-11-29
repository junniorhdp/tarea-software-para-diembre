from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# 1. Función para el Login
def login_view(request):
    # Si el usuario ya está autenticado, lo enviamos al Dashboard
    if request.user.is_authenticated:
        return redirect('dashboard') 

    if request.method == 'POST':
        # Procesar el formulario enviado
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # El formulario de autenticación ya maneja el username/password internamente
            user = form.get_user() 
            if user is not None:
                login(request, user)
                return redirect('dashboard') # ÉXITO: Va al Dashboard
    else:
        # Mostrar el formulario si es la primera vez que se visita la página
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})

# 2. Función para el Logout
def logout_view(request):
    logout(request)
    # Después de cerrar sesión, volvemos a la página de login
    return redirect('login')