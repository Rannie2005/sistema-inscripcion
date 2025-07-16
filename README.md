# Sistema de Inscripción
¡Bienvenido al Sistema de Gestión de Inscripciones!
Este proyecto está diseñado para administrar el proceso de inscripción de materias en una universidad, garantizando seguridad y facilidad de uso tanto para estudiantes como para administradores.


# Características Principales
## 👨‍🎓 Para Estudiantes
Acceso controlado: Solo los estudiantes registrados en la base de datos pueden iniciar sesión (no hay registro público).

Gestión de perfil:

Ver y editar información personal.

Cambiar contraseña y correo electrónico.

Inscripción académica:

Ver materias disponibles.

Inscribirse en asignaturas.

Visualizar materias inscritas.

Retirar (eliminar) materias.

Sesión segura: Cierre de sesión protegido.


## 👨‍💼 Para Administradores (Django Admin)
Gestión de estudiantes:

Añadir nuevos estudiantes manualmente (sin autoregistro).

Actualizar o eliminar registros existentes.

Control de materias:

Crear, editar o eliminar asignaturas.

Asignar horarios y requisitos.


## 🖥️ Interfaz Responsiva

Diseño adaptado para móviles, tablets y laptops.

Navegación intuitiva y accesible.


## 🛠️ Tecnologías Utilizadas
Backend: Django (Python) + PostgreSQL.

Frontend: HTML y CSS.

Autenticación: Sistema personalizado basado en la base de datos.



# 🚀 Cómo Clonar y Ejecutar (Python 3.11)

## 1. Verifica tu versión de Python
   python --version  # Debe mostrar 3.11.x
   
## 2. Clona el repositorio
   git clone https://github.com/Rannie2005/sistema-inscripcion.git
   cd sistema-inscripcion

## 3. Crea y activa el entorno virtual (Python 3.11)
   python3.11 -m venv venv
## Windows:
.\venv\Scripts\activate
## Linux/Mac:
source venv/bin/activate

## 4. Instala dependencias exactas para Python 3.11
   pip install -r requirements.txt

## 5. Configuración PostgreSQL
   Crea la base de datos SOFTWARE_INSCRIPCION

   Copia y configura .env:
   cp .env.example .env
   
## 6. Migraciones e inicio
   python manage.py migrate
   python manage.py runserver
   ## 🔗 Accede: http://localhost:8000

   ## 7. Inicia Session con:
   USER: raniel@utm.edu.do
   PASSWORD: 1234utm

   USER: vielko@utm.edu.do
   PASSWORD: 1234utm

   USER: sara@utm.edu.do
   PASSWORD: 1234utm


## 8. 🐍 Especificaciones Técnicas
Python 3.11 (requerido)

Entorno virtual: Creado específicamente con 3.11

Django: Optimizado para esta versión

Psycopg2: Compilado para Python 3.11


## 📸 Capturas de Pantalla 
<img width="1351" height="596" alt="image" src="https://github.com/user-attachments/assets/a4947b1a-ae74-4328-bad0-5a94e8d284f0" />
<img width="1365" height="599" alt="image" src="https://github.com/user-attachments/assets/9a322d5c-4767-4eee-bd8f-9c58f30699c0" />
<img width="1365" height="599" alt="image" src="https://github.com/user-attachments/assets/2c2af518-799d-4fc5-a099-83e759a65af8" />
<img width="1365" height="597" alt="image" src="https://github.com/user-attachments/assets/481f5c49-cb9a-4241-9fb1-80394c424983" />
<img width="1365" height="595" alt="image" src="https://github.com/user-attachments/assets/f963fcff-f75a-4050-ae2f-6226f7ea573b" />
<img width="1362" height="599" alt="image" src="https://github.com/user-attachments/assets/6751d954-2a1f-4bca-8847-d6758e53b8bd" />




## Para contribuir o reportar issues, visita el repositorio.
📧 Contacto: raniel.ant0880@gmail.com


## 📜 Licencia
MIT License © Ranniel Muñoz.
   

   
   
