from django.db import models
from django.core.exceptions import ValidationError
from app_estudiante.models import Estudiante
from app_asignatura.models import Asignatura


# TABLA INSCRIPCIÓN
class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.correo} inscrito en {self.curso.nombre}"

    @property
    def curso_nombre(self):
        return self.curso.nombre

    @property
    def profesor(self):
        return self.curso.profesor

    @property
    def horario(self):
        return self.curso.horario

    
def clean(self):
    # Evitar gradar si faltan datos
    if not self.estudiante_id or not self.curso_id:
        return

    conflicto = Inscripcion.objects.filter(
        estudiante=self.estudiante,
        curso__horario=self.curso.horario
    ).exclude(pk=self.pk)

    if conflicto.exists():
        raise ValidationError(
            f"Ya estás inscrito en otra asignatura en el horario {self.curso.horario}."
        )


    #Llama a la validación cada vez que se guarda el registro
    def save(self, *args, **kwargs):
        self.clean()# Ejecuta validaciones personalizadas
        super().save(*args, **kwargs) # Guardado estándar de Django
