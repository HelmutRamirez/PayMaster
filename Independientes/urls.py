from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('cerrar_sesion_redirect/', views.cerrar_sesion_redirect, name='cerrar_sesion_redirect'),
    path('home/',  views.homeIndependientes, name='homeIndependiente'),
    path('registroIndepe', views.RegistroIndependi,name='registrarIndependiente'),
    path('editaIndepe/<int:numero_identificacion>/', views.editarIndependiente,name='editarIndependiente'),
    path('actualizaIndepe/<int:numero_identificacion>/', views.actualizarIndependiente,name='actualizarIndependiente'),
    path('eliminarIndepen/<int:numero_identificacion>', views.eliminarEmpleado, name='eliminaremple'),
   
]
