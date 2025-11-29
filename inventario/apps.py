from django.apps import AppConfig

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' 
    name = 'inventario'
    verbose_name = 'Módulo de Inventario' 



INSTALLED_APPS = [
    # ...
    'inventario.apps.InventarioConfig', 
]