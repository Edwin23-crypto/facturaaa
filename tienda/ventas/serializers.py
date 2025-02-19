from rest_framework import serializers
from .models import Cliente, Trabajador, Producto, FormaPago, Factura
from django.core.exceptions import ValidationError
from decimal import Decimal

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate_telefono(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError("El teléfono debe contener exactamente 10 dígitos numéricos.")
        return value

    def validate_cedula_cli(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError("La cédula debe contener exactamente 10 dígitos numéricos.")
        if Cliente.objects.filter(cedula_cli=value).exists():
            raise ValidationError("La cédula ya está registrada.")
        return value

    def validate_email(self, value):
        if Cliente.objects.filter(email=value).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return value

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'

    def validate_telefono(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError("El teléfono debe contener exactamente 10 dígitos numéricos.")
        return value

    def validate_cedula_tra(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValidationError("La cédula debe contener exactamente 10 dígitos numéricos.")
        if Trabajador.objects.filter(cedula_tra=value).exists():
            raise ValidationError("La cédula ya está registrada.")
        return value

    def validate_email(self, value):
        if Trabajador.objects.filter(email=value).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return value

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate_id_producto(self, value):
        if Producto.objects.filter(id_producto=value).exists():
            raise ValidationError("El ID del producto ya está registrado.")
        return value

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = '__all__'

    def validate_id_forma_pago(self, value):
        if FormaPago.objects.filter(id_forma_pago=value).exists():
            raise ValidationError("El ID de la forma de pago ya está registrado.")
        return value

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['id', 'cedula_cli', 'cedula_tra', 'producto', 'cantidad', 'subtotal', 'iva', 'total', 'forma_pago']

    def validate(self, data):
        # Aquí validas si los productos y formas de pago existen, antes de hacer el cálculo
        cliente = Cliente.objects.get(cedula_cli=data['cedula_cli'])
        trabajador = Trabajador.objects.get(cedula_tra=data['cedula_tra'])
        producto = Producto.objects.get(id_producto=data['producto'].id_producto)
        forma_pago = FormaPago.objects.get(id_forma_pago=data['forma_pago'].id_forma_pago)

        # Realizar los cálculos antes de devolver la data
        cantidad = Decimal(data['cantidad'])  # Asegurarse de que cantidad es Decimal
        precio = Decimal(producto.precio)  # Convertir precio a Decimal
        subtotal = cantidad * precio
        iva = subtotal * Decimal('0.15')  # IVA como Decimal
        total = subtotal + iva

        # Asignar los valores calculados
        data['subtotal'] = subtotal
        data['iva'] = iva
        data['total'] = total
        return data

