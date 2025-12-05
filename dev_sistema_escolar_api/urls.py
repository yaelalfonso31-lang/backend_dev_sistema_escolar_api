from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from dev_sistema_escolar_api.views import users
from dev_sistema_escolar_api.views import alumnos
from dev_sistema_escolar_api.views import maestros
from dev_sistema_escolar_api.views import auth
from dev_sistema_escolar_api.views import eventos

urlpatterns = [
  
    #Registrar un Admin
    path('api/registro/admin/', users.AdminView.as_view()),
    #Lista de Admins
    path('api/lista-admins/', users.AdminAll.as_view()),

    #Registrar un Alumno
    path('api/registro/alumno/', alumnos.AlumnosView.as_view()),
    #Lista de Alumnos
    path('api/lista-alumnos/', alumnos.AlumnosAll.as_view()),

    #Registrar un Maestro
    path('api/registro/maestro/', maestros.MaestrosView.as_view()),
    #Lista de Maestros
    path('api/lista-maestros/', maestros.MaestrosAll.as_view()),

    #Total Users
    path('api/total-usuarios/', users.TotalUsers.as_view()),

    #Login
    path('api/login/', auth.CustomAuthToken.as_view()),

    #Logout
    path('api/logout/', auth.Logout.as_view()),

    # Eventos 
    path('api/registro/evento/', eventos.EventosView.as_view()),
    # Lista de eventos
    path('api/lista-eventos/', eventos.EventosAll.as_view()),



    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
