from Independientes.forms import IndependienteForm,LoginForm
from .models import Independiente, Usuarios
from django.shortcuts import render ,redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            numero_identificacion = form.cleaned_data['numero_identificacion']
            contrasena = form.cleaned_data['contrasena']

            try:
                usuario = Usuarios.objects.get(usuario__numero_identificacion=numero_identificacion)
                if check_password(contrasena, usuario.contrasena):
                    # Autenticación exitosa
                    request.session['usuario_id'] = usuario.usuario.numero_identificacion
                    return redirect('independientes/home.html')  # Redirigir a la página de inicio
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Usuarios.DoesNotExist:
                messages.error(request, 'El usuario no existe')
    else:
        form = LoginForm()

    return render(request, 'independientes/login.html', {'form': form})

def inicio_view(request):
    # Aquí puedes implementar la lógica para la página de inicio después de iniciar sesión
    return render(request, 'independientes/home.html')








# Create your views here.
def homeIndependientes(request): 
     return render(request,'independientes/home.html')


def RegistroIndependi(request):
    formulario = IndependienteForm(request.POST, request.FILES)
    if formulario.is_valid():
        formula = formulario.save()
        docu = formula.primer_nombre
        raw_password = docu
        usuario = Usuarios(
            usuario=formula,
            intentos=0,
            estado_u=True,
            id_rol='Independiente'
        )
        usuario.save()
        usuario.set_password(raw_password)     
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
