from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from dev_sistema_escolar_api.serializers import *
from dev_sistema_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import json


class EventosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        eventos = Eventos.objects.all().order_by("id")
        lista = EventoSerializer(eventos, many=True).data
        es_alumno = request.user.groups.filter(name='alumno').exists()
        es_maestro = request.user.groups.filter(name='maestro').exists()
        lista_final = []
        # Procesar la lista antes de enviarla
        for evento in lista:
            if evento["publico"]:
                try:
                    evento["publico"] = json.loads(evento["publico"])
                except:
                    evento["publico"] = []
            audiencia = evento["publico"]
            # 2. FILTRO PARA ALUMNOS
            if es_alumno:
                if "Estudiantes" not in audiencia and "Público general" not in audiencia:
                    continue 
            
            # 3. FILTRO PARA MAESTROS (NUEVO)
            if es_maestro:
                if "Profesores" not in audiencia and "Público general" not in audiencia:
                    continue

            resp_valor = evento["responsable"]
            evento["rol_responsable"] = "Desconocido"

            if resp_valor:
                try:
                    tipo, id_real = resp_valor.split("-")
                    id_real = int(id_real)
                    if tipo == "M":
                        maestro = Maestros.objects.get(id=id_real)
                        # Nombre limpio
                        evento["responsable"] = f"{maestro.user.first_name} {maestro.user.last_name}"
                        # Campo nuevo para el rol
                        evento["rol_responsable"] = "Maestro"
                        
                    elif tipo == "A":
                        admin = Administradores.objects.get(id=id_real)
                        # Nombre limpio
                        evento["responsable"] = f"{admin.user.first_name} {admin.user.last_name}"
                        # Campo nuevo para el rol
                        evento["rol_responsable"] = "Administrador"
                except Exception as e:
                    print(f"Error buscando responsable: {e}")
                    pass
                lista_final.append(evento)
        return Response(lista_final, 200)

class EventosView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # Obtener un evento por ID
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        data = EventoSerializer(evento).data
        if data["publico"]:
            try:
                data["publico"] = json.loads(data["publico"])
            except:
                data["publico"] = []
                
        return Response(data, 200)

    # Registrar nuevo evento
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Convertir la lista de público a String JSON para guardar en BD
        publico_json = json.dumps(request.data["publico"], ensure_ascii=False)
        
        evento = Eventos.objects.create(
            nombre=request.data["nombre"],
            tipo=request.data["tipo"],
            fecha=request.data["fecha"],
            hora_inicio=request.data["hora_inicio"],
            hora_fin=request.data["hora_fin"],
            lugar=request.data["lugar"],
            publico=publico_json,
            programa=request.data.get("programa"), # .get por si viene vacío
            responsable=request.data["responsable"],
            descripcion=request.data["descripcion"],
            cupo=request.data["cupo"]
        )
        evento.save()
        
        return Response({"evento_created_id": evento.id}, 201)

    # Actualizar evento
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.data["id"])
        
        publico_json = json.dumps(request.data["publico"], ensure_ascii=False)
        
        evento.nombre = request.data["nombre"]
        evento.tipo = request.data["tipo"]
        evento.fecha = request.data["fecha"]
        evento.hora_inicio = request.data["hora_inicio"]
        evento.hora_fin = request.data["hora_fin"]
        evento.lugar = request.data["lugar"]
        evento.publico = publico_json
        evento.programa = request.data.get("programa")
        evento.responsable = request.data["responsable"]
        evento.descripcion = request.data["descripcion"]
        evento.cupo = request.data["cupo"]
        
        evento.save()
        
        return Response({"message": "Evento actualizado correctamente"}, 200)

    # Eliminar evento
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            evento = get_object_or_404(Eventos, id=request.GET.get("id"))
            evento.delete()
            return Response({"details": "Evento eliminado"}, 200)
        except Exception as e:
            return Response({"details": "Error al eliminar"}, 400)