from Independientes.forms import IndependienteForm,LoginForm
from .models import Independiente, Usuarios
from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import logout,authenticate,login
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            numero_identificacion = form.cleaned_data['numero_identificacion']
            contrasena = form.cleaned_data['contrasena']

            try:
                # Busca el usuario por número de identificación en tu modelo personalizado
                usuario = Usuarios.objects.get(usuario__numero_identificacion=numero_identificacion)
                permisos=usuario.id_rol
              
                if usuario and usuario.check_password(contrasena):
                    # Autenticación exitosa
                    request.session['numero_identificacion'] = numero_identificacion
                    request.session['estadoSesion'] = True
                    request.session['permisos'] = permisos

                    # Redirige al usuario a la página deseada después del inicio de sesión
                    return redirect('homeIndependiente')
                else:
                    messages.error(request, 'Número de identificación o contraseña incorrectos')
            except Usuarios.DoesNotExist:
                messages.error(request, 'El usuario no existe')

    else:
        form = LoginForm()

    return render(request, 'independientes/login.html', {'form': form})

# @login_required
# def editarIndependiente(request, numero_identificacion):
#     try:
#         empleado = Independiente.objects.get(pk=numero_identificacion)
#         formulario = IndependienteForm(instance=empleado)
#         return render(request, 'independientes/editarIndependi.html', {"form": formulario, "empleado": empleado})
#     except Independiente.DoesNotExist:
#         messages.error(request, 'No se encontró el perfil de Independiente asociado')
#         return redirect('home')

def homeIndependientes(request):
    numero_identificacion = request.session.get('numero_identificacion')
    try:
        independi = Independiente.objects.get(pk=numero_identificacion)
        return render(request, 'independientes/home.html', {'independi': independi})
    except Independiente.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de Independiente asociado')
        return redirect('login')



def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()  
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def cerrar_sesion_redirect(request):
    logout(request)
    request.session.flush()
    return redirect('login') 







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
    independiente = get_object_or_404(Independiente, pk=numero_identificacion)
    formulario = IndependienteForm(instance=independiente)
    return render(request, 'independientes/editarIndependi.html', {'form': formulario, 'independi': independiente})

def actualizarIndependiente(request, numero_identificacion):
    independiente = Independiente.objects.get(pk=numero_identificacion)
    formulario = IndependienteForm(request.POST, instance=independiente)
    if formulario.is_valid():
        formulario.save()
    independiente = Independiente.objects.all()
    return render(request, 'independientes/home.html', {"get_empleados": independiente})


def eliminarEmpleado(request, numero_identificacion):
    independiente=Independiente.objects.get(pk=numero_identificacion)
    independiente.delete()
    independientes=Independiente.objects.all() 
    return render (request, 'independientes/listarEmpleado.html', { "get_empleados": independientes})
