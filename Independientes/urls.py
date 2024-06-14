from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('recuperar-contrasena/', views.GestionLogin.recuperar_contrasena, name='recuperar_contrasena'),
    path('resetear-contrasena/<str:uidb64>/<str:token>/', views.GestionLogin.resetear_contrasena, name='resetear_contrasena'),
    path('ponerToken/', views.ponerToken, name='cargar_token'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('cerrar_sesion_redirect/', views.cerrar_sesion_redirect, name='cerrar_sesion_redirect'),
    path('home/', views.homeIndependientes, name='homeIndependiente'),
    path('registroIndepe/', views.RegistroIndependi, name='registrarIndependiente'),
    path('editaIndepe/<int:numero_identificacion>/', views.editarIndependiente, name='editarIndependiente'),
    path('actualizaIndepe/<int:numero_identificacion>/', views.actualizarIndependiente, name='actualizarIndependiente'),
    path('eliminarIndepen/<int:numero_identificacion>/', views.eliminarEmpleado, name='eliminaremple'),
]