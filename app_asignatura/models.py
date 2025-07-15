from django.db import models

# CREAMOS LA TABLA SQL CURSO
class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.CharField(max_length=100)
    aula = models.CharField(max_length=50, default='Aula 1') 
    credito = models.PositiveIntegerField(default=6)
    horario = models.CharField(max_length=100)
    cupo_maximo = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f'{self.nombre}  ({self.horario})'