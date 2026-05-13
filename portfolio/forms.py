from django import forms
from .models import Projeto, Tecnologia, UnidadeCurricular, Licenciatura

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
        widgets = {
            'tecnologias': forms.CheckboxSelectMultiple(), # Facilita a seleção múltipla
        }

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'

class UnidadeCurricularForm(forms.ModelForm):
    class Meta:
        model = UnidadeCurricular
        fields = '__all__'

class LicenciaturaForm(forms.ModelForm):
    class Meta:
        model = Licenciatura
        fields = '__all__'