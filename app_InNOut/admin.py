from django.contrib import admin
from .models import Sucursal, Trabajador, Pedido, Proveedor, Producto, Inventario
@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre_tienda', 'ciudad', 'telefono_tienda', 'es_drive_thru', 'fecha_apertura')
    search_fields = ('nombre_tienda', 'ciudad')
    list_filter = ('es_drive_thru',)

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'puesto', 'sucursal', 'email')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('puesto', 'sucursal')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'total_pedido', 'tipo_orden', 'pagado', 'fecha_pedido')
    search_fields = ('numero_orden', 'tipo_orden')
    list_filter = ('pagado', 'tipo_orden')

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'contacto', 'telefono', 'email', 'tipo_proveedor', 'activo')
    search_fields = ('nombre_empresa', 'contacto', 'email')
    list_filter = ('tipo_proveedor', 'activo')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'costo', 'disponible', 'fecha_creacion')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria', 'disponible')

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'proveedor', 'cantidad', 'stock_minimo', 'ubicacion', 'lote')
    search_fields = ('producto__nombre', 'proveedor__nombre_empresa', 'lote')
    list_filter = ('ubicacion', 'unidad_medida')