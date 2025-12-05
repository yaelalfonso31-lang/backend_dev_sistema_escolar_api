from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import *
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin "+self.first_name+" "+self.last_name
    
class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=10, null=False, blank=False, default=" indefinida")
    curp = models.CharField(max_length=18, null=False, blank=False, default="indefinida")
    rfc = models.CharField(max_length=13, null=True, blank=True, default=None)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    edad = models.IntegerField(null=False, blank=False)
    telefono = models.CharField(max_length=10, null=True, blank=True, default=None)
    ocupacion = models.CharField(max_length=50, null=True, blank=True, default=None)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.CharField(max_length=10, null=False, blank=False, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    rfc = models.CharField(max_length=13, null=False, blank=False, unique=True)
    telefono = models.CharField(max_length=10, null=True, blank=True, default=None)
    cubiculo = models.CharField(max_length=50, null=True, blank=True, default=None)
    area_investigacion = models.CharField(max_length=100, null=True, blank=True, default=None)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Eventos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False, blank=False)
    tipo = models.CharField(max_length=50, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    hora_inicio = models.CharField(max_length=20, null=False, blank=False)
    hora_fin = models.CharField(max_length=20, null=False, blank=False)
    lugar = models.CharField(max_length=255, null=False, blank=False)
    publico = models.TextField(null=False, blank=False) 
    programa = models.CharField(max_length=255, null=True, blank=True)
    responsable = models.CharField(max_length=20, null=False, blank=False) 
    descripcion = models.TextField(null=True, blank=True)
    cupo = models.IntegerField(null=False, blank=False)
    
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre