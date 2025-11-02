from django.contrib import admin
from .models import OrdenDeTrabajo, Suministro, ConsumoSuministro

# Register your models here.

admin.site.register(OrdenDeTrabajo)
admin.site.register(Suministro)
admin.site.register(ConsumoSuministro)
