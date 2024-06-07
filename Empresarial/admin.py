from django.contrib import admin # type: ignore

# Register your models here.
from .models import Empleado, Empresa, Usuarios

admin.site.register(Empleado)
admin.site.register(Empresa)
admin.site.register(Usuarios)