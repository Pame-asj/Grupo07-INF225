from django import forms
from .models import Ensayo, Pregunta, Tema, Tag
from django.utils.text import slugify


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = "__all__"


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]  # el slug se autogenera, no se expone

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return name

    def _build_unique_slug(self, base_text: str) -> str:
        """
        Genera un slug único a partir de base_text. Si existe, agrega sufijos -2, -3, ...
        """
        base_slug = slugify(base_text) or "tag"
        slug = base_slug
        i = 2
        from .models import Tag  # import local para evitar ciclos
        while Tag.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{i}"
            i += 1
        return slug

    def save(self, commit=True):
        tag = super().save(commit=False)
        # Siempre autogenerar/normalizar slug a partir del name
        tag.slug = self._build_unique_slug(tag.name)
        if commit:
            tag.save()
        return tag


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
        # 👉 Incluye los nuevos campos:
        fields = ['enunciado', 'respuesta_correcta', 'temas', 'is_free', 'tags']
        widgets = {
            'temas': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple,
        }
        labels = {
            'enunciado': 'Enunciado de la pregunta',
            'temas': 'Etiquetas (Temas)',
            'is_free': 'Pregunta libre',
            'tags': 'Etiquetas',
        }

    def save(self, commit=True):
        pregunta = super().save(commit=False)
        # Persistimos las alternativas en el JSONField del modelo
        pregunta.opciones = {
            'A': self.cleaned_data['opcion_A'],
            'B': self.cleaned_data['opcion_B'],
            'C': self.cleaned_data['opcion_C'],
            'D': self.cleaned_data['opcion_D'],
        }
        if commit:
            pregunta.save()
            self.save_m2m()

            # Si es libre y NO seleccionaron tags, generamos tags desde los Temas elegidos
            if self.cleaned_data.get("is_free"):
                tags = self.cleaned_data.get("tags")
                temas = self.cleaned_data.get("temas")
                if (not tags or tags.count() == 0) and temas and temas.count() > 0:
                    for tema in temas:
                        tag, _ = Tag.objects.get_or_create(
                            slug=slugify(tema.nombre),
                            defaults={"name": tema.nombre}
                        )
                        pregunta.tags.add(tag)
        return pregunta


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-cargar las opciones si ya existen (editar)
        if self.instance and self.instance.opciones:
            self.fields['opcion_A'].initial = self.instance.opciones.get('A', '')
            self.fields['opcion_B'].initial = self.instance.opciones.get('B', '')
            self.fields['opcion_C'].initial = self.instance.opciones.get('C', '')
            self.fields['opcion_D'].initial = self.instance.opciones.get('D', '')

    def clean(self):
        cleaned = super().clean()
        is_free = cleaned.get("is_free")
        tags = cleaned.get("tags")
        temas = cleaned.get("temas")

        # Si es libre, aceptamos "Etiquetas específicas (tags)" O "Temas" como respaldo.
        if is_free:
            no_tags = (not tags or tags.count() == 0)
            no_temas = (not temas or temas.count() == 0)
            if no_tags and no_temas:
                raise forms.ValidationError(
                    "Las preguntas libres requieren al menos una etiqueta o tema."
                )
        return cleaned
