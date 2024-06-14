from Independientes.forms import IndependienteForm,LoginForm,RestablecerContrasenaForm
from .models import Independiente, Usuarios,PasswordResetRequest
from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages
from django.contrib.auth import logout,authenticate,login
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RecuperarContrasenaForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpRequest
import secrets

def ponerToken(request):
    return render(request, 'independientes/resetear_contrasena.html')


class GestionLogin:
    @staticmethod
    def recuperar_contrasena(request):
        if request.method == 'POST':
            form = RecuperarContrasenaForm(request.POST)
            if form.is_valid():
                numero_identificacion = form.cleaned_data['numero_identificacion']

                try:
                    usuario = Independiente.objects.get(numero_identificacion=numero_identificacion)

                    # Crear una solicitud de recuperación de contraseña y guardarla en la base de datos
                    solicitud = PasswordResetRequest(usuario=usuario, token=GestionLogin.generate_token())
                    solicitud.save()

                    # Enviar el correo electrónico con el token para restablecer la contraseña
                    subject = 'Recuperación de Contraseña'
                    html_message = render_to_string('independientes/email/recuperacion_contrasena.html', {'usuario': usuario, 'token': solicitud.token})
                    plain_message = strip_tags(html_message)
                    from_email = 'p4ym4ster@gmail.com'  # Cambiar por tu dirección de correo
                    to_email = usuario.correo
                    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

                    messages.success(request, 'Se ha enviado un correo electrónico con el token para restablecer tu contraseña.')
                    return redirect('resetear_contrasena')  # Redirigir a la página de inicio de sesión después de enviar el correo
                except Independiente.DoesNotExist:
                    messages.error(request, 'No se encontró un usuario con ese número de identificación.')
        else:
            form = RecuperarContrasenaForm()

        return render(request, 'independientes/recuperar_contrasena.html', {'form': form})
    
    
    
    @staticmethod
    def generate_token():
        # Generar un token único y seguro
        return secrets.token_urlsafe(20)


    @staticmethod
    def resetear_contrasena(request):
        if request.method == 'POST':
            form = RestablecerContrasenaForm(request.POST)
            if form.is_valid():
                token = form.cleaned_data['token']
                nueva_contrasena = form.cleaned_data['nueva_contrasena']

                try:
                    solicitud = PasswordResetRequest.objects.get(token=token, used=False)
                    usuario = solicitud.usuario

                    # Cambiar la contraseña del usuario y marcar la solicitud como utilizada
                    usuario.contrasena = make_password(nueva_contrasena)  # Asegúrate de usar make_password para encriptar la contraseña
                    usuario.save()
                    
                    solicitud.used = True
                    solicitud.save()

                    messages.success(request, 'Tu contraseña ha sido restablecida con éxito.')
                    return redirect('resetear_contrasena')  # Redirigir a la página de inicio de sesión

                except PasswordResetRequest.DoesNotExist:
                    messages.error(request, 'El enlace para restablecer la contraseña no es válido o ha expirado.')
                    return redirect('recuperar_contrasena')

        else:
            form = RestablecerContrasenaForm()

        return render(request, 'independientes/resetear_contrasena.html', {'form': form})



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
