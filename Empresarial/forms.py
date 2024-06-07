
from django import forms   # type: ignore 
from .models import Empleado,Usuarios,Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'