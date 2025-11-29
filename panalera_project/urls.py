from django.contrib import admin
from django.urls import path, include 
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# Las importaciones necesarias están aquí arriba. No se necesita importar nada más.

urlpatterns = [
    # Redirecciona la raíz (/) a la URL del Login
    path('', RedirectView.as_view(url='login/', permanent=True)), 

    # Rutas de autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Ruta principal del Admin
    path('admin/', admin.site.urls),
    
    # Incluye las URLs de tus aplicaciones
    path('', include('usuarios.urls')), 
    path('', include('inventario.urls')), 
]

# CÓDIGO CRÍTICO para servir archivos media (imágenes) en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)