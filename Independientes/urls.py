
from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static 
from . import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homePrincipal,name='homeIndependiente'),
    path('registroIndepe', views.RegistroIndependi,name='registrarIndependiente'),
    path('editaIndepe/<int:numero_identificacion>/', views.homePrincipal,name='editarIndependiente'),
    path('actualizaIndepe/<int:numero_identificacion>/', views.homePrincipal,name='actualizarIndependiente'),
    path('eliminarIndepen/<int:numero_identificacion>', views.eliminarEmpleado, name='eliminaremple'),
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
