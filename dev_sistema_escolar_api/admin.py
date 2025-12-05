from django.contrib import admin
from django.utils.html import format_html
from dev_sistema_escolar_api.models import *
from .models import Administradores, Alumnos, Maestros

@admin.register(Administradores)
@admin.register(Alumnos)
@admin.register(Maestros)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'creation', 'update')
    search_fields = ('user__username', 'user__email', 'user_first_name', 'user_last_name')