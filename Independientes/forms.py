
from django import forms   # type: ignore 
from .models import Independiente, DatosCalculos


class IndependienteForm(forms.ModelForm):
    class Meta:
        model = Independiente
        fields ='__all__'


class LoginForm(forms.Form):
    numero_identificacion = forms.IntegerField(label='Número de identificación')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class RecuperarContrasenaForm(forms.Form):
    numero_identificacion = forms.IntegerField(label='Número de Identificación')


class PasswordResetForm(forms.Form):
    token = forms.CharField(label='Token')
    new_password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)
    
    confirm_password = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    
class DatosCalculosForm(forms.ModelForm):
    class Meta:
        model = DatosCalculos
        fields = ['salarioBase', 'ibc', 'salud', 'pension', 'arl', 'CCF']