from django.shortcuts import render ,get_object_or_404, redirect # type: ignore
from Empresarial.forms import EmpresaForm, EmpleadoForm, UsuariosForm
from .models import Empresa, Empleado, Usuarios

from .models import Empleado, Calculos, Novedades
from .forms import EmpleadoForm, CalculosForm, NovedadesForm

def home (request): 
     return render(request,'empresarial/home.html')
def homeEmpleado (request): 
     return render(request,'empresarial/homeEmpleado.html')
def homeEmpresa (request): 
     return render(request,'empresarial/homeEmpresa.html')

def crearEmpresa(request):
    formulario = EmpresaForm(request.POST, request.FILES)
    if formulario.is_valid():
        formulario.save()
        formulario = EmpresaForm()
    return render(request, 'empresarial/registroEmpresa.html', {'form': formulario, 'mensaje': 'ok'})

def crearEmpleado(request):
    formulario = EmpleadoForm(request.POST, request.FILES)
    if formulario.is_valid():
        formula=formulario.save()
        docu=formula.numero_identificacion
        usuario=Usuarios(None,docu,0,False,'','Empleado General')
        usuario.save()
        formulario = EmpleadoForm()
    return render(request, 'empresarial/registroEmpleado.html', {'form': formulario, 'mensaje': 'ok'})

def crearUsuarios(request):
    formulario = UsuariosForm(request.POST, request.FILES)
    if formulario.is_valid():
        formulario.save()
        formulario = UsuariosForm()
    return render(request, 'empresarial/registroUsuarios.html', {'form': formulario, 'mensaje': 'ok'})

def ListarEmpleados(request):
    get_empleados = Empleado.objects.all()
    data = {
        'get_empleados': get_empleados
    }
    return render(request, 'empresarial/listarEmpleado.html', data)

def ListarEmpresa(request):
    get_empresa = Empresa.objects.all()
    data = {
        'get_empresa': get_empresa
    }
    return render(request, 'empresarial/listarEmpresa.html', data)

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



def editarEmpresa(request, nit):
    empresa = Empresa.objects.get(pk=nit)
    formulario = EmpresaForm(instance=empresa)
    return render(request, 'empresarial/editarEmpresa.html', {"form": formulario, "empresa": empresa})


def actualizarEmpresa(request, nit):
    empresa = Empresa.objects.get(pk=nit)
    formulario = EmpresaForm(request.POST, instance=empresa)
    if formulario.is_valid():
        formulario.save()
    empresa = Empresa.objects.all()
    return render(request, 'empresarial/listarEmpresa.html', {"get_empresa": empresa})


def eliminarEmpleado(request, numero_identificacion):
    empleado=Empleado.objects.get(pk=numero_identificacion)
    empleado.delete()
    emple=Empleado.objects.all() 
    return render (request, 'listarEmpleado.html', { "get_empleados": emple})

def eliminarEmpresa(request, nit):
    empresa=Empresa.objects.get(pk=nit)
    empresa.delete()
    empre=Empresa.objects.all() 
    return render (request, 'listarEmpresa.html', { "get_empresa": empre})

def calcularSalario(request, numero_identificacion):
    empleado = get_object_or_404(Empleado, numero_identificacion=numero_identificacion)
    calculos, created = Calculos.objects.get_or_create(documento=empleado)
    novedades = Novedades.objects.filter(empleado=empleado).first()

    salario_base = calculos.salarioBase 
    salud = salario_base * 0.04
    pension = salario_base * 0.04
    arl = salario_base * 0.00522
    caja_compensacion = salario_base * 0.04
    cesantias = salario_base * 0.0833
    interes_cesantias = cesantias * 0.12
    vacaciones = salario_base * 0.0417

    if novedades:
        horas_extra_diurnas = novedades.HorasExDiu 
        horas_extra_nocturnas = novedades.HorasExNoc 
        horas_extra_festivas_diurnas = novedades.HorasExFestivaDiu 
        horas_extra_festivas_nocturnas = novedades.HorasExFestivaNoc 

        valor_hora_extra_diurna = (salario_base / 240) * 1.25 * horas_extra_diurnas
 
        valor_hora_extra_nocturna = (salario_base / 240) * 1.75 * horas_extra_nocturnas
      
        valor_hora_extra_festiva_diurna = (salario_base / 240) * 2.0 * horas_extra_festivas_diurnas
      
        valor_hora_extra_festiva_nocturna = (salario_base / 240) * 2.5 * horas_extra_festivas_nocturnas
    else:
        valor_hora_extra_diurna = 0
        valor_hora_extra_nocturna = 0
        valor_hora_extra_festiva_diurna = 0
        valor_hora_extra_festiva_nocturna = 0

    total_extras = (valor_hora_extra_diurna + valor_hora_extra_nocturna +
                    valor_hora_extra_festiva_diurna + valor_hora_extra_festiva_nocturna)

    calculos.salud = salud
    calculos.pension = pension
    calculos.arl = arl
    calculos.cajaCompensacion = caja_compensacion
    calculos.vacaciones = vacaciones

    calculos.save()

    context = {
        'empleado': empleado,
        'calculos': calculos,
        'total_extras': total_extras
    }
    return render(request, './empresarial/resultado_calculo.html', context)


def registrarNovedades(request):
    if request.method == 'POST':
        form = NovedadesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ListarEmpleados')
    else:
        form = NovedadesForm()
    return render(request, 'registrar_novedades.html', {'form': form})

def calcular_contribuciones(salario, nivel_riesgo):
    salud = salario * 0.04
    pension = salario * 0.04

    arl_porcentajes = {
        1: 0.00522,
        2: 0.01044,
        3: 0.02436,
        4: 0.04350,
        5: 0.06960,
    }
    arl = salario * arl_porcentajes.get(nivel_riesgo, 0.00522)

    return salud, pension, arl

def registrarCalculos(request):
    if request.method == 'POST':
        form = CalculosForm(request.POST)
        if form.is_valid():
            calculo = form.save(commit=False)
            calculo.salud, calculo.pension, calculo.arl = calcular_contribuciones(calculo.salarioBase, calculo.nivel_riesgo)
            calculo.save()
            return redirect('ListarEmpleados')
    else:
        form = CalculosForm()
    return render(request, './empresarial/registrar_calculos.html', {'form': form})