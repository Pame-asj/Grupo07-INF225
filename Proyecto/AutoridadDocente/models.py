
from LoginRegister.models import User
from django.db import models

class Tema(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    enunciado = models.TextField()
    opciones = models.JSONField() 
    respuesta_correcta = models.CharField(max_length=1)
    temas = models.ManyToManyField(Tema)

    def __str__(self):
        return self.enunciado

class Ensayo(models.Model):
    titulo = models.CharField(max_length=200)
    nivel = models.CharField(max_length=50, choices=User.NIVELES)
    colegio = models.CharField(max_length=100)
    temas = models.ManyToManyField(Tema,blank=True)
    preguntas = models.ManyToManyField(Pregunta,blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class RespuestaEnsayo(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Estudiante'})
    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    puntaje = models.FloatField(null=True, blank=True)  # ya calculado como porcentaje

    def total_preguntas(self):
        return self.ensayo.preguntas.count()

    def porcentaje(self):
        return self.puntaje or 0

    def __str__(self):
        return f"{self.estudiante.username} - {self.ensayo.titulo}"
    
class RespuestaPregunta(models.Model):
    respuesta_ensayo = models.ForeignKey(RespuestaEnsayo, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    alternativa_elegida = models.CharField(max_length=1)

    def es_correcta(self):
        return self.alternativa_elegida == self.pregunta.respuesta_correcta