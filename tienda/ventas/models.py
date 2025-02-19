from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


# Validadores
cedula_validator = RegexValidator(r'^\d{10}$', 'La cédula debe contener exactamente 10 dígitos numéricos.')
telefono_validator = RegexValidator(r'^\d{10}$', 'El teléfono debe contener exactamente 10 dígitos numéricos.')


# Tabla: Clientes
class Cliente(models.Model):
    cedula_cli = models.CharField(max_length=10, primary_key=True, validators=[cedula_validator], unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10, validators=[telefono_validator])
    direccion = models.TextField()

    def save(self, *args, **kwargs):
        # Validar que no se repita la cédula
        if Cliente.objects.filter(cedula_cli=self.cedula_cli).exists():
            raise ValidationError("La cédula ya está registrada.")
        # Validar que no se repita el email
        if Cliente.objects.filter(email=self.email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


# Tabla: Trabajadores
class Trabajador(models.Model):
    CARGO_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Cajero', 'Cajero'),
        ('Vendedor', 'Vendedor'),
    ]

    cedula_tra = models.CharField(max_length=10, primary_key=True, validators=[cedula_validator], unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, validators=[telefono_validator])
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        # Validar que no se repita la cédula
        if Trabajador.objects.filter(cedula_tra=self.cedula_tra).exists():
            raise ValidationError("La cédula ya está registrada.")
        # Validar que no se repita el email
        if Trabajador.objects.filter(email=self.email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"


# Tabla: Productos
class Producto(models.Model):
    id_producto = models.CharField(max_length=4, primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    id_categoria = models.CharField(max_length=100, blank=True, null=True)  # Permite escribir la categoría manualmente

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


# Tabla: Métodos de Pago
class FormaPago(models.Model):
    NOMBRE_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    ]

    id_forma_pago = models.CharField(max_length=10, primary_key=True, unique=True)
    nombre = models.CharField(max_length=20, choices=NOMBRE_CHOICES)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Forma de Pago"
        verbose_name_plural = "Formas de Pago"


# Tabla: Facturas

from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    cedula_cli = models.CharField(max_length=10)
    cedula_tra = models.CharField(max_length=10)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Obtener cliente y trabajador según la cédula
        try:
            if not self.cliente:
                self.cliente = Cliente.objects.get(cedula_cli=self.cedula_cli)
        except Cliente.DoesNotExist:
            raise ValidationError("No se encontró un cliente con esa cédula.")
        
        try:
            if not self.trabajador:
                self.trabajador = Trabajador.objects.get(cedula_tra=self.cedula_tra)
        except Trabajador.DoesNotExist:
            raise ValidationError("No se encontró un trabajador con esa cédula.")
        
        # Obtener producto y forma de pago
        self.producto = Producto.objects.get(id_producto=self.producto.id_producto)
        self.forma_pago = FormaPago.objects.get(id_forma_pago=self.forma_pago.id_forma_pago)

        # Convertir el IVA a tipo Decimal y calcular los valores
        iva_percentage = Decimal('0.15')  # Asegurarnos de que sea un Decimal

        # Calcular subtotal, IVA y total
        self.subtotal = self.cantidad * self.producto.precio
        self.iva = self.subtotal * iva_percentage  # Multiplicamos con Decimal
        self.total = self.subtotal + self.iva

        # Guardar la factura con los cálculos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.id} - {self.cliente.nombre}"

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
