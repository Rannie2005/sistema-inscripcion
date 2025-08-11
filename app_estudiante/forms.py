# forms.py
from django import forms
from .models import Estudiante
from django.contrib.auth.hashers import make_password

class LoginForm(forms.Form):
    correo = forms.CharField(label='Correo', max_length=50)
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class CheckForm(forms.Form):
    codigo = forms.IntegerField(label="Codigo De Verificacion") 


class EditarForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Estudiante
        fields = ['correo', 'telefono', 'contrasena']  # Campos en el formulario

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if contrasena:
            #si hay algo
            return contrasena
        return self.instance.contrasena  # Si no cambió la contraseña, conservar la anterior
        