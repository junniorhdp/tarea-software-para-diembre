from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, DecimalField, F
from django.contrib import messages
from django import forms 
from .models import Producto, Venta, Categoria # Importa todos los modelos necesarios
from .forms import CustomUserCreationForm, ProductoForm, VentaForm # Asegúrate de que estos forms existan
from datetime import date 
import datetime # Se usa para datetime.date.today()

# -----------------------------------------------------------------
# --- Definición de Formularios Auxiliares ---
# Si CategoriaForm no está en .forms, lo definimos aquí temporalmente para que las vistas funcionen
# Si ya lo tienes en .forms, puedes eliminar este bloque.
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
# -----------------------------------------------------------------


# =======================================================
# --- VISTAS PÚBLICAS Y DE AUTENTICACIÓN ---
# =======================================================

def pagina_compra_view(request):
    """ Muestra el catálogo de productos disponibles para los compradores (público). """
    productos_disponibles = Producto.objects.filter(stock__gt=0).order_by('nombre')
    context = {'productos': productos_disponibles}
    return render(request, 'inventario/pagina_compra.html', context)

def register_view(request):
    """ Vista de Registro de Usuario. """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado con éxito. ¡Ya puedes iniciar sesión!")
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form, 'title': 'Registro de Usuario'}
    return render(request, 'inventario/register.html', context)


# =======================================================
# --- VISTAS PROTEGIDAS (DASHBOARD y PRODUCTOS) ---
# =======================================================

@login_required
def dashboard_view(request):
    """
    Vista principal del Dashboard con KPIs.
    CRÍTICO: REDIRECCIÓN a 'pagina_compra' si el usuario NO es staff.
    """
    if not request.user.is_staff:
        return redirect('pagina_compra')
    
    # --- 1. Datos de Productos ---
    productos = Producto.objects.all().order_by('nombre')
    
    # --- 2. Alerta de Stock Bajo (CRÍTICO: QuerySet para ser iterable) ---
    # ESTO ES LO QUE ARREGLA EL TypeError 'int' object is not iterable
    alerta_stock_bajo = Producto.objects.filter(stock__lt=50).order_by('stock')
    
    # --- 3. KPIs y Métricas ---
    productos_totales = productos.count()
    categorias_totales = Categoria.objects.count()
    
    # Cálculo robusto del total de ventas monetario de hoy
    try:
        ventas_hoy_qs = Venta.objects.filter(fecha_venta=date.today()).aggregate(
            total_sum=Sum(F('cantidad') * F('precio_unitario'), output_field=DecimalField())
        )
        total_ventas_hoy = ventas_hoy_qs['total_sum'] if ventas_hoy_qs['total_sum'] is not None else 0
        transacciones_hoy = Venta.objects.filter(fecha_venta=date.today()).count()
    except Exception as e:
        print(f"Error al calcular ventas del día: {e}")
        total_ventas_hoy = 0
        transacciones_hoy = 0
    
    context = {
        'productos': productos,
        'alerta_stock_bajo': alerta_stock_bajo,  # QuerySet de productos (iterable)
        'productos_totales': productos_totales,
        'categorias_totales': categorias_totales,
        'total_ventas_hoy': total_ventas_hoy,  # Valor monetario
        'transacciones_hoy': transacciones_hoy, # Cantidad de ventas
    }
    return render(request, 'inventario/dashboard.html', context)

@login_required
def producto_crear_view(request, pk=None):
    """ Vista para Crear y Editar Productos - Protegida """
    if not request.user.is_staff:
        return redirect('pagina_compra')

    producto = get_object_or_404(Producto, pk=pk) if pk else None
        
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto) 
        if form.is_valid():
            form.save()
            messages.success(request, "Producto guardado correctamente.")
            return redirect('dashboard')
    else:
        form = ProductoForm(instance=producto) 
        
    context = {
        'form': form,
        'producto': producto,
        'title': 'Editar Producto' if pk else 'Añadir Nuevo Producto'
    }
    return render(request, 'inventario/producto_form.html', context)

@login_required
def producto_eliminar_view(request, pk):
    """ Vista para Eliminar Productos - Protegida """
    if not request.user.is_staff:
        return redirect('pagina_compra')
        
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('dashboard')
    return render(request, 'inventario/producto_confirm_delete.html', {'producto': producto})

@login_required
def registrar_venta_view(request):
    """ Vista para el registro manual de ventas - Protegida """
    if not request.user.is_staff:
        return redirect('pagina_compra')
        
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            producto_vendido = venta.producto
            cantidad_vendida = venta.cantidad
            
            if cantidad_vendida > producto_vendido.stock:
                messages.error(request, 
                              f"Error: Stock insuficiente para {producto_vendido.nombre} ({producto_vendido.variacion}). Stock actual: {producto_vendido.stock}.")
                return redirect('registrar_venta')
                
            venta.precio_unitario = producto_vendido.precio 
            venta.save()
            producto_vendido.stock -= cantidad_vendida
            producto_vendido.save()
            
            messages.success(request, f"Venta registrada con éxito. Se descontaron {cantidad_vendida} unidades de {producto_vendido.nombre}.")
            return redirect('dashboard')
    else:
        form = VentaForm()
        
    context = {'form': form}
    return render(request, 'inventario/registrar_venta.html', context)

@login_required
def venta_rapida_view(request, pk):
    """
    Vista para registrar una venta de 1 unidad directamente desde el catálogo.
    Protegida, pero accesible por el botón "Comprar" del catálogo (si el usuario es staff).
    """
    if not request.user.is_staff:
        messages.error(request, "Acceso denegado. Solo personal autorizado puede registrar ventas.")
        return redirect('pagina_compra')

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        cantidad_vendida = 1
        
        if producto.stock >= cantidad_vendida:
            # 1. Crear el registro de venta
            Venta.objects.create(
                producto=producto,
                cantidad=cantidad_vendida,
                precio_unitario=producto.precio,
                fecha_venta=date.today()
            )
            
            # 2. Descontar el stock
            producto.stock -= cantidad_vendida
            producto.save()
            
            messages.success(request, f"Venta rápida de 1 unidad de '{producto.nombre}' registrada. Stock restante: {producto.stock}.")
        else:
            messages.error(request, f"Error: '{producto.nombre}' está agotado o tiene stock insuficiente.")
            
    # Redirige a la página del catálogo después de la acción
    return redirect('pagina_compra')

# =======================================================
# --- VISTAS DE CATEGORÍA ---
# =======================================================

@login_required
def categoria_list_view(request):
    """ Muestra la lista de categorías. """
    if not request.user.is_staff:
        return redirect('pagina_compra')
    
    categorias = Categoria.objects.all().order_by('nombre')
    context = {'categorias': categorias}
    return render(request, 'inventario/categoria_list.html', context)

@login_required
def categoria_crear_view(request, pk=None):
    """ Vista para Crear (pk=None) y Editar (con pk) Categorías. """
    if not request.user.is_staff:
        return redirect('pagina_compra')

    categoria = get_object_or_404(Categoria, pk=pk) if pk else None
    
    # Usamos el CategoriaForm definido al inicio
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria) 
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría guardada correctamente.")
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria) 
        
    context = {
        'form': form,
        'categoria': categoria,
        'title': 'Editar Categoría' if pk else 'Añadir Nueva Categoría'
    }
    return render(request, 'inventario/categoria_form.html', context)

@login_required
def categoria_eliminar_view(request, pk):
    """ Vista para Eliminar Categorías. """
    if not request.user.is_staff:
        return redirect('pagina_compra')
        
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre_cat = categoria.nombre
        categoria.delete()
        messages.warning(request, f"Categoría '{nombre_cat}' eliminada. Los productos asociados quedaron sin clase.")
        return redirect('categoria_list')
        
    return render(request, 'inventario/categoria_confirm_delete.html', {'categoria': categoria})

@login_required
def reporte_ventas_view(request):
    """ Vista de Reporte de Ventas. """
    if not request.user.is_staff:
        return redirect('pagina_compra')
        
    ventas = Venta.objects.all().order_by('-fecha_venta')
    
    # Cálculo del total vendido (eficiente)
    total_vendido = Venta.objects.aggregate(
        total_sum=Sum(F('cantidad') * F('precio_unitario'), output_field=DecimalField())
    )['total_sum'] or 0

    ventas_agrupadas = Venta.objects.values(
        'producto__nombre', 
        'producto__variacion'
    ).annotate(
        total_cantidad_vendida=Sum('cantidad')
    ).order_by('-total_cantidad_vendida')
    
    context = {
        'ventas': ventas,
        'total_general_vendido': total_vendido,
        'ventas_agrupadas': ventas_agrupadas,
        'cantidad_transacciones': ventas.count()
    }
    return render(request, 'inventario/reporte_ventas.html', context)