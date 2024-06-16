
from django import forms   # type: ignore 
from .models import Empleado,Usuarios,Empresa, Calculos, Novedades

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields ='__all__'
        
        
        # ['numero_identificacion', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'estado_civil']

    # def __init__(self, *args, **kwargs):
    #     super(EmpleadoForm, self).__init__(*args, **kwargs)
    #     readonly_fields = ['numero_identificacion', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']
    #     for filtro in self.fields:
    #         if filtro in readonly_fields:
    #             self.fields[filtro].widget.attrs['readonly'] = True

class LoginForm(forms.Form):
    numero_identificacion = forms.IntegerField(label='Número de identificación')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class RecuperarContrasenaForm(forms.Form):
    numero_identificacion = forms.IntegerField(label='Número de Identificación')


class PasswordResetForm(forms.Form):
    token = forms.CharField(label='Token', max_length=255)
    new_password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
