from rest_framework import serializers as s
from .models import *
class HorarioSerializer(s.ModelSerializer):
    class Meta: model=Horario; fields='__all__'; read_only_fields=('colaborador_ref',)
    def validate(self,d):
        def v(k): return d.get(k,getattr(self.instance,k,0 if k=='tolerancia_min' else None))
        if not 0<=v('dia_semana')<=6 or not 0<=v('tolerancia_min')<=180 or v('hora_salida')<=v('hora_entrada'): raise s.ValidationError('Horario inválido; solo turnos del mismo día.')
        return d
class PermisoSerializer(s.ModelSerializer):
    class Meta: model=Permiso; fields='__all__'; read_only_fields=('colaborador_ref',)
    def validate(self,d):
        if d.get('fecha_fin',getattr(self.instance,'fecha_fin',None))<d.get('fecha_inicio',getattr(self.instance,'fecha_inicio',None)): raise s.ValidationError('Fin anterior al inicio')
        return d
def serializer(model):
    if model==Horario:return HorarioSerializer
    if model==Permiso:return PermisoSerializer
    return type(model.__name__+'Serializer',(s.ModelSerializer,),{'Meta':type('Meta',(),{'model':model,'fields':'__all__','read_only_fields':('departamento_ref',) if model==Colaborador else ('colaborador_ref',) if model==Marcacion else ()})})
