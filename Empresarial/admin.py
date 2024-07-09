from django.contrib import admin # type: ignore

# Register your models here.
from .models import Empleado, Empresa, Usuarios,Novedades,Calculos,PasswordResetRequest

admin.site.register(Empleado)
admin.site.register(Empresa)
admin.site.register(Usuarios)
admin.site.register(Novedades)
admin.site.register(Calculos)
admin.site.register(PasswordResetRequest)