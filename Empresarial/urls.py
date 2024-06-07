
from django.urls import path #type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='InicioSesion'),
    path('listarEmpleados', views.ListarEmpleados, name='ListarEmpleados'),
    path('registroEmpleado', views.crearEmpleado, name='registroEmpleado'),
    path('registroEmpresa', views.crearEmpresa, name='registroEmpresa'),
   
]
