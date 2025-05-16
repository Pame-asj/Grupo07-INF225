from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  # Heredar de AbstractUser
    ROLES = [
        ('Estudiante', 'Estudiante'),
        ('AutoridadDocente', 'AutoridadDocente'),
    ]
    
    NIVELES = [
        ('primero', '1° Medio'),
        ('segundo', '2° Medio'),
        ('tercero', '3° Medio'),
        ('cuarto', '4° Medio'),
    ]

    first_name = None
    last_name = None
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default='Estudiante')
    nivel = models.CharField(max_length=50, choices=NIVELES, null=True, blank=True)
    colegio = models.CharField(max_length=100, blank=True, default='Colegio SIP')  # Campo nuevo

    def __str__(self):
        return f"{self.username} - {self.role} - {self.nivel}"

class Ensayo(models.Model):
    titulo = models.CharField(max_length=200)
    asignatura = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50, choices=User.NIVELES)
    colegio = models.CharField(max_length=100)
    contenido = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.asignatura}"