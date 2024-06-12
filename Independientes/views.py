from django.shortcuts import render  
from Independientes.forms import IndependienteForm
from .models import Independiente

# Create your views here.
def homeIndependientes(request): 
     return render(request,'independientes/home.html')
def RegistroIndependi(request):
    formulario = IndependienteForm(request.POST, request.FILES)
    if formulario.is_valid():
        formula=formulario.save()
        # docu=formula.numero_identificacion
        # usuario=Usuarios(None,docu,0,False,'',' General')
        # usuario.save()
        formulario = IndependienteForm()
    return render(request, 'independientes/registroIndependi.html', {'form': formulario, 'mensaje': 'ok'})
def editarIndependiente(request, numero_identificacion):
    empleado = Independiente.objects.get(pk=numero_identificacion)
    formulario = IndependienteForm(instance=empleado)
    return render(request, 'independientes/editarEmpleado.html', {"form": formulario, "empleado": empleado})

def actualizarIndependiente(request, numero_identificacion):
    empleado = Independiente.objects.get(pk=numero_identificacion)
    formulario = IndependienteForm(request.POST, instance=empleado)
    if formulario.is_valid():
        formulario.save()
    empleados = Independiente.objects.all()
    return render(request, 'independientes/listarEmpleado.html', {"get_empleados": empleados})
def eliminarEmpleado(request, numero_identificacion):
    empleado=Independiente.objects.get(pk=numero_identificacion)
    empleado.delete()
    emple=Independiente.objects.all() 
    return render (request, 'independientes/listarEmpleado.html', { "get_empleados": emple})
