
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Estudiante
from .forms import LoginForm

#VISTA PARA EL FORMULARIO DEL LOGIN
def login_estudiante(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

            try:
                estudiante = Estudiante.objects.get(correo=correo)
                if estudiante.contrasena == contrasena:  # comparo la contraseña
                    request.session['estudiante_id'] = estudiante.id
                    request.session['nombre'] = estudiante.nombre
                    apellido = estudiante.apellido
                    return redirect('home_estudiante')
                else:
                    return HttpResponse("""
    <body style="background-color: black">
        <h1 style="color: red; text-align: center; padding-top: 100px;">
            Contraseña incorrecta!
        </h1>
    </body>
""")
            except Estudiante.DoesNotExist:
                return HttpResponse("""
    <body style="background-color: black">
        <h1 style="color: red; text-align: center; padding-top: 100px;">
            Usuario no encontrado!
        </h1>
    </body>
""")
    else:
        form = LoginForm()

    return render(request, 'estudiante/login.html', {'form': form})


# vista de HOME SI EL LOGIN ES EXITOSO

def home_estudiante(request):
    if 'estudiante_id' in request.session:
        estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
        nombre = request.session['nombre'] 
        apellido = estudiante.apellido

        return render(request, 'estudiante/MENU_EST.HTML', {'nombre': nombre, 'apellido': apellido})
    else:
        return redirect('login_estudiante')
    

#vista cerrar session
def logout_estudiante(request):
    request.session.flush()
    return redirect('login_estudiante')


