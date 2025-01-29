from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Empresa)
admin.site.register(models.Profile)
admin.site.register(models.Producto)
admin.site.register(models.Producto_Listing)
admin.site.register(models.Carrito_Detalle)
admin.site.register(models.Categoria)
admin.site.register(models.SubCategoria)