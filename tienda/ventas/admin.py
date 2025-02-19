from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Trabajador, Producto, FormaPago, Factura
from django.core.validators import RegexValidator

# Formularios personalizados con validaciones
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 10:
            raise ValidationError("El teléfono debe contener exactamente 10 dígitos numéricos.")
        return telefono

    def clean_cedula_cli(self):
        cedula = self.cleaned_data.get('cedula_cli')
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValidationError("La cédula debe contener exactamente 10 dígitos numéricos.")
        if Cliente.objects.filter(cedula_cli=cedula).exists():
            raise ValidationError("La cédula ya está registrada.")
        return cedula

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cliente.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = '__all__'

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 10:
            raise ValidationError("El teléfono debe contener exactamente 10 dígitos numéricos.")
        return telefono

    def clean_cedula_tra(self):
        cedula = self.cleaned_data.get('cedula_tra')
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValidationError("La cédula debe contener exactamente 10 dígitos numéricos.")
        if Trabajador.objects.filter(cedula_tra=cedula).exists():
            raise ValidationError("La cédula ya está registrada.")
        return cedula

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Trabajador.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def clean_id_producto(self):
        id_producto = self.cleaned_data.get('id_producto')
        if Producto.objects.filter(id_producto=id_producto).exists():
            raise ValidationError("El ID del producto ya está registrado.")
        return id_producto

class FormaPagoForm(forms.ModelForm):
    class Meta:
        model = FormaPago
        fields = '__all__'

    def clean_id_forma_pago(self):
        id_forma_pago = self.cleaned_data.get('id_forma_pago')
        if FormaPago.objects.filter(id_forma_pago=id_forma_pago).exists():
            raise ValidationError("El ID de la forma de pago ya está registrado.")
        return id_forma_pago

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'

    def clean_cedula_cli(self):
        cedula_cli = self.cleaned_data.get('cedula_cli')
        if not cedula_cli.isdigit() or len(cedula_cli) != 10:
            raise ValidationError("La cédula del cliente debe contener exactamente 10 dígitos numéricos.")
        try:
            cliente = Cliente.objects.get(cedula_cli=cedula_cli)
            self.cleaned_data['cliente'] = cliente
        except Cliente.DoesNotExist:
            raise ValidationError("La cédula del cliente no está registrada.")
        return cedula_cli

    def clean_cedula_tra(self):
        cedula_tra = self.cleaned_data.get('cedula_tra')
        if not cedula_tra.isdigit() or len(cedula_tra) != 10:
            raise ValidationError("La cédula del trabajador debe contener exactamente 10 dígitos numéricos.")
        try:
            trabajador = Trabajador.objects.get(cedula_tra=cedula_tra)
            self.cleaned_data['trabajador'] = trabajador
        except Trabajador.DoesNotExist:
            raise ValidationError("La cédula del trabajador no está registrada.")
        return cedula_tra

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        producto = self.cleaned_data.get('producto')
        if cantidad and producto:
            subtotal = cantidad * producto.precio
            iva = subtotal * 0.15  # IVA del 15%
            total = subtotal + iva
            self.cleaned_data['subtotal'] = subtotal
            self.cleaned_data['iva'] = iva
            self.cleaned_data['total'] = total
        return cantidad

class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm

class TrabajadorAdmin(admin.ModelAdmin):
    form = TrabajadorForm

class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm

class FormaPagoAdmin(admin.ModelAdmin):
    form = FormaPagoForm

class FacturaAdmin(admin.ModelAdmin):
    form = FacturaForm
    list_display = ('id', 'cedula_cli', 'cliente', 'cedula_tra', 'trabajador', 'producto', 'cantidad', 'subtotal', 'iva', 'total', 'forma_pago', 'fecha')
    search_fields = ['id', 'cliente__cedula_cli', 'trabajador__cedula_tra']
    list_filter = ['fecha', 'forma_pago']

# Registro de modelos
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(FormaPago, FormaPagoAdmin)
admin.site.register(Factura, FacturaAdmin)
