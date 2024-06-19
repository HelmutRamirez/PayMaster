
from datetime import date, datetime
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from Empresarial.forms import EmpresaForm, EmpleadoForm,LoginForm, PasswordResetForm,RecuperarContrasenaForm,NovedadesForm
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
import re


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
                confirm_password = form.cleaned_data['confirm_password']
                
                try:
                    reset_request = PasswordResetRequest.objects.get(token=token, used=False)
                except PasswordResetRequest.DoesNotExist:
                    reset_request = None

                if new_password != confirm_password:
                    messages.error(request, 'Las contraseñas no coinciden.')
                else:
                    if len(new_password) < 6:
                        messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
                    elif not re.search(r'[A-Za-z]', new_password):
                        messages.error(request, 'La contraseña debe contener al menos una letra.')
                    elif not re.search(r'[A-Z]', new_password):
                        messages.error(request, 'La contraseña debe contener al menos una letra Mayuscula.')
                           
                    elif not re.search(r'\d', new_password):
                        messages.error(request, 'La contraseña debe contener al menos un número.')
                    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                        messages.error(request, 'La contraseña debe contener al menos un carácter especial.')
                    elif reset_request:
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
                                # return render(request, 'empresarial/listarEmpresa.html', data)
                                return redirect('ListarEmpresa')
                            elif permisos == 'Empleado General':
                                return redirect('homeEmpleado',numero_identificacion=numero_identificacion)

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
    def homeEmpleado(request,numero_identificacion): 
        
        indepe = Empleado.objects.get(pk=numero_identificacion)
        data = {'independi': indepe}
        return render(request, 'empresarial/Empleado.html', data)
    def homeEmpresa(request):
            numero_identificacion = request.session.get('numero_identificacion')
            try:
                independi = Empleado.objects.get(pk=numero_identificacion)
                return render(request, 'empresarial/homeEmpresa.html', {'independi': independi})
            except Empleado.DoesNotExist:
                messages.error(request, 'No se encontró el perfil de Empleado asociado')
                return redirect('loginEmpresa')

class GestionEmpleado(HttpRequest):
   
    def crearEmpleado(request, nit):
        empresa = get_object_or_404(Empresa, nit=nit)  # Obtén la empresa basada en el nit

        if request.method == 'POST':
            formulario = EmpleadoForm(request.POST, request.FILES)
            if formulario.is_valid():
                formula = formulario.save(commit=False)
                formula.empresa = empresa  # Asigna la empresa al empleado
                formula.save()
                raw_password = formula.primer_nombre + str(formula.numero_identificacion) + '@'
                usuario = Usuarios(
                    usuario=formula,
                    intentos=0,
                    estado_u=False,
                    id_rol='Empleado General'
                )
                usuario.set_password(raw_password)
                usuario.save()
                return redirect('ListarEmpleados', empresa.nit)
        else:
            formulario = EmpleadoForm(initial={'empresa': empresa.nit})  # Inicializa el formulario con el valor de la empresa

        return render(request, 'empresarial/registroEmpleado.html', {'form': formulario, 'mensaje': 'ok','empresa': empresa.nit})
        
    def ListarEmpleados(request,nit):

        empresa = Empresa.objects.get(pk=nit)
        get_empleados = Empleado.objects.filter(empresa=empresa)
        
        empleados_con_antiguedad = []
        for empleado in get_empleados:
            fecha_ingreso = empleado.fecha_ingreso
            dias_trabajados_anteriores, dias_trabajados_actuales, antiguedad_dias = CalculosGenerales.diasTrabajados(fecha_ingreso)
            empleados_con_antiguedad.append({
                'empleado': empleado,
                'antiguedad': antiguedad_dias
            })
        
        data = {
            'empleados_con_antiguedad': empleados_con_antiguedad,
            'empresa': empresa
        }
        
        return render(request, 'empresarial/listarEmpleado.html', data)
    

        return HttpResponseNotFound("La empresa solicitada no existe.")
    
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
        empresa=empleado.empresa.nit
        empleado.delete()
        data = {
            'empresa': empresa
        }
        return render(request, 'empresarial/listarEmpleado.html', data)
       

class GestionarEmpresa(HttpRequest):
    def crearEmpresa(request):
        formulario = EmpresaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            formulario = EmpresaForm()
            return redirect('ListarEmpresa')
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
        get_empresa=Empresa.objects.get(pk=nit)
        get_empresa.delete()
        empre=Empresa.objects.all() 
        data = {
            'get_empresa': empre
        }
        return redirect('ListarEmpresa')
    
class CalculosGenerales(HttpRequest):
    def calcularSalario(request, numero_identificacion):
        empleado = Empleado.objects.get(pk=numero_identificacion)
        empresa = empleado.empresa.nit
        # Verificar si ya existe un cálculo para este mes
        hoy = datetime.now()
        mes_actual = hoy.month
        anio_actual = hoy.year
        
        existe_calculo = Calculos.objects.filter(
            documento=empleado,
            fecha_calculos__year=anio_actual,
            fecha_calculos__month=mes_actual
        ).exists()
        
        if existe_calculo:
            mensaje = "Ya se ha calculado la nómina para este mes."
            response = redirect('ListarEmpleados', nit=empleado.empresa.nit)
            
            return response
        
        # Si no existe el cálculo, procedemos a realizarlo
        dias_trabajados = empleado.fecha_ingreso
        dias_trabajados_anteriores, dias_trabajados_actuales, dias_antiguedad = CalculosGenerales.diasTrabajados(dias_trabajados)
        salario_base = empleado.salario
        transporte = CalculosGenerales.auxilioTrasnporte(salario_base)
        salario_base_transpor = salario_base + transporte
       
        salario_base_transpor=salario_base+transporte

        #caclulos de aportes seguridad sociales
        salario_base_sin_trasnpo=salario_base
        salud = salario_base_sin_trasnpo * 0.04
        salud_empleador=salario_base_sin_trasnpo * 0.085#se le debe sumar si aplica----> comisiones+Horas, extras, Bonificaciones habituales, Recargos nocturnos.
        pension = salario_base_sin_trasnpo * 0.04
        pension_empleador = salario_base_sin_trasnpo * 0.12
        #se le debe sumar si aplica----> comisiones+Horas, extras, Bonificaciones habituales, Recargos nocturnos.
        nivel_riesgo = int(empleado.nivel_riesgo)
        arl=CalculosGenerales.nivelRiesgo(salario_base,nivel_riesgo)#se le debe sumar si aplica----> comisiones+Horas, extras, Bonificaciones habituales, Recargos nocturnos.

        #calculos de novedades
        horas_extras=CalculosGenerales.horasExtras(salario_base,empleado)
        horas_extras_diurnas = horas_extras['diurna']
        horas_extras_nocturnas = horas_extras['nocturna']
        horas_extras_diurnas_festivas = horas_extras['diurna_festiva']
        horas_extras_nocturnas_festivas = horas_extras['nocturna_festiva']
        recargo1=0
        recargo2=0
        recargo3=0
        
        cesantias,intereses_cesantias=CalculosGenerales.calculoCesantias(salario_base_transpor,dias_trabajados_actuales)
        dias_vacaciones,valor_vacaciones=CalculosGenerales.calculoVacaciones(salario_base,dias_antiguedad)
        #calculo de aportes parafiscales
        sena,icbf,cajaCompensacion=CalculosGenerales.prestacionesSociales(salario_base)

        
        # Guardar el cálculo en la base de datos
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
            antiguedad=dias_antiguedad,
            cesantias=cesantias,
            interesCesantias=intereses_cesantias,
            vacaciones=valor_vacaciones,
            dias_vacaciones=dias_vacaciones,
            fecha_calculos=hoy , # Se guarda la fecha actual como fecha de cálculo
            HorasExDiu=horas_extras_diurnas,
            HorasExNoc=horas_extras_nocturnas,
            HorasExFestivaDiu=horas_extras_diurnas_festivas,
            HorasExFestivaNoc=horas_extras_nocturnas_festivas,
            recargoDiuFes=recargo1,
            recargoNoc=recargo2,
            recargoNocFest=recargo3,
            salud_empeador=salud_empleador,
            pension_empleador=pension_empleador,
            
            
        )
        calculos.save()
        
        # Generar el contexto para mostrar los resultados
        
        total_valor_horas_extras = sum(horas_extras.values())
        salario_total = transporte + total_valor_horas_extras + salario_base_transpor
        
        context = {
            'calculos':calculos,
            'empresa': empresa,
            'empleado': numero_identificacion,
            'salud': salud,
            'pension': pension,
            'arl': arl,
            'transporte': transporte,
            'sena': sena,
            'ICBF': icbf,
            'CajaCompensa': cajaCompensacion,
            'cesantias': cesantias,
            'intereses_cesantias': intereses_cesantias,
            'valor_vacaciones': valor_vacaciones,
            'antiguedad':dias_antiguedad,
            'dias_vacaciones': dias_vacaciones,
            'valor_horas_extras': horas_extras,
            'salario_total': salario_total,
            'salud_empeador':salud_empleador,
            'pension_empleador':pension_empleador,
            'dias_antiguedad':dias_antiguedad,
            'dias_trabajados':dias_trabajados
        }
        
        return render(request, 'empresarial/resultado_calculo.html', context)
    
    def horasExtras(salario, empleado):
        # Obtener el año y mes actual
        año_actual = timezone.now().year
        mes_actual = timezone.now().month
        
        # Consultar las horas extras registradas para el empleado en el mes actual
        horas_extras = Novedades.objects.filter(
            empleado=empleado,
            fecha_novedad__year=año_actual,
            fecha_novedad__month=mes_actual
        ).aggregate(
            total_horas_diu=Sum('HorasExDiu'),
            total_horas_noc=Sum('HorasExNoc'),
            total_horas_diu_fest=Sum('HorasExFestivaDiu'),
            total_horas_noc_fest=Sum('HorasExFestivaNoc')
        )
        salario=(salario/235)
        # Calcular el valor de las horas extras usando los porcentajes establecidos
        valor_horas_extras = {
            'diurna': (salario * 1.25) * (horas_extras['total_horas_diu'] or 0),
            'nocturna': (salario * 1.75) * (horas_extras['total_horas_noc'] or 0),
            'diurna_festiva': (salario * 2) * (horas_extras['total_horas_diu_fest'] or 0),
            'nocturna_festiva': (salario * 2.5) * (horas_extras['total_horas_noc_fest'] or 0)
        }
        
        return valor_horas_extras
 
    
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
       
        if dias_diferencia >0:
            dias_diferencia -=1
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
        
        return dias_trabajados_anteriores, dias_trabajados_actuales, dias_diferencia
    
    def calculoCesantias(salario_base_transpor,dias_trabajados_actuales):
        #Como el salario ha variado todo el tiempo, unas veces por incremento o disminución 
        # del sueldo básico y otras por efecto de horas extras, recargos nocturnos, dominicales 
        # y festivos, es preciso tomar el promedio de los 8 meses para determinar la base a utilizar 
        # para calcular las cesantías.
        #tener encuenta los ultimos salrios devengados que incluyen, horas extras,auxilio de trasnporte,
        # comisiones,recargos
        cesantias=(salario_base_transpor*dias_trabajados_actuales)/360
        interes_cesantias=(cesantias*dias_trabajados_actuales*0.12)/360
        return cesantias,interes_cesantias
        
    def calculoVacaciones(salario_base,dias_antiguedad):
        #se tiene en cuenta estos conceptoshoras extras, auxilio de transporte, comisiones y recargos,
        valor_dia=salario_base/30
        dias_vaciones=(dias_antiguedad/360)*15
        valor_vacciones=valor_dia*dias_vaciones
        return dias_vaciones,valor_vacciones
        
    def registroNovedades(request, numero_identificacion):
        empleado = get_object_or_404(Empleado, pk=numero_identificacion)
        if request.method == 'POST':
            formularioNov = NovedadesForm(request.POST)
            if formularioNov.is_valid():
                novedad = formularioNov.save(commit=False)
                novedad.empleado = empleado
                novedad.fecha_novedad = timezone.now()
                
                # Obtener límite máximo de horas permitido
                limite_maximo_horas = 48
                
                # Calcular la suma total de horas considerando los campos llenados en el formulario
                suma_total = Novedades.objects.filter(
                    empleado=empleado,
                    fecha_novedad__year=timezone.now().year,
                    fecha_novedad__month=timezone.now().month
                ).aggregate(
                    total_horas=Sum('HorasExDiu') + Sum('HorasExNoc') +
                                Sum('HorasExFestivaNoc') + Sum('HorasExFestivaDiu')
                )['total_horas'] or 0
                
                # Verificar si la suma total más el nuevo registro excede el límite máximo de horas
                if (suma_total or 0) + (novedad.HorasExDiu or 0) + (novedad.HorasExNoc or 0) + \
                (novedad.HorasExFestivaNoc or 0) + (novedad.HorasExFestivaDiu or 0) > limite_maximo_horas:
                    error_message = f"La suma de horas excede el límite máximo permitido de {limite_maximo_horas} horas en el mes."
                
                    return render(request, 'empresarial/novedadesForm.html', {'formularioNov': formularioNov, 'error_message': error_message,'empleado':empleado})
                novedad.save()
                    
                return redirect('ListarEmpleados', nit=empleado.empresa.nit)
        else:
            formularioNov = NovedadesForm()
        
        return render(request, 'empresarial/novedadesForm.html', {'formularioNov': formularioNov,'empleado': empleado})

    
    def HistorialNomina(request,documento,fecha ):
     
        empleado = get_object_or_404(Empleado, pk=documento)
    
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()

        calculos_empleado = Calculos.objects.filter(documento=empleado, fecha_calculos=fecha)

        empresa = empleado.empresa.nit
        calculo = calculos_empleado.first()
            

        salario_total = (
            (calculo.salarioBase if calculo.salarioBase else 0.0) +
            (calculo.transporte if calculo.transporte else 0.0) +
            (calculo.HorasExDiu if calculo.HorasExDiu else 0.0) +
            (calculo.HorasExNoc if calculo.HorasExNoc else 0.0) +
            (calculo.HorasExFestivaDiu if calculo.HorasExFestivaDiu else 0.0) +
            (calculo.HorasExFestivaNoc if calculo.HorasExFestivaNoc else 0.0) +
            (calculo.recargoDiuFes if calculo.recargoDiuFes else 0.0) +
            (calculo.recargoNoc if calculo.recargoNoc else 0.0) +
            (calculo.recargoNocFest if calculo.recargoNocFest else 0.0) -
            ((calculo.salud if calculo.salud else 0.0) + (calculo.pension if calculo.pension else 0.0))
        )

         
        context = {
                'empresa': empresa,
                'fecha': calculo.fecha_calculos,
                'empleado': empleado,
                'salud': calculo.salud,
                'pension': calculo.pension,
                'arl': calculo.arl,
                'transporte': calculo.transporte,
                'sena': calculo.sena,
                'ICBF': calculo.icbf,
                'CajaCompensa': calculo.cajaCompensacion,
                'cesantias': calculo.cesantias,
                'intereses_cesantias': calculo.interesCesantias,
                'valor_vacaciones': calculo.vacaciones,
                'dias_vacaciones': calculo.dias_vacaciones,
                'HorasExDiu': calculo.HorasExDiu,
                'HorasExNoc': calculo.HorasExNoc,
                'HorasExFestivaDiu': calculo.HorasExFestivaDiu,
                'HorasExFestivaNoc': calculo.HorasExFestivaNoc,
                'recargoDiuFes': calculo.recargoDiuFes,
                'recargoNoc': calculo.recargoNoc,
                'recargoNocFest': calculo.recargoNocFest,
                'salario_total': salario_total,
                'calculo':calculo
            }
                        
        return render(request, 'empresarial/historialNomina.html', context)
       

    def obtener_todos_los_calculos(request,numero_identificacion):
        empleado = get_object_or_404(Empleado, pk=numero_identificacion)
        todos_los_calculos = Calculos.objects.filter(documento=empleado)
        
        # Preparar el contexto
        context = {
            'calculos': todos_los_calculos,
            'empleado':empleado
        }
        
        # Renderizar la plantilla con el contexto
        return render(request, 'empresarial/HistoricoGeneral.html', context)


