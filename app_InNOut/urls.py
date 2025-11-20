from django.contrib import admin
from django.urls import path
from app_InNOut import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio_in_n_out, name='inicio'),

    # SUCURSALES
    path('sucursal/agregar/', views.agregar_sucursal, name='agregar_sucursal'),
    path('sucursal/ver/', views.ver_sucursales, name='ver_sucursales'),
    path('sucursal/actualizar/<int:sucursal_id>/', views.actualizar_sucursal, name='actualizar_sucursal'),
    path('sucursal/actualizar/realizar/<int:sucursal_id>/', views.realizar_actualizacion_sucursal, name='realizar_actualizacion_sucursal'),
    path('sucursal/borrar/<int:sucursal_id>/', views.borrar_sucursal, name='borrar_sucursal'),

    # TRABAJADORES
    path('trabajador/agregar/', views.agregar_trabajador, name='agregar_trabajador'),
    path('trabajador/ver/', views.ver_trabajadores, name='ver_trabajadores'),
    path('trabajador/actualizar/<int:trabajador_id>/', views.actualizar_trabajador, name='actualizar_trabajador'),
    path('trabajador/actualizar/realizar/<int:trabajador_id>/', views.realizar_actualizacion_trabajador, name='realizar_actualizacion_trabajador'),
    path('trabajador/borrar/<int:trabajador_id>/', views.borrar_trabajador, name='borrar_trabajador'),

    # PEDIDOS (INTEGRADO CON CLIENTES)
    path('pedido/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedido/ver/', views.ver_pedidos, name='ver_pedidos'),
    path('pedido/actualizar/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('pedido/actualizar/realizar/<int:pedido_id>/', views.realizar_actualizacion_pedido, name='realizar_actualizacion_pedido'),
    path('pedido/borrar/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),

    # PRODUCTOS
    path('producto/agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/ver/', views.ver_productos, name='ver_productos'),
    path('producto/actualizar/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('producto/actualizar/realizar/<int:producto_id>/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
    path('producto/borrar/<int:producto_id>/', views.borrar_producto, name='borrar_producto'),

    # PROVEEDORES
    path('proveedor/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedor/ver/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedor/actualizar/<int:proveedor_id>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedor/actualizar/realizar/<int:proveedor_id>/', views.realizar_actualizacion_proveedor, name='realizar_actualizacion_proveedor'),
    path('proveedor/borrar/<int:proveedor_id>/', views.borrar_proveedor, name='borrar_proveedor'),

    # INVENTARIO
    path('inventario/agregar/', views.agregar_inventario, name='agregar_inventario'),
    path('inventario/ver/', views.ver_inventarios, name='ver_inventarios'),
    path('inventario/actualizar/<int:inventario_id>/', views.actualizar_inventario, name='actualizar_inventario'),
    path('inventario/actualizar/realizar/<int:inventario_id>/', views.realizar_actualizacion_inventario, name='realizar_actualizacion_inventario'),
    path('inventario/borrar/<int:inventario_id>/', views.borrar_inventario, name='borrar_inventario'),

    # CLIENTES (CRUD + HISTORIAL)
    path('cliente/ver/', views.ver_clientes, name='ver_clientes'),
    path('cliente/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('cliente/actualizar/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cliente/actualizar/realizar/<int:cliente_id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('cliente/borrar/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
    # ESTA ES LA NUEVA FUNCIONALIDAD CLAVE:
    path('cliente/historial/<int:cliente_id>/', views.ver_historial_cliente, name='ver_historial_cliente'),

    # MEMBRESIAS
    path('membresia/ver/', views.ver_membresias, name='ver_membresias'),
]