from django.contrib import admin
from .models import *
for model in [Departamento,Colaborador,Marcacion,Horario,Permiso,Importacion,Auditoria]: admin.site.register(model)
