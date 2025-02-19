from rest_framework import viewsets
from .models import Cliente, Trabajador, Producto, FormaPago, Factura
from .serializers import ClienteSerializer, TrabajadorSerializer, ProductoSerializer, FormaPagoSerializer, FacturaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class FormaPagoViewSet(viewsets.ModelViewSet):
    queryset = FormaPago.objects.all()
    serializer_class = FormaPagoSerializer

from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status
from .serializers import FacturaSerializer
from .models import Factura, Producto, Cliente, Trabajador, FormaPago

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

    def perform_create(self, serializer):
        # Obtener los datos
        cedula_cli = self.request.data.get('cedula_cli')
        cedula_tra = self.request.data.get('cedula_tra')
        producto_id = self.request.data.get('producto')
        cantidad = self.request.data.get('cantidad')
        forma_pago_id = self.request.data.get('forma_pago')

        # Obtener las instancias de Cliente, Trabajador, Producto y FormaPago
        cliente = Cliente.objects.get(cedula_cli=cedula_cli)
        trabajador = Trabajador.objects.get(cedula_tra=cedula_tra)
        producto = Producto.objects.get(id_producto=producto_id)
        forma_pago = FormaPago.objects.get(id_forma_pago=forma_pago_id)

        # Asegurarse de que cantidad y precio son de tipo Decimal
        cantidad_decimal = Decimal(cantidad)
        precio_decimal = Decimal(producto.precio)

        # Realizar los cálculos
        subtotal = cantidad_decimal * precio_decimal
        iva = subtotal * Decimal('0.15')  # 15% de IVA
        total = subtotal + iva

        # Guardar los datos calculados en el serializer
        serializer.save(
            cliente=cliente,
            trabajador=trabajador,
            producto=producto,
            forma_pago=forma_pago,
            subtotal=subtotal,
            iva=iva,
            total=total
        )

        # Devolver la respuesta
        return Response(serializer.data, status=status.HTTP_201_CREATED)


