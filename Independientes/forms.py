
from django import forms   # type: ignore 
from .models import Independiente


class IndependienteForm(forms.ModelForm):
    class Meta:
        model = Independiente
        fields ='__all__'
