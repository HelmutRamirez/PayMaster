from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='InicioSesion'),
    path('listarEmpleados', views.ListarEmpleados, name='ListarEmpleados'),
    path('registroEmpleado', views.crearEmpleado, name='registroEmpleado'),
    path('registroEmpresa', views.crearEmpresa, name='registroEmpresa'),
    path('editarEmpleado/<int:numero_identificacion>/', views.editarEmpleado, name='editarEmpleado'),
    path('actualizar/<int:numero_identificacion>/', views.actualizarEmpleado, name='actualizarEmpleado'),
    path('eliminar/<int:numero_identificacion>', views.eliminarEmpleado, name='eliminaremple'),
]
