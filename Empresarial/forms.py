from django import forms   # type: ignore 
from .models import Empleado, Usuarios, Empresa, Calculos, Novedades

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
        
class CalculosForm(forms.ModelForm):
    class Meta:
        model = Calculos
        fields = ['documento', 'salarioBase', 'nivel_riesgo']

class NovedadesForm(forms.ModelForm):
    class Meta:
        model = Novedades
        fields = '__all__'
