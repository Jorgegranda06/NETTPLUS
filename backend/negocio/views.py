from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate,get_user_model
from django.db.models import Count
from django.http import HttpResponse
from datetime import datetime,timedelta
from .models import *
from .serializers import serializer
from openpyxl import load_workbook,Workbook
from util.validador_excel import ValidadorExcel
class Bearer(TokenAuthentication): keyword='Bearer'
def role(u): return 'Administrador' if u.is_superuser else (u.groups.first().name if u.groups.exists() else 'Consulta')
def user(u): return dict(id=u.id,nombre=u.get_full_name() or u.username,usuario=u.username,rol=role(u),activo=u.is_active)
class Editor(permissions.BasePermission):
    def has_permission(self,r,v): return r.user.is_authenticated and (r.method in permissions.SAFE_METHODS or role(r.user) in ['Administrador','Recursos Humanos'])
class CRUD(viewsets.ModelViewSet):
    permission_classes=[Editor]
    def perform_create(self,s): s.save(); Auditoria.objects.create(usuario=self.request.user.username,accion='Crear '+self.basename)
    def perform_update(self,s): s.save(); Auditoria.objects.create(usuario=self.request.user.username,accion='Actualizar '+self.basename)
    def perform_destroy(self,o): o.delete(); Auditoria.objects.create(usuario=self.request.user.username,accion='Eliminar '+self.basename)
def crud(model): return type(model.__name__+'ViewSet',(CRUD,),{'queryset':model.objects.all().order_by('pk'),'serializer_class':serializer(model)})
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(r):
    u=authenticate(username=r.data.get('usuario'),password=r.data.get('password'))
    if not u:return Response({'error':'Credenciales incorrectas'},status=401)
    return Response({'token':Token.objects.get_or_create(user=u)[0].key,'usuario':user(u)})
@api_view(['GET','POST'])
def session(r):
    if r.method=='POST': Token.objects.filter(user=r.user).delete(); return Response({'mensaje':'Sesión cerrada'})
    return Response({'usuario':user(r.user)})
@api_view(['GET','POST'])
def usuarios(r):
    if not r.user.is_superuser:return Response(status=403)
    U=get_user_model()
    if r.method=='GET':return Response({'usuarios':[user(u) for u in U.objects.all()]})
    from .usuarios_api import UsuarioSerializer
    d=r.data
    s=UsuarioSerializer(data=dict(username=d.get('usuario'),password=d.get('password'),first_name=d.get('nombre',''),rol=d.get('rol','Recursos Humanos')))
    s.is_valid(raise_exception=True); obj=s.save(); Auditoria.objects.create(usuario=r.user.username,accion=f'Crear cuenta #{obj.pk}'); return Response({'mensaje':'Usuario creado'},status=201)
@api_view(['GET'])
def auditoria(r):
    if not r.user.is_superuser:return Response(status=403)
    return Response({'registros':rows(Auditoria,Auditoria.objects.order_by('-fecha','-pk'))})

def rows(model,qs=None):return serializer(model)(model.objects.all() if qs is None else qs,many=True).data
@api_view(['GET'])
def resumen(r):return Response(dict(marcaciones=Marcacion.objects.count(),colaboradores=Colaborador.objects.count(),importaciones=Importacion.objects.count(),ultimas=rows(Importacion,Importacion.objects.order_by('-fecha')[:6])))
@api_view(['GET'])
def historial(r):return Response({'importaciones':rows(Importacion)})
@api_view(['GET','POST','DELETE'])
def sprint(r,accion,pk=None):
    emp=r.query_params.get('empleado_id',''); marks=Marcacion.objects.all(); cs=Colaborador.objects.all(); hs=Horario.objects.all()
    if emp:marks=marks.filter(empleado_id=emp)
    if accion=='colaboradores':
        from django.db.models import Q
        q=r.query_params.get('q','');return Response({'colaboradores':rows(Colaborador,cs.filter(Q(nombre__icontains=q)|Q(empleado_id__icontains=q)))})
    if accion=='asistencia':return Response({'marcaciones':rows(Marcacion,marks.order_by('-fecha','-hora'))})
    if accion=='indicadores':return Response(dict(marcaciones=marks.count(),empleados_identificados=marks.filter(empleado_id__in=cs.values('empleado_id')).values('empleado_id').distinct().count(),dias_con_marcaciones=marks.values('fecha').distinct().count()))
    if accion=='no-identificadas':return Response({'colaboradores':list(marks.exclude(empleado_id__in=cs.values('empleado_id')).values('empleado_id','nombre').annotate(total=Count('id')))})
    if accion=='permisos':return Response({'permisos':rows(Permiso)})
    if accion=='horarios':
        if r.method!='GET' and role(r.user) not in ['Administrador','Recursos Humanos']:return Response(status=403)
        if r.method=='DELETE':
            n,_=hs.filter(pk=pk).delete();return Response({'eliminado':bool(n)},status=200 if n else 404)
        if r.method=='POST':
            s=serializer(Horario)(data=r.data)
            if not s.is_valid():return Response({'error':str(s.errors)},status=400)
            s.save();return Response({'mensaje':'Horario guardado'},status=201)
        data=rows(Horario,hs.filter(empleado_id=emp) if emp else hs); names=dict(cs.values_list('empleado_id','nombre'))
        return Response({'horarios':[dict(x,nombre_empleado=names.get(x['empleado_id'],'Sin coincidencia')) for x in data]})
    if accion=='atrasos':
        reglas={(h.empleado_id,h.dia_semana):h for h in hs}; seen=set(); out=[]; evaluados=sin=0
        for m in marks.filter(tipo_marcacion='Entrada').order_by('fecha','hora'):
            k=(m.empleado_id,m.fecha)
            if k in seen:continue
            seen.add(k); h=reglas.get((m.empleado_id,m.fecha.weekday()))
            if not h:sin+=1;continue
            evaluados+=1; mins=int((datetime.combine(m.fecha,m.hora)-datetime.combine(m.fecha,h.hora_entrada)).total_seconds()//60)-h.tolerancia_min
            if mins>0:out.append(dict(empleado_id=m.empleado_id,nombre=m.nombre,fecha=m.fecha,hora_entrada=m.hora,hora_programada=h.hora_entrada,tolerancia_min=h.tolerancia_min,minutos_atraso=mins))
        return Response(dict(atrasos=out,total_atrasos=len(out),dias_evaluados=evaluados,dias_sin_horario=sin,criterio='Provisional: primera marcación de Entrada menos entrada y tolerancia; confirmar RRHH.'))
    return Response(status=404)
@api_view(['GET'])
def ficha(r,emp):
    c=Colaborador.objects.filter(empleado_id=emp).first()
    if not c:return Response(status=404)
    h=Horario.objects.filter(empleado_id=emp);return Response(dict(colaborador=serializer(Colaborador)(c).data,marcaciones=Marcacion.objects.filter(empleado_id=emp).count(),permisos=Permiso.objects.filter(empleado_id=emp).count(),horarios=h.count(),detalle_horarios=rows(Horario,h)))
@api_view(['POST'])
@permission_classes([Editor])
def importar(r,categoria):
    a=r.FILES.get('archivo')
    if not a or not a.name.lower().endswith('.xlsx'):return Response({'error':'Selecciona Excel .xlsx'},status=400)
    if categoria in ('solicitudes','consolidado'):
        from .importadores import auxiliar
        return auxiliar(a,categoria,r.user.username)
    if categoria!='marcaciones':return Response({'error':'Formato oficial de horarios pendiente'},status=400)
    try:
        wb=load_workbook(a,read_only=True,data_only=True); it=iter(wb.active.values); head=next(it,()); start=2
        if head and str(head[0]).strip().lower()=='reporte de marcaciones':head=next(it,());start=3
        v=ValidadorExcel(); idx=v.indices(head); total=insertados=duplicados=rechazados=0; errores=[]
        for i,row in enumerate(it,start):
            if not any(x is not None and str(x).strip() for x in row):continue
            total+=1
            try:
                v.convertir_marcacion(row,idx); d={k:row[j] for k,j in idx.items()}; emp=str(d['Id del Empleado']).strip(); nombre=str(d['Nombres']).strip(); dep=str(d['Departamento'] or '')
                _,new=Marcacion.objects.get_or_create(empleado_id=emp,fecha=v.fecha(d['Fecha']),hora=v.hora(d['Hora']),tipo_marcacion=str(d['Tipo de Marcación']).strip().title(),defaults=dict(nombre=nombre,departamento=dep,tipo=str(d['Tipo'] or '')))
                insertados+=int(new);duplicados+=int(not new)
            except Exception as e:rechazados+=1;errores.append(dict(fila=i,motivo=str(e)))
        wb.close(); Importacion.objects.create(archivo=a.name,usuario=r.user.username,total=total,insertados=insertados,duplicados=duplicados,rechazados=rechazados)
        return Response(dict(mensaje='Importación procesada',total=total,insertados=insertados,duplicados=duplicados,rechazados=rechazados,errores=errores[:30]))
    except Exception as e:return Response({'error':str(e)},status=400)
