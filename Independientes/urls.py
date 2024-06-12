from django.urls import path
from . import views


urlpatterns = [
    path('', views.homeIndependientes,name='homeIndependiente'),
    path('registroIndepe', views.RegistroIndependi,name='registrarIndependiente'),
    path('editaIndepe/<int:numero_identificacion>/', views.editarIndependiente,name='editarIndependiente'),
    path('actualizaIndepe/<int:numero_identificacion>/', views.actualizarIndependiente,name='actualizarIndependiente'),
    path('eliminarIndepen/<int:numero_identificacion>', views.eliminarEmpleado, name='eliminaremple'),
   
]
