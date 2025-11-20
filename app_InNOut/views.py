from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal, Trabajador, Pedido, Proveedor, Producto, Inventario, Cliente, Membresia
from django.db.models import Sum

# ==========================================
# INICIO
# ==========================================
def inicio_in_n_out(request):
    return render(request, 'inicio.html', {
        'total_sucursales': Sucursal.objects.count(),
        'total_trabajadores': Trabajador.objects.count(),
        'total_pedidos': Pedido.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_proveedores': Proveedor.objects.count(),
        'total_inventarios': Inventario.objects.count(),
        'total_clientes': Cliente.objects.count(),
        'sucursales': Sucursal.objects.all().order_by('-fecha_apertura')[:5],
        'trabajadores': Trabajador.objects.all().order_by('-fecha_contratacion')[:5]
    })

# ==========================================
# SUCURSALES
# ==========================================
def agregar_sucursal(request):
    if request.method == 'POST':
        Sucursal.objects.create(
            nombre_tienda=request.POST.get('nombre_tienda'), ciudad=request.POST.get('ciudad'),
            codigo_postal=request.POST.get('codigo_postal'), telefono_tienda=request.POST.get('telefono_tienda'),
            direccion=request.POST.get('direccion'), es_drive_thru=request.POST.get('es_drive_thru') == 'on',
            fecha_apertura=request.POST.get('fecha_apertura')
        )
        return redirect('ver_sucursales')
    return render(request, 'sucursal/agregar_sucursal.html')

def ver_sucursales(request):
    return render(request, 'sucursal/ver_sucursales.html', {'sucursales': Sucursal.objects.all().order_by('nombre_tienda')})

def actualizar_sucursal(request, sucursal_id):
    return render(request, 'sucursal/actualizar_sucursal.html', {'sucursal': get_object_or_404(Sucursal, id=sucursal_id)})

def realizar_actualizacion_sucursal(request, sucursal_id):
    s = get_object_or_404(Sucursal, id=sucursal_id)
    if request.method == 'POST':
        s.nombre_tienda = request.POST.get('nombre_tienda')
        s.direccion, s.ciudad = request.POST.get('direccion'), request.POST.get('ciudad')
        s.codigo_postal, s.telefono_tienda = request.POST.get('codigo_postal'), request.POST.get('telefono_tienda')
        s.es_drive_thru = request.POST.get('es_drive_thru') == 'on'
        s.fecha_apertura = request.POST.get('fecha_apertura')
        s.save()
    return redirect('ver_sucursales')

def borrar_sucursal(request, sucursal_id):
    s = get_object_or_404(Sucursal, id=sucursal_id)
    if request.method == 'POST': s.delete(); return redirect('ver_sucursales')
    return render(request, 'sucursal/borrar_sucursal.html', {'sucursal': s})

# ==========================================
# TRABAJADORES
# ==========================================
def agregar_trabajador(request):
    if request.method == 'POST':
        Trabajador.objects.create(
            nombre=request.POST.get('nombre'), apellido=request.POST.get('apellido'),
            puesto=request.POST.get('puesto'), fecha_contratacion=request.POST.get('fecha_contratacion'),
            email=request.POST.get('email'), telefono_personal=request.POST.get('telefono_personal'),
            sucursal=get_object_or_404(Sucursal, id=request.POST.get('sucursal')) if request.POST.get('sucursal') else None
        )
        return redirect('ver_trabajadores')
    return render(request, 'trabajador/agregar_trabajador.html', {'sucursales': Sucursal.objects.all()})

def ver_trabajadores(request):
    return render(request, 'trabajador/ver_trabajadores.html', {'trabajadores': Trabajador.objects.select_related('sucursal').all()})

def actualizar_trabajador(request, trabajador_id):
    return render(request, 'trabajador/actualizar_trabajador.html', {'trabajador': get_object_or_404(Trabajador, id=trabajador_id), 'sucursales': Sucursal.objects.all()})

def realizar_actualizacion_trabajador(request, trabajador_id):
    t = get_object_or_404(Trabajador, id=trabajador_id)
    if request.method == 'POST':
        t.nombre, t.apellido = request.POST.get('nombre'), request.POST.get('apellido')
        t.puesto, t.fecha_contratacion = request.POST.get('puesto'), request.POST.get('fecha_contratacion')
        t.email, t.telefono_personal = request.POST.get('email'), request.POST.get('telefono_personal')
        if request.POST.get('sucursal'): t.sucursal = get_object_or_404(Sucursal, id=request.POST.get('sucursal'))
        t.save()
    return redirect('ver_trabajadores')

def borrar_trabajador(request, trabajador_id):
    t = get_object_or_404(Trabajador, id=trabajador_id)
    if request.method == 'POST': t.delete(); return redirect('ver_trabajadores')
    return render(request, 'trabajador/borrar_trabajador.html', {'trabajador': t})

# ==========================================
# PEDIDOS (¡FUNCIONALIDAD UNIDA CON CLIENTES!)
# ==========================================
def agregar_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        trabajador_id = request.POST.get('trabajador')
        
        Pedido.objects.create(
            numero_orden=request.POST.get('numero_orden'),
            total_pedido=request.POST.get('total_pedido') or 0,
            tipo_orden=request.POST.get('tipo_orden'),
            nombre_cliente_temporal=request.POST.get('nombre_cliente_temporal'),
            pagado=request.POST.get('pagado') == 'on',
            trabajador=get_object_or_404(Trabajador, id=trabajador_id) if trabajador_id else None,
            cliente=get_object_or_404(Cliente, id=cliente_id) if cliente_id else None
        )
        return redirect('ver_pedidos')
    return render(request, 'pedido/agregar_pedido.html', {'trabajadores': Trabajador.objects.all(), 'clientes': Cliente.objects.all().order_by('nombre')})

def ver_pedidos(request):
    return render(request, 'pedido/ver_pedidos.html', {'pedidos': Pedido.objects.select_related('trabajador', 'cliente').all().order_by('-fecha_pedido')})

def actualizar_pedido(request, pedido_id):
    return render(request, 'pedido/actualizar_pedido.html', {
        'pedido': get_object_or_404(Pedido, id=pedido_id),
        'trabajadores': Trabajador.objects.all(),
        'clientes': Cliente.objects.all()
    })

def realizar_actualizacion_pedido(request, pedido_id):
    p = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        p.numero_orden = request.POST.get('numero_orden')
        p.total_pedido = request.POST.get('total_pedido') or 0
        p.tipo_orden = request.POST.get('tipo_orden')
        p.nombre_cliente_temporal = request.POST.get('nombre_cliente_temporal')
        p.pagado = request.POST.get('pagado') == 'on'
        if request.POST.get('trabajador'): p.trabajador = get_object_or_404(Trabajador, id=request.POST.get('trabajador'))
        if request.POST.get('cliente'): 
            p.cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))
        else:
            p.cliente = None
        p.save()
    return redirect('ver_pedidos')

def borrar_pedido(request, pedido_id):
    p = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST': p.delete(); return redirect('ver_pedidos')
    return render(request, 'pedido/borrar_pedido.html', {'pedido': p})

# ==========================================
# CLIENTES (CON HISTORIAL DE COMPRAS)
# ==========================================
def agregar_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST.get('nombre'), apellido=request.POST.get('apellido'),
            telefono=request.POST.get('telefono'), email=request.POST.get('email')
        )
        return redirect('ver_clientes')
    return render(request, 'cliente/agregar_cliente.html')

def ver_clientes(request):
    return render(request, 'cliente/ver_clientes.html', {'clientes': Cliente.objects.all().order_by('nombre')})

def actualizar_cliente(request, cliente_id):
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': get_object_or_404(Cliente, id=cliente_id)})

def realizar_actualizacion_cliente(request, cliente_id):
    c = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        c.nombre, c.apellido = request.POST.get('nombre'), request.POST.get('apellido')
        c.telefono, c.email = request.POST.get('telefono'), request.POST.get('email')
        c.save()
    return redirect('ver_clientes')

def borrar_cliente(request, cliente_id):
    c = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST': c.delete(); return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': c})

# --- VISTA NUEVA: HISTORIAL DE CLIENTE ---
def ver_historial_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # Traemos todos los pedidos de este cliente
    pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha_pedido')
    # Calculamos el total gastado
    total_gastado = pedidos.aggregate(Sum('total_pedido'))['total_pedido__sum'] or 0
    
    return render(request, 'cliente/historial_cliente.html', {
        'cliente': cliente,
        'pedidos': pedidos,
        'total_gastado': total_gastado
    })

# ==========================================
# RESTO DE VISTAS (Productos, Proveedores, Inventario, Membresias)
# ==========================================
def agregar_producto(request):
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST.get('nombre'), descripcion=request.POST.get('descripcion'),
            categoria=request.POST.get('categoria'), precio=request.POST.get('precio'), costo=request.POST.get('costo'),
            disponible=request.POST.get('disponible') == 'on', imagen=request.POST.get('imagen')
        )
        return redirect('ver_productos')
    return render(request, 'producto/agregar_producto.html')

def ver_productos(request):
    return render(request, 'producto/ver_productos.html', {'productos': Producto.objects.all().order_by('categoria')})

def actualizar_producto(request, producto_id):
    return render(request, 'producto/actualizar_producto.html', {'producto': get_object_or_404(Producto, id=producto_id)})

def realizar_actualizacion_producto(request, producto_id):
    p = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        p.nombre, p.descripcion = request.POST.get('nombre'), request.POST.get('descripcion')
        p.categoria, p.precio, p.costo = request.POST.get('categoria'), request.POST.get('precio'), request.POST.get('costo')
        p.disponible = request.POST.get('disponible') == 'on'
        p.imagen = request.POST.get('imagen')
        p.save()
    return redirect('ver_productos')

def borrar_producto(request, producto_id):
    p = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST': p.delete(); return redirect('ver_productos')
    return render(request, 'producto/borrar_producto.html', {'producto': p})

def agregar_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre_empresa=request.POST.get('nombre_empresa'), contacto=request.POST.get('contacto'),
            telefono=request.POST.get('telefono'), email=request.POST.get('email'), direccion=request.POST.get('direccion'),
            tipo_proveedor=request.POST.get('tipo_proveedor'), activo=request.POST.get('activo') == 'on'
        )
        return redirect('ver_proveedores')
    return render(request, 'proveedor/agregar_proveedor.html')

def ver_proveedores(request):
    return render(request, 'proveedor/ver_proveedores.html', {'proveedores': Proveedor.objects.all().order_by('nombre_empresa')})

def actualizar_proveedor(request, proveedor_id):
    return render(request, 'proveedor/actualizar_proveedor.html', {'proveedor': get_object_or_404(Proveedor, id=proveedor_id)})

def realizar_actualizacion_proveedor(request, proveedor_id):
    p = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        p.nombre_empresa, p.contacto = request.POST.get('nombre_empresa'), request.POST.get('contacto')
        p.telefono, p.email, p.direccion = request.POST.get('telefono'), request.POST.get('email'), request.POST.get('direccion')
        p.tipo_proveedor = request.POST.get('tipo_proveedor')
        p.activo = request.POST.get('activo') == 'on'
        p.save()
    return redirect('ver_proveedores')

def borrar_proveedor(request, proveedor_id):
    p = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST': p.delete(); return redirect('ver_proveedores')
    return render(request, 'proveedor/borrar_proveedor.html', {'proveedor': p})

def agregar_inventario(request):
    if request.method == 'POST':
        Inventario.objects.create(
            producto=get_object_or_404(Producto, id=request.POST.get('producto')),
            proveedor=get_object_or_404(Proveedor, id=request.POST.get('proveedor')),
            cantidad=request.POST.get('cantidad'), unidad_medida=request.POST.get('unidad_medida'),
            stock_minimo=request.POST.get('stock_minimo'), ubicacion=request.POST.get('ubicacion'), lote=request.POST.get('lote')
        )
        return redirect('ver_inventarios')
    return render(request, 'inventario/agregar_inventario.html', {'productos': Producto.objects.all(), 'proveedores': Proveedor.objects.all()})

def ver_inventarios(request):
    return render(request, 'inventario/ver_inventarios.html', {'inventarios': Inventario.objects.all().order_by('producto__nombre')})

def actualizar_inventario(request, inventario_id):
    return render(request, 'inventario/actualizar_inventario.html', {
        'inventario': get_object_or_404(Inventario, id=inventario_id),
        'productos': Producto.objects.all(), 'proveedores': Proveedor.objects.all()
    })

def realizar_actualizacion_inventario(request, inventario_id):
    i = get_object_or_404(Inventario, id=inventario_id)
    if request.method == 'POST':
        i.cantidad, i.unidad_medida = request.POST.get('cantidad'), request.POST.get('unidad_medida')
        i.stock_minimo, i.ubicacion, i.lote = request.POST.get('stock_minimo'), request.POST.get('ubicacion'), request.POST.get('lote')
        i.producto = get_object_or_404(Producto, id=request.POST.get('producto'))
        i.proveedor = get_object_or_404(Proveedor, id=request.POST.get('proveedor'))
        i.save()
    return redirect('ver_inventarios')

def borrar_inventario(request, inventario_id):
    i = get_object_or_404(Inventario, id=inventario_id)
    if request.method == 'POST': i.delete(); return redirect('ver_inventarios')
    return render(request, 'inventario/borrar_inventario.html', {'inventario': i})

def ver_membresias(request):
    return render(request, 'membresia/ver_membresias.html', {'membresias': Membresia.objects.select_related('cliente').all()})