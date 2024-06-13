from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home', views.homeIndependientes,name='homeIndependiente'),
    path('registroIndepe', views.RegistroIndependi,name='registrarIndependiente'),
    path('editaIndepe/', views.editarIndependiente,name='editarIndependiente'),
    path('actualizaIndepe/<int:numero_identificacion>/', views.actualizarIndependiente,name='actualizarIndependiente'),
    path('eliminarIndepen/<int:numero_identificacion>', views.eliminarEmpleado, name='eliminaremple'),
   
]
