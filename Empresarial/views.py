from django.shortcuts import render  # type: ignore
from Empresarial.forms import EmpresaForm, EmpleadoForm, UsuariosForm
from .models import Empresa, Empleado, Usuarios

def home (request): 
     return render(request,'home.html')

def crearEmpresa(request):
    formulario = EmpresaForm(request.POST, request.FILES)
    if formulario.is_valid():
        formulario.save()
        formulario = EmpresaForm()
    return render(request, 'registroEmpresa.html', {'form': formulario, 'mensaje': 'ok'})

def crearEmpleado(request):
    formulario = EmpleadoForm(request.POST, request.FILES)
    if formulario.is_valid():
        formula=formulario.save()
        docu=formula.numero_identificacion
        usuario=Usuarios(None,docu,0,False,'','Empleado General')
        usuario.save()
        formulario = EmpleadoForm()
    return render(request, 'registroEmpleado.html', {'form': formulario, 'mensaje': 'ok'})

def crearUsuarios(request):
    formulario = UsuariosForm(request.POST, request.FILES)
    if formulario.is_valid():
        formulario.save()
        formulario = UsuariosForm()
    return render(request, 'registroUsuarios.html', {'form': formulario, 'mensaje': 'ok'})

def ListarEmpleados(request):
    get_empleados = Empleado.objects.all()
    data = {
        'get_empleados': get_empleados
    }
    return render(request, 'listarEmpleado.html', data)

def ListarEmpresa(request):
    get_empresa = Empresa.objects.all()
    data = {
        'get_empresa': get_empresa
    }
    return render(request, 'listarEmpresa.html', data)

def editarEmpleado(request, numero_identificacion):
    empleado = Empleado.objects.get(pk=numero_identificacion)
    formulario = EmpleadoForm(instance=empleado)
    return render(request, 'editarEmpleado.html', {"form": formulario, "empleado": empleado})

def actualizarEmpleado(request, numero_identificacion):
    empleado = Empleado.objects.get(pk=numero_identificacion)
    formulario = EmpleadoForm(request.POST, instance=empleado)
    if formulario.is_valid():
        formulario.save()
    empleados = Empleado.objects.all()
    return render(request, 'listarEmpleado.html', {"get_empleados": empleados})



def editarEmpresa(request, nit):
    empresa = Empresa.objects.get(pk=nit)
    formulario = EmpresaForm(instance=empresa)
    return render(request, 'editarEmpresa.html', {"form": formulario, "empresa": empresa})


def actualizarEmpresa(request, nit):
    empresa = Empresa.objects.get(pk=nit)
    formulario = EmpresaForm(request.POST, instance=empresa)
    if formulario.is_valid():
        formulario.save()
    empresa = Empresa.objects.all()
    return render(request, 'listarEmpresa.html', {"get_empresa": empresa})


def eliminarEmpleado(request, numero_identificacion):
    empleado=Empleado.objects.get(pk=numero_identificacion)
    empleado.delete()
    emple=Empleado.objects.all() 
    return render (request, 'listarEmpleado.html', { "get_empleados": emple})