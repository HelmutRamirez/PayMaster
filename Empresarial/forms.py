
from django import forms   # type: ignore 
from .models import Empleado,Usuarios,Empresa

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

class UsuariosForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'