from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homeEmpresarial'),
    path('empresa', views.homeEmpresa, name='homeEmpresa'),
    path('empleado', views.homeEmpleado, name='homeEmpleado'),
    path('listarEmpleados', views.ListarEmpleados, name='ListarEmpleados'),
    path('registroEmpleado', views.crearEmpleado, name='registroEmpleado'),
    path('registroEmpresa', views.crearEmpresa, name='registroEmpresa'),
    path('editarEmpleado/<int:numero_identificacion>/', views.editarEmpleado, name='editarEmpleado'),
    path('actualizar/<int:numero_identificacion>/', views.actualizarEmpleado, name='actualizarEmpleado'),
    path('eliminar/<int:numero_identificacion>/', views.eliminarEmpleado, name='eliminaremple'),
    path('listarEmpresa', views.ListarEmpresa, name='ListarEmpresa'),
    path('editarEmpresa/<int:nit>/', views.editarEmpresa, name='editarEmpresa'),
    path('actualizarempre/<int:nit>/', views.actualizarEmpresa, name='actualizarEmpresa'),
    path('eliminar/<int:nit>/', views.eliminarEmpresa, name='eliminarempre'),
    path('registroCalculos', views.registrarCalculos, name='registroCalculos'), 
    path('calcular/<int:numero_identificacion>/', views.calcularSalario, name='calcularemple'),
    path('registrarNovedades', views.registrarNovedades, name='registrarNovedades')
]
