from django.contrib import admin
from .models import Independiente,Usuarios,PasswordResetRequest
# Register your models here.


admin.site.register(Independiente)
admin.site.register(Usuarios)
admin.site.register(PasswordResetRequest)
