from datetime import datetime
from django.db import transaction
from django.utils import timezone
from openpyxl import load_workbook
from rest_framework.response import Response
from .models import Colaborador, Departamento, Permiso, Importacion

def auxiliar(a,categoria,usuario):
    def txt(x): return str(x).strip() if x is not None else ''
    def dt(x):
        d=x if isinstance(x,datetime) else datetime.fromisoformat(txt(x))
        return timezone.make_aware(d) if timezone.is_naive(d) else d
    total=insertados=duplicados=rechazados=0
    errores=[]
    try:
        wb=load_workbook(a,read_only=True,data_only=True)
        try:
            it=iter(wb.active.values)
            next(it)
            head=[txt(x).casefold() for x in next(it)]
            required={'id','nombres','apellidos','empresa','departamento','cargo'} if categoria=='consolidado' else {'id del empleado','nombres','hora entrada','hora salida','estado de aprobación'}
            if not required.issubset(head): raise ValueError('Columnas obligatorias ausentes: '+', '.join(required-set(head)))
            with transaction.atomic():
                for i,row in enumerate(it,3):
                    if not any(txt(x) for x in row): continue
                    total+=1
                    d=dict(zip(head,row))
                    def g(k): return txt(d.get(k))
                    try:
                        with transaction.atomic():
                            if categoria=='consolidado':
                                emp=g('id'); nombre=(g('nombres')+' '+g('apellidos')).strip()
                                if not emp or not nombre: raise ValueError('ID o nombre vacío')
                                data=dict(nombre=nombre,empresa=g('empresa'),departamento=g('departamento'),cargo=g('cargo'),origen='consolidado')
                                if data['departamento']: Departamento.objects.get_or_create(nombre=data['departamento'])
                                obj=Colaborador.objects.filter(empleado_id=emp).first()
                                changed=obj is None or any(getattr(obj,k)!=val for k,val in data.items())
                                if changed: Colaborador.objects.update_or_create(empleado_id=emp,defaults=data)
                            else:
                                emp=g('id del empleado'); ini=dt(d.get('hora entrada')); fin=dt(d.get('hora salida'))
                                if not emp or not g('nombres') or not g('estado de aprobación') or fin<ini: raise ValueError('Permiso inválido')
                                _,changed=Permiso.objects.get_or_create(empleado_id=emp,fecha_inicio=ini,fecha_fin=fin,codigo_pago=g('código de pago'),defaults=dict(nombres=g('nombres'),apellidos=g('apellidos'),departamento=g('departamento'),estado=g('estado de aprobación')))
                            insertados+=int(changed); duplicados+=int(not changed)
                    except Exception as e:
                        rechazados+=1; errores.append(dict(fila=i,motivo=str(e)))
                Importacion.objects.create(archivo=a.name,usuario=usuario,total=total,insertados=insertados,duplicados=duplicados,rechazados=rechazados)
        finally: wb.close()
        return Response(dict(mensaje='Procesado (insertados incluye actualizados)',total=total,insertados=insertados,duplicados=duplicados,rechazados=rechazados,errores=errores[:30]))
    except Exception as e: return Response({'error':str(e)},status=400)
