from Independientes.forms import IndependienteForm,LoginForm,PasswordResetForm
from .models import DatosCalculos, Independiente, Usuarios,PasswordResetRequest
from django.shortcuts import render ,redirect, get_object_or_404 # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import logout # type: ignore
from django.http import JsonResponse, HttpResponseRedirect # type: ignore
from .forms import DatosCalculosForm, RecuperarContrasenaForm
from django.core.mail import send_mail # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.http import HttpRequest # type: ignore
import secrets
from django.utils.http import urlsafe_base64_decode # type: ignore
from django.utils.encoding import force_str # type: ignore

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
                indepe = Independiente.objects.get(pk=numero_identificacion)
                permisos=usuario.id_rol
                userName=indepe.primer_nombre
              
                if usuario and usuario.check_password(contrasena):
                    # Autenticación exitosa
                    request.session['numero_identificacion'] = numero_identificacion
                    request.session['estadoSesion'] = True
                    request.session['permisos'] = permisos
                    request.session['user'] = userName


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
        raw_password = formula.primer_nombre
        usuario = Usuarios(
            usuario=formula,
            intentos=0,
            estado_u=True,
            id_rol='Independiente'
        )
        usuario.save()
        usuario.set_password(raw_password)  
        datos_calculos=DatosCalculos(documento=formula)
        datos_calculos.save()   
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
        independiente = Independiente.objects.get(pk=numero_identificacion)
    return render(request, 'independientes/home.html', {"independi": independiente})


def eliminarEmpleado(request, numero_identificacion):
    independiente=Independiente.objects.get(pk=numero_identificacion)
    independiente.delete()
    independientes=Independiente.objects.all() 
    return render (request, 'independientes/listarEmpleado.html', { "get_empleados": independientes})

class CalculosGenerales(HttpRequest):
    def calcular_aportes(request, numero_identificacion):
        
            independiente = Independiente.objects.get(pk=numero_identificacion)

# Busca la instancia de DatosCalculos relacionada con el independiente
            try:
                datos_calculos = DatosCalculos.objects.get(documento=independiente)
            except DatosCalculos.DoesNotExist:
                datos_calculos = None

            if request.method == 'POST':
                form = DatosCalculosForm(request.POST, instance=datos_calculos)
                if form.is_valid():
                    # Asigna la relación con independiente si es una nueva instancia
                    calculos = form.save(commit=False)
                    if datos_calculos is None:
                        calculos.documento = independiente
                    calculos.save()
                    # Aquí puedes redirigir a otra página o renderizar una respuesta
          
                datos_calculos=DatosCalculos.objects.filter(documento=independiente)#esto es para traer los datos                 
                
                for objeto in datos_calculos:
                    
                    salario_base = objeto.salarioBase
                    nivel_arl = objeto.arl
                    ccf = objeto.CCF
                    porcentaje_ibc=objeto.ibc
                    
                
                ibc = salario_base * (porcentaje_ibc/100)
                if ibc<1300000:
                    ibc=1300000
                    
                salud = ibc * 0.125
                pension = ibc * 0.16
                
                
             
                # fsp =fsp
            
                arl = CalculosGenerales.calcular_arl (ibc,nivel_arl)
                
                
                if ccf == 'Si':
                    ccf = ibc * 0.04
                else:
                    ccf = 0
                
                salud = salud
                pension = pension
                # fsp = fsp
                
                context = {
                    'independiente': independiente,
                    'salario_base': salario_base,
                    'ibc': ibc,
                    'salud': salud,
                    'pension': pension,
                    'arl': arl,
                    'ccf': ccf,
                    # 'fsp': fsp
                }
                
                return render(request, 'independientes/resultado_calculos.html', context)
            
            
            else:
                form = DatosCalculosForm()
        
            return render(request, 'independientes/calcular_aportes.html', {'form': form, 'independiente': independiente})
    

    # def calcular_fsp(ibc):
    #         smmlv = 1300000  
    #         if 4 * smmlv <= ibc < 16 * smmlv:
    #             return ibc * 0.01
    #         elif 16 * smmlv <= ibc < 17 * smmlv:
    #             return ibc * 0.012
    #         elif 17 * smmlv <= ibc < 18 * smmlv:
    #             return ibc * 0.014
    #         elif 18 * smmlv <= ibc < 19 * smmlv:
    #             return ibc * 0.016
    #         elif 19 * smmlv <= ibc < 20 * smmlv:
    #             return ibc * 0.018
    #         elif ibc >= 20 * smmlv:
    #             return ibc * 0.02
    #         else:
    #             return 0

    def calcular_arl(ibc, arl_nivel):
        
        if arl_nivel == '1':
                arl = ibc * 0.00522
        elif arl_nivel == '2':
                arl = ibc * 0.01044
        elif arl_nivel == '3':
                arl = ibc * 0.02436
        elif arl_nivel == '4':
                arl = ibc * 0.04350
        elif arl_nivel == '5':
                arl = ibc * 0.06960
        elif arl_nivel == '0':
                arl = 0
        return (arl)
        


      

