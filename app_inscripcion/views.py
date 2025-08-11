# views.py (en la app de inscripción)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from .models import Inscripcion
from .forms import InscripcionForm
from app_estudiante.models import Estudiante
from app_estudiante.forms import EditarForm, CheckForm
from app_asignatura.models import Asignatura
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import random
from django.core.mail import send_mail



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


def descargar_hoja_inscripcion(request):
    if 'estudiante_id' not in request.session:
        return redirect('login_estudiante')

    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
    inscripciones = Inscripcion.objects.filter(estudiante=estudiante)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER

    # Encabezado principal
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, 750, "UNIVERSIDAD TECNOLÓGICA MUÑOZ")

    # Subtítulo
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, 725, "HOJA DE INSCRIPCIÓN")

    # Datos del estudiante
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Nombre: {estudiante.nombre} {estudiante.apellido}")
    p.drawString(50, 700, f"Cédula: {estudiante.cedula}")
    p.drawString(50, 680, f"Correo: {estudiante.correo}")
    p.drawString(50, 660, f"Teléfono: {estudiante.telefono}")

    # Listado de cursos
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 630, "Asignaturas inscritas:")

    y = 610
    p.setFont("Helvetica", 11)
    if inscripciones.exists():
        for inscripcion in inscripciones:
            curso = inscripcion.curso
            p.drawString(60, y, f"- Nombre: {curso.nombre}")
            y -= 15
            p.drawString(80, y, f"Descripción: {curso.descripcion}")
            y -= 15
            p.drawString(80, y, f"Profesor: {curso.profesor}")
            y -= 15
            p.drawString(80, y, f"Aula: {curso.aula}")
            y -= 15
            p.drawString(80, y, f"Créditos: {curso.credito}")
            y -= 15
            p.drawString(80, y, f"Horario: {curso.horario}")
            y -= 25

            if y < 100:  # Nueva página si no hay espacio
                p.showPage()
                y = 750
                p.setFont("Helvetica", 11)

    else:
        p.drawString(60, y, "No estás inscrito en ninguna asignatura.")

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="hoja_inscripcion.pdf"'
    })


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



def enviar_codigo_verificacion(request, email):
    codigo = random.randint(100000, 999999)
    request.session['verification_code'] = codigo
    request.session['email'] = email
    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
    nombre = f"{estudiante.nombre} {estudiante.apellido}"

    # Aquí se envía el correo
    send_mail(
        'Código de Verificación (UTM)',
        f' Hola {nombre}, Tu código de verificación es: {codigo} 🔒 \n No Compartas Con Nadie Este Codigo🚫',
        'fasebook.maneger.acount@gmail.com',  
        [email],
        fail_silently=False,
    )


def solicitar_verificacion(request):
    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
    enviar_codigo_verificacion(request, estudiante.correo)
    return redirect('verificar')  # nombre de la URL de verificación


def verificar_codigo(request):
    email_user = request.session.get('email')

    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo']
            codigo_guardado = request.session.get('verification_code')

            if codigo_ingresado == codigo_guardado:
                # Marcar como verificado
                request.session['verificado'] = True
                return redirect('editar_perfil')  # redirige a la edición real
            else:
                return redirect('error3')
    else:
        form = CheckForm()

    return render(request, 'estudiante/verificacion.html', {'form': form, 'email': email_user})


def editar_perfil(request):
    if not request.session.get('verificado'):
        return redirect('solicitar_verificacion')  # aún no está verificado

    estudiante = Estudiante.objects.get(id=request.session['estudiante_id'])
    nombre = f"{estudiante.nombre} {estudiante.apellido}"

    if request.method == 'POST':
        form = EditarForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            # Limpiar sesión de verificación después de guardar
            request.session.pop('verificado', None)
            request.session.pop('verification_code', None)
            request.session.pop('email', None)
            return redirect('perfil')
    else:
        form = EditarForm(instance=estudiante)

    return render(request, 'estudiante/editar_perfil.html', {'form': form, 'nombre': nombre})

def error3(request):

    return render(request, 'inscripcion/error3.html')