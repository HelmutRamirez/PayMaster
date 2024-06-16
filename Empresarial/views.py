
from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from Empresarial.forms import EmpresaForm, EmpleadoForm,LoginForm, PasswordResetForm,RecuperarContrasenaForm
from .models import Empresa, Empleado, Usuarios, Calculos, Novedades, PasswordResetRequest
from django.core.mail import send_mail # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect # type: ignore
import secrets
from django.contrib import messages # type: ignore
from django.contrib.auth import logout # type: ignore
from django.utils.http import urlsafe_base64_decode # type: ignore
from django.utils.encoding import force_str # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.http import require_POST # type: ignore

class GestionLogin:

    @staticmethod
    def recuperar_contrasena(request):
        if request.method == 'POST':
            form = RecuperarContrasenaForm(request.POST)
            if form.is_valid():
                numero_identificacion = form.cleaned_data['numero_identificacion']

                try:
                    usuario = Empleado.objects.get(numero_identificacion=numero_identificacion)

                    # Crear una solicitud de recuperación de contraseña y guardarla en la base de datos
                    solicitud = PasswordResetRequest(usuario=usuario, token=GestionLogin.generate_token())
                    solicitud.save()

                    # Enviar el correo electrónico con el token para restablecer la contraseña
                    subject = 'Recuperación de Contraseña'
                    html_message = render_to_string('empresarial/email/recuperacion_contrasena.html', {'usuario': usuario, 'token': solicitud.token})
                    plain_message = strip_tags(html_message)
                    from_email = 'p4ym4ster@gmail.com'  # Cambiar por tu dirección de correo
                    to_email = usuario.correo
                    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

                    messages.success(request, 'Se ha enviado un correo electrónico con el token para restablecer tu contraseña.')
                    return redirect('password_reset_empre')  # Redirigir a la página para ingresar el token

                except Empleado.DoesNotExist:
                    messages.error(request, 'No se encontró un usuario con ese número de identificación.')

        else:
            form = RecuperarContrasenaForm()

        return render(request, 'empresarial/recuperar_contrasena.html', {'form': form})

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

                    usuario.intentos = 0
                    usuario.estado_u = True
                    usuario.save()
                    
                    messages.success(request, 'Contraseña actualizada correctamente. Por favor, inicia sesión.')
                    return redirect('loginEmpresa')  # Redirige a la página de inicio de sesión después de cambiar la contraseña

                else:
                    messages.error(request, 'El token de restablecimiento de contraseña no es válido o ya ha sido utilizado.')
            
            else:
                messages.error(request, 'Por favor, corrige los errores del formulario.')

        else:
            form = PasswordResetForm()

        return render(request, 'empresarial/password_reset.html', {'form': form})



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
                    usuario = Usuarios.objects.get(usuario__numero_identificacion=numero_identificacion)
                    indepe = Empleado.objects.get(pk=numero_identificacion)
                    permisos = usuario.id_rol
                    userName = indepe.primer_nombre

                    if usuario.estado_u:
                        if usuario.check_password(contrasena):
                           
                            usuario.intentos = 0
                            usuario.save()
                            
                            request.session['numero_identificacion'] = numero_identificacion
                            request.session['estadoSesion'] = True
                            request.session['permisos'] = permisos
                            request.session['user'] = userName

                            data = {'independi': indepe}

                            if permisos == 'Contador' or permisos == 'Auxiliar Contable' or permisos == 'RRHH':
                                return render(request, 'empresarial/homeEmpresa.html', data)
                            elif permisos == 'Empleado General':
                                return render(request, 'empresarial/Empleado.html', data)

                        else:
                            
                            usuario.intentos += 1
                            usuario.save()
                            if usuario.intentos >= 3:
                                usuario.estado_u = False
                                usuario.save()
                                messages.error(request, 'La cuenta ha sido inhabilitada debido a múltiples intentos fallidos de inicio de sesión.')
                            else:
                                messages.error(request, 'Número de identificación o contraseña incorrectos')

                    else:
                        messages.error(request, 'La cuenta está inhabilitada.')

                except Usuarios.DoesNotExist:
                    messages.error(request, 'El usuario no existe')

        else:
            form = LoginForm()

        return render(request, 'empresarial/login.html', {'form': form})
# def editarIndependiente(request, numero_identificacion):
#     try:
#         empleado = Empleado.objects.get(pk=numero_identificacion)
#         formulario = IndependienteForm(instance=empleado)
#         return render(request, 'empresarial/editarIndependi.html', {"form": formulario, "empleado": empleado})
#     except Independiente.DoesNotExist:
#         messages.error(request, 'No se encontró el perfil de Independiente asociado')
#         return redirect('home')

    



    def cerrar_sesion(request):
            if request.method == 'POST':
                logout(request)
                request.session.flush()  
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error'}, status=400)

    def cerrar_sesion_redirect(request):
            logout(request)
            request.session.flush()
            return redirect('loginEmpresa') 
        
def keep_session_alive(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'Session is alive'})
    else:
        return JsonResponse({'status': 'Method not allowed'}, status=405)



class Paginas(HttpRequest):
    def home (request): 
        return render(request,'empresarial/home.html')
    def homeEmpleado (request): 
        return render(request,'empresarial/homeEmpleado.html')
    def homeEmpresa(request):
            numero_identificacion = request.session.get('numero_identificacion')
            try:
                independi = Empleado.objects.get(pk=numero_identificacion)
                return render(request, 'empresarial/homeEmpresa.html', {'independi': independi})
            except Empleado.DoesNotExist:
                messages.error(request, 'No se encontró el perfil de Empleado asociado')
                return redirect('loginEmpresa')

class GestionEmpleado(HttpRequest):
   
    def crearEmpleado(request):
        formulario = EmpleadoForm(request.POST, request.FILES)
        if formulario.is_valid():
            formula=formulario.save()
            name = formula.primer_nombre
            docu= formula.numero_identificacion
            raw_password=docu+name
            usuario = Usuarios(
                usuario=formula,
                intentos=0,
                estado_u=True,
                id_rol='Empleado General'
            )
            usuario.set_password(raw_password)  
            usuario.save()
            formulario = EmpleadoForm()
            return redirect('homeEmpleado') 
        return render(request, 'empresarial/registroEmpleado.html', {'form': formulario, 'mensaje': 'ok'})

    
    def ListarEmpleados(request,nit):

        empresa = Empresa.objects.get(pk=nit)
        get_empleados = Empleado.objects.filter(empresa=empresa)
        data = {
            'get_empleados': get_empleados,
            'empresa': empresa  
        }
        return render(request, 'empresarial/listarEmpleado.html', data)
    
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
        return render (request, 'listarEmpleado.html', { "get_empleados": emple})

class GestionarEmpresa(HttpRequest):
    def crearEmpresa(request):
        formulario = EmpresaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            formulario = EmpresaForm()
        return render(request, 'empresarial/registroEmpresa.html', {'form': formulario, 'mensaje': 'ok'})

    def ListarEmpresa(request):
        get_empresa = Empresa.objects.all()
        data = {
            'get_empresa': get_empresa
        }
        return render(request, 'empresarial/listarEmpresa.html', data)
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
    
    def eliminarEmpresa(request, nit):
        empresa=Empresa.objects.get(pk=nit)
        empresa.delete()
        empre=Empresa.objects.all() 
        return render (request, 'listarEmpresa.html', { "get_empresa": empre})
    
class CalculosGenerales(HttpRequest):
    def calcularSalario(request, numero_identificacion):
        empleado = Empleado.objects.get(pk=numero_identificacion)


        #calculo de dias trabajados
        dias_trabajados=empleado.fecha_ingreso
        dias_trabajados_anteriores,dias_trabajados_actuales,dias_antiguedad=CalculosGenerales.diasTrabajados(dias_trabajados)
       
        salario_base = empleado.salario

        transporte=CalculosGenerales.auxilioTrasnporte(salario_base)



        #caclulos de aportes seguridad sociales
        salario_base_sin_trasnpo=salario_base
        salud = salario_base_sin_trasnpo * 0.04#se le debe sumar si aplica----> comisiones+Horas, extras, Bonificaciones habituales, Recargos nocturnos.
        pension = salario_base_sin_trasnpo * 0.04#se le debe sumar si aplica----> comisiones+Horas, extras, Bonificaciones habituales, Recargos nocturnos.
        nivel_riesgo = int(empleado.nivel_riesgo)
        arl=CalculosGenerales.nivelRiesgo(salario_base,nivel_riesgo)#se le debe sumar si aplica----> comisiones+Horas, extras, Bonificaciones habituales, Recargos nocturnos.



        salario_base_transpor=salario_base+transporte
        
        cesantias,intereses_cesantias=CalculosGenerales.calculoCesantias(salario_base_transpor,dias_trabajados_actuales)
        dias_vacaciones,valor_vacaciones=CalculosGenerales.calculoVacaciones(salario_base,dias_antiguedad)
        #calculo de aportes parafiscales
        sena,icbf,cajaCompensacion=CalculosGenerales.prestacionesSociales(salario_base)

        
        calculos = Calculos(
            documento=empleado,
            salud=salud,
            pension=pension,
            arl=arl,
            transporte=transporte,
            salarioBase=salario_base,
            cajaCompensacion=cajaCompensacion,
            sena=sena,
            icbf=icbf,
            cesantias=cesantias,
            interesCesantias=intereses_cesantias,
            vacaciones=valor_vacaciones,
            dias_vacaciones=dias_vacaciones
        )
        calculos.save()
        
        context = {
            'empleado': numero_identificacion,
            'salud': salud,
            'pension': pension,
            'arl': arl,
            'transporte': transporte,
            'sena':sena,
            'ICBF':icbf,
            'CajaCompensa':cajaCompensacion,
            'cesantias':cesantias,
            'intereses_cesantias':intereses_cesantias,
            'valor_vacaciones':valor_vacaciones,
            'dias_vacaciones':dias_vacaciones
        }
        return render(request, 'empresarial/resultado_calculo.html', context)
    
    def nivelRiesgo(salario_base,nivel_riesgo):
        
        if nivel_riesgo == 1:
            arl = salario_base * 0.00522
        elif nivel_riesgo == 2:
            arl = salario_base * 0.01044
        elif nivel_riesgo == 3:
            arl = salario_base * 0.02436
        elif nivel_riesgo == 4:
            arl = salario_base * 0.04350
        elif nivel_riesgo == 5:
            arl = salario_base * 0.06960
        else:
            arl = 0  
        return (arl)
    
    def auxilioTrasnporte(salario_base):
        if salario_base >= 1300000 and salario_base <= 2600000 and salario_base>0:
            auxilio=162000
        else:
            auxilio=0
        return (auxilio)
    
    def prestacionesSociales(salario_base):
        sena=0
        icbf=0
        if salario_base >= 10000000 and salario_base>0:
            sena = salario_base * 0.02
            icbf = salario_base * 0.03
            cajaCompensacion =  salario_base *0.04
        else:
            cajaCompensacion =  salario_base *0.04
        return (sena,icbf,cajaCompensacion)
    
    def diasTrabajados(fecha_ingreso):
        # Verificar si fecha_ingreso es datetime.date y convertir a str si es necesario
        if isinstance(fecha_ingreso, date):
            fecha_ingreso = fecha_ingreso.strftime("%d-%m-%Y")
        
        # Convertir la fecha_ingreso de string a objeto datetime
        fecha_ingresada = datetime.strptime(fecha_ingreso, "%d-%m-%Y")
        
        # Obtener la fecha de hoy
        hoy = datetime.today()
        
        # Calcular la diferencia en días entre hoy y la fecha ingresada
        dias_diferencia = (hoy - fecha_ingresada).days
        antiguedad_dias = dias_diferencia
        
        # Establecer la fecha de referencia
        fecha_referencia = datetime(hoy.year, 1, 1)
        
        # Inicializar variables
        dias_trabajados_anteriores = 0
        dias_trabajados_actuales = 0
        
        # Clasificar los días trabajados
        if fecha_ingresada < fecha_referencia:
            dias_trabajados_anteriores = (fecha_referencia - fecha_ingresada).days
            dias_trabajados_actuales = dias_diferencia - dias_trabajados_anteriores
        else:
            dias_trabajados_actuales = dias_diferencia
        
        return dias_trabajados_anteriores, dias_trabajados_actuales, antiguedad_dias
    
    def calculoCesantias(salario_base_transpor,dias_trabajados_actuales):
        #Como el salario ha variado todo el tiempo, unas veces por incremento o disminución 
        # del sueldo básico y otras por efecto de horas extras, recargos nocturnos, dominicales 
        # y festivos, es preciso tomar el promedio de los 8 meses para determinar la base a utilizar 
        # para calcular las cesantías.
        #tener encuenta los ultimos salrios devengados que incluyen, horas extras,auxilio de trasnporte,
        # comisiones,recargos
        cesantias=(salario_base_transpor*dias_trabajados_actuales)/360
        interes_cesantias=(cesantias*dias_trabajados_actuales)/360
        return cesantias,interes_cesantias
        
    def calculoVacaciones(salario_base,dias_antiguedad):
        #se tiene en cuenta estos conceptoshoras extras, auxilio de transporte, comisiones y recargos,
        valor_dia=salario_base/30
        dias_vaciones=(dias_antiguedad/360)*15
        valor_vacciones=valor_dia*dias_vaciones
        return dias_vaciones,valor_vacciones



















