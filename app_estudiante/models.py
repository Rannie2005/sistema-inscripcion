from django.db import models
from django.contrib.auth.hashers import make_password, check_password
#asta haora todo esta bien

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=15, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    contrasena = models.CharField(max_length=100)  # aquí se guarda en texto, pero deberías cifrarla si es posible
    

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    