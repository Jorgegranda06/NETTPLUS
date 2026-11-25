from django.db import models as m
class Departamento(m.Model):
    nombre=m.CharField(max_length=150,unique=True)
    def __str__(self): return self.nombre
class Colaborador(m.Model):
    departamento_ref=m.ForeignKey(Departamento,null=True,blank=True,on_delete=m.SET_NULL)
    empleado_id=m.CharField(max_length=80,unique=True)
    nombre=m.CharField(max_length=200)
    empresa=m.CharField(max_length=150,blank=True)
    departamento=m.CharField(max_length=150,blank=True)
    cargo=m.CharField(max_length=150,blank=True)
    origen=m.CharField(max_length=80,default='manual')
    activo=m.BooleanField(default=True)
class Marcacion(m.Model):
    colaborador_ref=m.ForeignKey(Colaborador,null=True,blank=True,on_delete=m.SET_NULL)
    empleado_id=m.CharField(max_length=80)
    nombre=m.CharField(max_length=200)
    departamento=m.CharField(max_length=150,blank=True)
    fecha=m.DateField()
    hora=m.TimeField()
    tipo_marcacion=m.CharField(max_length=10,choices=[('Entrada','Entrada'),('Salida','Salida')])
    tipo=m.CharField(max_length=80,blank=True)
    class Meta:
        constraints=[m.UniqueConstraint(fields=['empleado_id','fecha','hora','tipo_marcacion'],name='marca_unica')]
class Horario(m.Model):
    colaborador_ref=m.ForeignKey(Colaborador,null=True,blank=True,on_delete=m.SET_NULL)
    empleado_id=m.CharField(max_length=80)
    dia_semana=m.PositiveSmallIntegerField()
    hora_entrada=m.TimeField()
    hora_salida=m.TimeField()
    tolerancia_min=m.PositiveSmallIntegerField(default=0)
    fuente=m.CharField(max_length=80,default='manual provisional')
    class Meta:
        constraints=[m.UniqueConstraint(fields=['empleado_id','dia_semana'],name='horario_unico')]
class Permiso(m.Model):
    colaborador_ref=m.ForeignKey(Colaborador,null=True,blank=True,on_delete=m.SET_NULL)
    empleado_id=m.CharField(max_length=80)
    nombres=m.CharField(max_length=150)
    apellidos=m.CharField(max_length=150,blank=True)
    departamento=m.CharField(max_length=150,blank=True)
    fecha_inicio=m.DateTimeField()
    fecha_fin=m.DateTimeField()
    estado=m.CharField(max_length=80)
    codigo_pago=m.CharField(max_length=80,blank=True)
class Importacion(m.Model):
    archivo=m.CharField(max_length=255)
    fecha=m.DateTimeField(auto_now_add=True)
    usuario=m.CharField(max_length=150)
    total=m.PositiveIntegerField(default=0)
    insertados=m.PositiveIntegerField(default=0)
    duplicados=m.PositiveIntegerField(default=0)
    rechazados=m.PositiveIntegerField(default=0)
class Auditoria(m.Model):
    usuario=m.CharField(max_length=150)
    accion=m.CharField(max_length=255)
    fecha=m.DateTimeField(auto_now_add=True)

from . import relaciones
