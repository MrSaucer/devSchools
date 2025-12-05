from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'  # Inclui todos os campos do Model
        # Alternativa: fields = ['nome', 'descricao', 'carga_horaria']