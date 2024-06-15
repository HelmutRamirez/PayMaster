from django.urls import path
from . import views
urlpatterns = [
    #gestion login
    path('accounts/login/', views.GestionLogin.login_view, name='loginEmpresa'),
    path('recuperar-contrasena_empre/', views.GestionLogin.recuperar_contrasena, name='recuperar_contrasena_empre'),
    path('password-reset_empre/', views.GestionLogin.password_reset, name='password_reset_empre'),
    path('cerrar_sesion_empre/', views.GestionLogin.cerrar_sesion, name='cerrar_sesion_empre'),
    path('cerrar_sesion_redirect_de/', views.GestionLogin.cerrar_sesion_redirect, name='cerrar_sesion_redirect_e'),
    path('keep-session-alive/', views.keep_session_alive, name='keep_session_alive'),
    
    #Gestion de Empresa
    path('empresa', views.Paginas.homeEmpresa, name='homeEmpresa'),
    path('registroEmpresa', views.GestionarEmpresa.crearEmpresa, name='registroEmpresa'),
    path('listarEmpresa', views.GestionarEmpresa.ListarEmpresa, name='ListarEmpresa'),
    path('editarEmpresa/<int:nit>/', views.GestionarEmpresa.editarEmpresa, name='editarEmpresa'),
    path('actualizarempre/<int:nit>/', views.GestionarEmpresa.actualizarEmpresa, name='actualizarEmpresa'),
    path('eliminar/<int:nit>/', views.GestionarEmpresa.eliminarEmpresa, name='eliminarempre'),
    #Gestion de empleado
    path('empleado', views.Paginas.homeEmpleado, name='homeEmpleado'),
    path('registroEmpleado', views.GestionEmpleado.crearEmpleado, name='registroEmpleado'),
    path('listarEmpleados/<int:nit>', views.GestionEmpleado.ListarEmpleados, name='ListarEmpleados'),
    path('editarEmpleado/<int:numero_identificacion>/', views.GestionEmpleado.editarEmpleado, name='editarEmpleado'),
    path('actualizar/<int:numero_identificacion>/', views.GestionEmpleado.actualizarEmpleado, name='actualizarEmpleado'),
    path('eliminar/<int:numero_identificacion>/', views.GestionEmpleado.eliminarEmpleado, name='eliminaremple'),
    #Gestion de Calculos
    path('calcular/<int:numero_identificacion>/', views.CalculosGenerales.calcularSalario, name='calcularemple'),

    
]