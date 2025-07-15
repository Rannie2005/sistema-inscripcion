# views.py (en la app de inscripción)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Inscripcion
from .forms import InscripcionForm
from app_estudiante.models import Estudiante
from app_estudiante.forms import EditarForm
from app_asignatura.models import Asignatura


#vista para inscribirse
def inscribir_curso(request):
    if 'estudiante_id' not in request.session: # para ver si el estudiante no esta en session
        return redirect('login_estudiante')

    # Obtener el estudiante de la sesión
    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])#aqui obtenemos el id del estudiante en session
    nombre = f"{estudiante.nombre} {estudiante.apellido}" #aqui una variable para el contexto del html

    # solo obtener los cursos disponibles, evitanda donde ya esta inscrito
    
    inscripciones = Inscripcion.objects.filter(estudiante=estudiante)
    cursos_inscritos = [inscripcion.curso for inscripcion in inscripciones]
    cursos_disponibles = Asignatura.objects.exclude(id__in=[curso.id for curso in cursos_inscritos])

    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        form.fields['curso'].queryset = cursos_disponibles  # Limitar los cursos disponibles

        # Pasar el estudiante_id al formulario
        form.data = form.data.copy()  # Hacer una copia de los datos
        form.data['estudiante_id'] = estudiante.id

        if form.is_valid():
            # Asignar estudiante antes de guardar la inscripción
            inscripcion = form.save(commit=False)
            inscripcion.estudiante = estudiante  # Asignar estudiante manualmente
            inscripcion.save()
            return redirect('mis_inscripciones')  # Redirige a la página de inscripciones

    else:
        form = InscripcionForm()

    return render(request, 'inscripcion/inscribir.html', {'form': form, 'nombre': nombre})


#vista para visualizar la incripciones
def mis_inscripciones(request):
    if 'estudiante_id' not in request.session:
        return redirect('login_estudiante')

    estudiante_id = request.session['estudiante_id']
    inscripciones = Inscripcion.objects.filter(estudiante_id=estudiante_id)
    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
    name = estudiante.nombre
    apellido = estudiante.apellido
    nombre = name+' '+apellido
    return render(request, 'inscripcion/mis_inscripciones.html', {'inscripciones': inscripciones, 'nombre':nombre})


def eliminar_inscripcion(request, inscripcion_id):
    if 'estudiante_id' not in request.session:
        return redirect('login_estudiante')

    estudiante_id = request.session['estudiante_id']
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
    name = estudiante.nombre
    apellido = estudiante.apellido
    nombre = name+' '+apellido

    if inscripcion.estudiante.id != estudiante_id:
        return HttpResponseForbidden("No tienes permiso para eliminar esta inscripción.")

    if request.method == 'POST':
        inscripcion.delete()
        return redirect('mis_inscripciones')

    return render(request, 'inscripcion/confirmar_eliminacion.html', {'inscripcion': inscripcion, 'nombre':nombre})


def lista_para_eliminar(request):
    if 'estudiante_id' not in request.session:
        return redirect('login_estudiante')

    estudiante_id = request.session['estudiante_id']
    inscripciones = Inscripcion.objects.filter(estudiante_id=estudiante_id)
    estudiante = Estudiante.objects.get(id = request.session['estudiante_id'])
    name = estudiante.nombre
    apellido = estudiante.apellido
    nombre = name+' '+apellido

    return render(request, 'inscripcion/eliminar.html', {'inscripciones': inscripciones, 'nombre': nombre})


def perfil(request):
    if 'estudiante_id' in request.session:
        estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
        nombre = estudiante.nombre
        apellido = estudiante.apellido
        correo = estudiante.correo
        cedula = estudiante.cedula
        telefono = estudiante.telefono
        return render(request, 'estudiante/perfil.html', {'nombre': nombre, 'apellido': apellido, 'correo': correo, 'cedula': cedula, 'telefono': telefono} )

    else:
        return redirect('login_estudiante')



def editar_perfil(request):
    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
    name = estudiante.nombre
    apellido = estudiante.apellido
    nombre = name+' '+apellido

    if request.method == 'POST':
        form = EditarForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Ajusta el nombre según tu URL
    else:
        form = EditarForm(instance=estudiante)

    return render(request, 'estudiante/editar_perfil.html', {'form': form, 'nombre': nombre})