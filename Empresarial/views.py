from django.shortcuts import render 
from Empresarial.forms import EmpresaForm, EmpleadoForm, UsuariosForm
from .models import Empresa, Empleado, Usuarios

def home (request): 
     return render(request,'home.html')

def crearEmpresa(request):
    formulario = EmpresaForm(request.POST, request.FILES)
    if formulario.is_valid():
        formulario.save()
        formulario = EmpresaForm()
    return render(request, 'registroEmpleado.html', {'form': formulario, 'mensaje': 'ok'})

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
   