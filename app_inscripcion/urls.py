from django.urls import path
from . import views

urlpatterns = [
    path('nueva/', views.inscribir_curso, name='inscribir_curso'),
    path('ver/', views.mis_inscripciones, name='mis_inscripciones'),
    path('eliminar/', views.lista_para_eliminar, name='lista_para_eliminar'),
    path('eliminar/<int:inscripcion_id>/', views.eliminar_inscripcion, name='eliminar_inscripcion'),
    path('perfil/',views.perfil, name='perfil' ),
    path('editar/',views.editar_perfil, name='editar_perfil' ),
]