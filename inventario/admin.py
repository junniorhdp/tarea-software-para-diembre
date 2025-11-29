from django.contrib import admin
from .models import Producto, Venta, Categoria # Importar Categoria
from django.utils.html import format_html 

print(">>> ADMIN INVENTARIO CARGADO")

# -----------------------------------------------------------------
# NUEVO ADMIN PARA EL MODELO CATEGORIA
# -----------------------------------------------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# -----------------------------------------------------------------
# Admin para el modelo Producto (Actualizado)
# -----------------------------------------------------------------
class ProductoAdmin(admin.ModelAdmin):
    # CAMBIO: 'tipo' por 'categoria'
    list_display = ('nombre', 'categoria', 'variacion', 'stock', 'precio', 'imagen_preview')
    
    # CAMBIO: 'tipo' por 'categoria'
    fields = (
        'nombre', 
        'categoria', # Usar la nueva clave foránea
        'precio', 
        'stock', 
        'variacion', 
        'imagen', 
        'imagen_preview'
    )
    
    # Filtrar productos por Categoría
    list_filter = ('categoria',)
    search_fields = ('nombre', 'variacion', 'categoria__nombre')
    
    readonly_fields = ('imagen_preview',)

    # Método para mostrar la vista previa de la imagen
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 150px; border-radius: 8px;" />', obj.imagen.url)
        return "No hay imagen subida"
    
    imagen_preview.short_description = 'Vista Previa'

# -----------------------------------------------------------------
# Admin para el modelo Venta (Actualizado)
# -----------------------------------------------------------------
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'precio_unitario', 'total_venta', 'fecha_venta')
    # CAMBIO: 'producto__tipo' por 'producto__categoria'
    list_filter = ('fecha_venta', 'producto__categoria')
    search_fields = ('producto__nombre',)
    ordering = ('-fecha_venta',)

# -----------------------------------------------------------------
# Registro de Modelos - Se mantiene el patrón de registro
# -----------------------------------------------------------------
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentaAdmin)