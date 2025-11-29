from django.db import models
from django.contrib.auth.models import User 

# Función para definir la ruta de subida de imágenes
def producto_imagen_path(instance, filename):
    # Usa el nombre del producto como parte de la ruta si el ID no está disponible
    return f'productos/{instance.nombre.replace(" ", "_")}/{filename}'


# --- NUEVO: Modelo para Categorías/Clases de Productos ---
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría de Producto"
        # ¡CORRECCIÓN CLAVE! Atributo correcto
        verbose_name_plural = "Categorías de Productos" 
        
    def __str__(self):
        return self.nombre


# --- Modelo Producto Actualizado ---
class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    
    # CRÍTICO: Clave foránea a Categoria
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Clase / Categoría",
        related_name='productos' 
    )
    
    variacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Variación (ej. Tamaño o Tipo)") 
    
    precio = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio Unitario")
    stock = models.IntegerField(default=0, verbose_name="Stock Disponible")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    imagen = models.ImageField(upload_to=producto_imagen_path, blank=True, null=True, verbose_name="Imagen del Producto")

    class Meta:
        verbose_name = "Producto"
        # ¡CORRECCIÓN CLAVE! Atributo correcto
        verbose_name_plural = "Productos"

    def __str__(self):
        # Muestra el nombre de la categoría o 'Sin Clase' si es nula
        return f"{self.nombre} ({self.categoria.nombre if self.categoria else 'Sin Clase'}) - Stock: {self.stock}"

# --- Modelo Venta (Mantenido) ---
class Venta(models.Model):
    # Usamos CASCADE ya que una venta sin producto no tiene sentido
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto Vendido")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio Unitario de Venta")
    fecha_venta = models.DateField(auto_now_add=True, verbose_name="Fecha de Venta")

    class Meta:
        verbose_name = "Venta"
        # ¡CORRECCIÓN CLAVE! Atributo correcto
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Venta de {self.cantidad}x {self.producto.nombre}"
    
    @property
    def total_venta(self):
        return self.cantidad * self.precio_unitario