
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
    temas = models.ManyToManyField(Tema)
    preguntas = models.ManyToManyField(Pregunta)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
