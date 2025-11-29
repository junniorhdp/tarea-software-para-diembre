from django import forms
# CRÍTICO: Importamos Categoria para su formulario
from .models import Producto, Venta, Categoria 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import get_user_model

User = get_user_model() 

# -----------------------------------------------------------------
# 1. FORMULARIO PARA PRODUCTOS
# -----------------------------------------------------------------
class ProductoForm(forms.ModelForm):
    """Formulario para la creación y edición de Productos."""
    
    class Meta:
        model = Producto
        # El campo 'categoria' es ahora la clave foránea a Categoria
        fields = ['imagen', 'nombre', 'categoria', 'precio', 'stock', 'variacion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'accept': 'image/*'})
        }

# -----------------------------------------------------------------
# 2. FORMULARIO PARA CATEGORÍAS (NUEVO)
# -----------------------------------------------------------------
class CategoriaForm(forms.ModelForm):
    """Formulario para la creación y edición de Categorías."""
    
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}) # Mejora visual para el campo de descripción
        }

# -----------------------------------------------------------------
# 3. FORMULARIO PARA REGISTRAR VENTAS
# -----------------------------------------------------------------
class VentaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(stock__gt=0).order_by('nombre'), # Filtramos solo productos con stock
        label="Seleccionar Producto" 
    )
    
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']

# -----------------------------------------------------------------
# 4. FORMULARIO PARA REGISTRO DE USUARIOS
# -----------------------------------------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')