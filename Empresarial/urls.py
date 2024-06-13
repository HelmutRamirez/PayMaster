from django.urls import path
from . import views
urlpatterns = [
    path('', views.Paginas.home, name='homeEmpresarial'),
    path('empresa', views.Paginas.homeEmpresa, name='homeEmpresa'),
    path('empleado', views.Paginas.homeEmpleado, name='homeEmpleado'),
    path('listarEmpleados', views.GestionEmpleado.ListarEmpleados, name='ListarEmpleados'),
    path('registroEmpleado', views.GestionEmpleado.crearEmpleado, name='registroEmpleado'),
    path('registroEmpresa', views.GestionarEmpresa.crearEmpresa, name='registroEmpresa'),
    path('editarEmpleado/<int:numero_identificacion>/', views.GestionEmpleado.editarEmpleado, name='editarEmpleado'),
    path('actualizar/<int:numero_identificacion>/', views.GestionEmpleado.actualizarEmpleado, name='actualizarEmpleado'),
    path('eliminar/<int:numero_identificacion>/', views.GestionEmpleado.eliminarEmpleado, name='eliminaremple'),
    path('listarEmpresa', views.GestionarEmpresa.ListarEmpresa, name='ListarEmpresa'),
    path('editarEmpresa/<int:nit>/', views.GestionarEmpresa.editarEmpresa, name='editarEmpresa'),
    path('actualizarempre/<int:nit>/', views.GestionarEmpresa.actualizarEmpresa, name='actualizarEmpresa'),
    path('eliminar/<int:nit>/', views.GestionarEmpresa.eliminarEmpresa, name='eliminarempre'),
    # path('registroCalculos', views.Calculos.registrarCalculos, name='registroCalculos'), 
    path('calcular/<int:numero_identificacion>/', views.Calculos.calcularSalario, name='calcularemple'),
    # path('registrarNovedades', views.Calculos.registrarNovedades, name='registrarNovedades')
]