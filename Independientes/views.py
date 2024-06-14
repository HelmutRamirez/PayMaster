from Independientes.forms import IndependienteForm,LoginForm,PasswordResetForm
from .models import Independiente, Usuarios,PasswordResetRequest
from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect

from .forms import RecuperarContrasenaForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpRequest
import secrets
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

def cargar_token(request): 
        return render(request,'independientes/resetear_contrasena.html')

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
                    return redirect('password_reset')  # Redirigir a la página para ingresar el token

                except Independiente.DoesNotExist:
                    messages.error(request, 'No se encontró un usuario con ese número de identificación.')

        else:
            form = RecuperarContrasenaForm()

        return render(request, 'independientes/recuperar_contrasena.html', {'form': form})

    def password_reset(request):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                token = form.cleaned_data['token']
                new_password = form.cleaned_data['new_password']

                try:
                    reset_request = PasswordResetRequest.objects.get(token=token, used=False)
                except PasswordResetRequest.DoesNotExist:
                    reset_request = None

                if reset_request:
                    usuario = reset_request.usuario  # Ajusta según tu modelo de PasswordResetRequest
                    usuario = Usuarios.objects.get(usuario=usuario)
                    
                    
                    usuario.set_password(new_password)

                    reset_request.used = True
                    reset_request.save()

                    messages.success(request, 'Contraseña actualizada correctamente. Por favor, inicia sesión.')
                    return redirect('login')  # Redirige a la página de inicio de sesión después de cambiar la contraseña

                else:
                    messages.error(request, 'El token de restablecimiento de contraseña no es válido o ya ha sido utilizado.')
            
            else:
                messages.error(request, 'Por favor, corrige los errores del formulario.')

        else:
            form = PasswordResetForm()

        return render(request, 'independientes/password_reset.html', {'form': form})



    @staticmethod
    def generate_token():
        # Generar un token único y seguro
        return secrets.token_urlsafe(20)


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
        return redirect('login') 
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
