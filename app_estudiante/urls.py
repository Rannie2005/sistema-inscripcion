from django.urls import path
from . import views
from INCRIPCION.views import *
urlpatterns = [
    path('login/', views.login_estudiante, name='login_estudiante'),
    path('home/', views.home_estudiante, name='home_estudiante'),
    path('logout/', views.logout_estudiante, name='logout_estudiante'),
    path('error2/',views.error2, name='error2' ),
    path('error1/',views.error1, name='error1' ),
    
]
