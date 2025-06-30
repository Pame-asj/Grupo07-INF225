
from django import forms
from .models import Ensayo, Pregunta, Tema


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nombre']

class EnsayoForm(forms.ModelForm):
    nuevo_tema = forms.CharField(
        max_length=100,
        required=False,
        label="Agregar nuevo tema (opcional)"
    )
    class Meta:
        model = Ensayo
        fields = ['titulo', 'nivel', 'colegio', 'temas', 'preguntas', 'nuevo_tema']
        widgets = {
            'temas': forms.CheckboxSelectMultiple,
            'preguntas': forms.CheckboxSelectMultiple,
        }

class PreguntaForm(forms.ModelForm):
    OPCIONES_CHOICES = [
        ('A', 'Opción A'),
        ('B', 'Opción B'),
        ('C', 'Opción C'),
        ('D', 'Opción D'),
    ]

    opcion_A = forms.CharField(label="Opción A")
    opcion_B = forms.CharField(label="Opción B")
    opcion_C = forms.CharField(label="Opción C")
    opcion_D = forms.CharField(label="Opción D")
    respuesta_correcta = forms.ChoiceField(choices=OPCIONES_CHOICES, label="Respuesta correcta")

    class Meta:
        model = Pregunta
        fields = ['enunciado', 'respuesta_correcta', 'temas']
        widgets = {
            'temas': forms.CheckboxSelectMultiple,
        }
        labels = {
            'enunciado': 'Enunciado de la pregunta',
            'temas': 'Temas relacionados',
        }

    def save(self, commit=True):
        pregunta = super().save(commit=False)
        pregunta.opciones = {
            'A': self.cleaned_data['opcion_A'],
            'B': self.cleaned_data['opcion_B'],
            'C': self.cleaned_data['opcion_C'],
            'D': self.cleaned_data['opcion_D'],
        }
        if commit:
            pregunta.save()
            self.save_m2m()
        return pregunta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.opciones:
            self.fields['opcion_A'].initial = self.instance.opciones.get('A', '')
            self.fields['opcion_B'].initial = self.instance.opciones.get('B', '')
            self.fields['opcion_C'].initial = self.instance.opciones.get('C', '')
            self.fields['opcion_D'].initial = self.instance.opciones.get('D', '')

