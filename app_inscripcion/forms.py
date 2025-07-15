# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Inscripcion
from app_estudiante.models import Estudiante

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['curso']

    def clean_curso(self):
        curso = self.cleaned_data['curso']
        # Obtener al estudiante de la vista
        estudiante_id = self.data.get('estudiante_id')  
        if not estudiante_id:
            raise ValidationError("El estudiante no está disponible.")
        
        estudiante = Estudiante.objects.get(id=estudiante_id)

        # Verificar si ya está inscrito en el mismo curso
        if Inscripcion.objects.filter(estudiante=estudiante, curso=curso).exists():
            raise ValidationError(f"Ya estás inscrito en el curso {curso.nombre}.")

        return curso