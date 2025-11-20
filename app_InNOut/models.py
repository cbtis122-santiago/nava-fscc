from django.db import models

# ==========================================
# MODELO: SUCURSAL
# ==========================================
class Sucursal(models.Model):
    nombre_tienda = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    telefono_tienda = models.CharField(max_length=20)
    es_drive_thru = models.BooleanField(default=False)
    fecha_apertura = models.DateField()

    def __str__(self):
        return f"{self.nombre_tienda} - {self.ciudad}"

# ==========================================
# MODELO: TRABAJADOR (Relación 1:N con Sucursal)
# ==========================================
class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    email = models.EmailField(unique=True)
    telefono_personal = models.CharField(max_length=20, blank=True)
    # Un trabajador pertenece a una sucursal, una sucursal tiene muchos trabajadores
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="trabajadores")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ==========================================
# MODELO: CLIENTE (Nuevo)
# ==========================================
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ==========================================
# MODELO: MEMBRESIA (Relación 1:1 con Cliente)
# ==========================================
class Membresia(models.Model):
    # Un cliente solo tiene una membresía y una membresía pertenece a un solo cliente
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name="membresia")
    numero_tarjeta = models.CharField(max_length=20, unique=True)
    puntos_acumulados = models.PositiveIntegerField(default=0)
    fecha_expiracion = models.DateField()
    nivel = models.CharField(max_length=20, default="Oro", choices=[('Oro', 'Oro'), ('Platino', 'Platino')])

    def __str__(self):
        return f"VIP Card: {self.numero_tarjeta} ({self.cliente.nombre})"

# ==========================================
# MODELO: PEDIDO (Actualizado con relación a Cliente)
# ==========================================
class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    numero_orden = models.PositiveIntegerField()
    total_pedido = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    tipo_orden = models.CharField(max_length=50, choices=[('Comer aqui', 'Comer aquí'), ('Para llevar', 'Para llevar')])
    
    # Relación opcional: Si es cliente frecuente lo seleccionamos, si no, usamos el nombre temporal
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name="pedidos")
    nombre_cliente_temporal = models.CharField(max_length=100, blank=True, help_text="Usar si el cliente no está registrado")
    
    pagado = models.BooleanField(default=False)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.SET_NULL, null=True, blank=True, related_name="pedidos")

    def __str__(self):
        return f"Pedido #{self.numero_orden}"

# ==========================================
# MODELO: PRODUCTO
# ==========================================
class Producto(models.Model):
    CATEGORIAS = [
        ('HAMBURGUESAS', 'Hamburguesas'),
        ('BEBIDAS', 'Bebidas'),
        ('PAPAS', 'Papas'),
        ('POSTRES', 'Postres'),
        ('COMBOS', 'Combos'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    costo = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    disponible = models.BooleanField(default=True)
    imagen = models.CharField(max_length=200, blank=True, help_text="URL de la imagen")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

# ==========================================
# MODELO: DETALLE PEDIDO (Relación N:M Intermedia)
# ==========================================
# Esta tabla conecta Pedidos con Productos (Muchos a Muchos)
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2, help_text="Precio al momento de la compra")
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcula el subtotal automáticamente antes de guardar
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Orden #{self.pedido.numero_orden}"

# ==========================================
# MODELO: PROVEEDOR
# ==========================================
class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    tipo_proveedor = models.CharField(max_length=50, choices=[
        ('ALIMENTOS', 'Alimentos'),
        ('BEBIDAS', 'Bebidas'),
        ('LIMPIEZA', 'Limpieza'),
        ('EQUIPOS', 'Equipos')
    ])
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre_empresa

# ==========================================
# MODELO: INVENTARIO (Actualizado)
# ==========================================
class Inventario(models.Model):
    UNIDADES = [
        ('Unidad', 'Unidad'),
        ('kg', 'Kilogramos'),
        ('lt', 'Litros'),
    ]
    UBICACIONES = [
        ('Almacén principal', 'Almacén principal'),
        ('Almacén secundario', 'Almacén secundario'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="inventarios")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="inventarios")
    
    # Permitimos decimales para kg o litros (ej. 2.5 kg)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    
    unidad_medida = models.CharField(max_length=20, choices=UNIDADES, default="Unidad")
    stock_minimo = models.PositiveIntegerField(default=10)
    ubicacion = models.CharField(max_length=50, choices=UBICACIONES, default="Almacén principal")
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    lote = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} {self.unidad_medida}"