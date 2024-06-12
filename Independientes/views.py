from django.shortcuts import render  
from Empresarial.forms import EmpresaForm, EmpleadoForm, UsuariosForm
from .models import Empresa, Empleado, Usuarios

# Create your views here.
def home (request): 
     return render(request,'empresarial/home.html')
def crearEmpleado(request):
    formulario = EmpleadoForm(request.POST, request.FILES)
    if formulario.is_valid():
        formula=formulario.save()
        docu=formula.numero_identificacion
        usuario=Usuarios(None,docu,0,False,'','Empleado General')
        usuario.save()
        formulario = EmpleadoForm()
    return render(request, 'empresarial/registroEmpleado.html', {'form': formulario, 'mensaje': 'ok'})
def editarEmpleado(request, numero_identificacion):
    empleado = Empleado.objects.get(pk=numero_identificacion)
    formulario = EmpleadoForm(instance=empleado)
    return render(request, 'empresarial/editarEmpleado.html', {"form": formulario, "empleado": empleado})

def actualizarEmpleado(request, numero_identificacion):
    empleado = Empleado.objects.get(pk=numero_identificacion)
    formulario = EmpleadoForm(request.POST, instance=empleado)
    if formulario.is_valid():
        formulario.save()
    empleados = Empleado.objects.all()
    return render(request, 'empresarial/listarEmpleado.html', {"get_empleados": empleados})
def eliminarEmpleado(request, numero_identificacion):
    empleado=Empleado.objects.get(pk=numero_identificacion)
    empleado.delete()
    emple=Empleado.objects.all() 
    return render (request, 'empresarial/listarEmpleado.html', { "get_empleados": emple})
