from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    # --------------------------------------------------------
    # VISTAS DE AUTENTICACIÓN
    # --------------------------------------------------------
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    
    # --------------------------------------------------------
    # VISTAS PÚBLICAS (ACCESO DE COMPRADORES)
    # --------------------------------------------------------
    path('compra/', views.pagina_compra_view, name='pagina_compra'),
    
    # NUEVA RUTA: Venta Rápida
    path('venta/rapida/<int:pk>/', views.venta_rapida_view, name='venta_rapida'),

    # --------------------------------------------------------
    # VISTAS PROTEGIDAS (ACCESO DE ADMINISTRADORES/STAFF)
    # --------------------------------------------------------
    
    # 1. DASHBOARD y REPORTES
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('reporte/ventas/', views.reporte_ventas_view, name='reporte_ventas'),
    path('venta/registrar/', views.registrar_venta_view, name='registrar_venta'),

    # 2. CRUD DE PRODUCTOS
    path('producto/nuevo/', views.producto_crear_view, name='producto_crear'), 
    path('producto/editar/<int:pk>/', views.producto_crear_view, name='producto_editar'), 
    path('producto/eliminar/<int:pk>/', views.producto_eliminar_view, name='producto_eliminar'),

    # 3. CRUD DE CATEGORÍAS
    path('categorias/', views.categoria_list_view, name='categoria_list'), 
    path('categoria/nuevo/', views.categoria_crear_view, name='categoria_crear'), 
    path('categoria/editar/<int:pk>/', views.categoria_crear_view, name='categoria_editar'), 
    path('categoria/eliminar/<int:pk>/', views.categoria_eliminar_view, name='categoria_eliminar'),
]