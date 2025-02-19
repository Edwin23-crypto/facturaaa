# ventas/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, TrabajadorViewSet, ProductoViewSet, FormaPagoViewSet, FacturaViewSet

# Creamos el router para registrar los ViewSets automáticamente
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'trabajadores', TrabajadorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'formas-pago', FormaPagoViewSet)
router.register(r'facturas', FacturaViewSet)

# Incluimos las rutas generadas por el router, con el prefijo 'api/'
urlpatterns = [
    path('', include(router.urls)),  # No es necesario repetir 'api/' aquí
]
