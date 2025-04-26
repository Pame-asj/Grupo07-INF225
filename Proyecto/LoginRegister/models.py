from django.db import models

class User(models.Model):
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

    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Cifrado recomendado
    role = models.CharField(max_length=50, choices=ROLES, default='Estudiante')
    nivel = models.CharField(max_length=50, choices=NIVELES, null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return f"{self.username} - {self.role} - {self.nivel}"
