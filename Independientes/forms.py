
from django import forms   # type: ignore 
from .models import Independiente


class IndependienteForm(forms.ModelForm):
    class Meta:
        model = Independiente
        fields ='__all__'


class LoginForm(forms.Form):
    numero_identificacion = forms.CharField(label='Número de identificación', max_length=20)
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class RecuperarContrasenaForm(forms.Form):
    numero_identificacion = forms.CharField(max_length=100, label='Número de Identificación')

class RestablecerContrasenaForm(forms.Form):
    token = forms.CharField(label='Token', max_length=100)
    nueva_contrasena = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput)