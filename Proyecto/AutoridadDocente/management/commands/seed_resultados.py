from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
import random

from LoginRegister.models import User
from AutoridadDocente.models import (
    Pregunta, Ensayo, RespuestaEnsayo, RespuestaPregunta, Tag, Tema
)

class Command(BaseCommand):
    help = "Genera resultados de prueba para gráficos por etiquetas."

    def add_arguments(self, parser):
        parser.add_argument('--intentos', type=int, default=20, help='Cantidad de intentos (Respuestas de ensayo)')
        parser.add_argument('--acierto', type=int, default=60, help='Porcentaje de acierto simulado (0-100)')

    @transaction.atomic
    def handle(self, *args, **opts):
        intentos = opts['intentos']
        acierto = max(0, min(100, opts['acierto']))

        # Asegurar un usuario estudiante
        estudiante, _ = User.objects.get_or_create(
            username='estudiante_demo',
            defaults={
                'role': 'Estudiante',
                'email': 'demo@example.com',
                'full_name': 'Estudiante Demo',
            }
        )

        # Asegurar un ensayo con preguntas
        preguntas = list(Pregunta.objects.all())
        if not preguntas:
            # Si no hay preguntas, crear mínimas con temas/tags
            tema, _ = Tema.objects.get_or_create(nombre='Demo')
            tag, _ = Tag.objects.get_or_create(name='Etiqueta Demo', slug='etiqueta-demo')

            for i in range(1, 6):
                p = Pregunta.objects.create(
                    enunciado=f"Pregunta demo {i}",
                    opciones={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    respuesta_correcta=random.choice(['A', 'B', 'C', 'D'])
                )
                p.temas.add(tema)
                p.tags.add(tag)
            preguntas = list(Pregunta.objects.all())

        ensayo, _ = Ensayo.objects.get_or_create(
            titulo='Ensayo de prueba',
            defaults={'nivel': '1° Medio', 'colegio': 'Colegio Demo'}
        )
        ensayo.preguntas.set(preguntas)

        creados = 0
        for n in range(intentos):
            re = RespuestaEnsayo.objects.create(
                estudiante=estudiante,
                ensayo=ensayo,
                fecha_respuesta=timezone.now(),
                puntaje=0.0
            )
            correctas = 0
            for preg in preguntas:
                # decidir si acierta según porcentaje
                corr = random.random() < (acierto / 100.0)
                alternativa = preg.respuesta_correcta if corr else random.choice([x for x in ['A','B','C','D'] if x != preg.respuesta_correcta])
                RespuestaPregunta.objects.create(
                    respuesta_ensayo=re,
                    pregunta=preg,
                    alternativa_elegida=alternativa
                )
                if corr:
                    correctas += 1
            re.puntaje = round(100.0 * correctas / max(len(preguntas),1), 2)
            re.save()
            creados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Sembrados {creados} intentos para {estudiante.username} con acierto ~{acierto}%"
        ))
