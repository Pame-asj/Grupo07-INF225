
from django import forms
from .models import Ensayo, Pregunta, Tema

class EnsayoForm(forms.ModelForm):
    class Meta:
        model = Ensayo
        fields = ['titulo', 'nivel', 'colegio', 'temas', 'preguntas']
        widgets = {
            'temas': forms.CheckboxSelectMultiple,
            'preguntas': forms.CheckboxSelectMultiple,
        }

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['enunciado', 'opciones', 'respuesta_correcta', 'temas']
        widgets = {
            'temas': forms.CheckboxSelectMultiple,
        }
