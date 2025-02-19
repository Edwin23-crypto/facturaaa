# tiendaproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ventas.urls')),  # Incluye las rutas de ventas con el prefijo 'api/'
]
