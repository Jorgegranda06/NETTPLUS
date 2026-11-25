from datetime import date
from django.db.models import Count
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from openpyxl import Workbook
from .models import Marcacion, Colaborador, Permiso

@api_view(['GET'])
def reporte(request):
    q = request.query_params
    marks = Marcacion.objects.all()
    people = Colaborador.objects.all()
    permits = Permiso.objects.all()
    try:
        start = date.fromisoformat(q['desde']) if q.get('desde') else None
        end = date.fromisoformat(q['hasta']) if q.get('hasta') else None
        if start and end and start > end:
            raise ValueError()
    except ValueError:
        return Response({'error': 'Rango de fechas inválido'}, status=400)
    for field in ('empleado_id', 'departamento'):
        if q.get(field):
            filters = {field: q[field]}
            marks = marks.filter(**filters)
            people = people.filter(**filters)
            permits = permits.filter(**filters)
    if start:
        marks = marks.filter(fecha__gte=start)
        permits = permits.filter(fecha_fin__date__gte=start)
    if end:
        marks = marks.filter(fecha__lte=end)
        permits = permits.filter(fecha_inicio__date__lte=end)
    known = marks.filter(empleado_id__in=Colaborador.objects.values('empleado_id'))
    daily = list(marks.values('fecha').annotate(total=Count('id')).order_by('fecha'))
    data = dict(marcaciones=marks.count(), identificados=known.values('empleado_id').distinct().count(), sin_coincidencia=marks.exclude(empleado_id__in=Colaborador.objects.values('empleado_id')).values('empleado_id').distinct().count(), permisos=permits.count(), dotacion_actual=people.filter(activo=True).count(), tendencia=daily)
    if q.get('formato') != 'xlsx':
        return Response(data)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Resumen'
    for k,v in data.items():
        if k != 'tendencia': ws.append([k,v])
    ws.append(['Dotación actual, no histórica'])
    ws = wb.create_sheet('Marcaciones')
    ws.append(['ID empleado','Nombre','Departamento','Fecha','Hora','Movimiento'])
    for row in marks.order_by('fecha','hora').values_list('empleado_id','nombre','departamento','fecha','hora','tipo_marcacion').iterator():
        ws.append(list(row))
    ws = wb.create_sheet('Tendencia')
    ws.append(['Fecha','Marcaciones'])
    for row in daily: ws.append([row['fecha'],row['total']])
    ws = wb.create_sheet('Permisos')
    ws.append(['ID empleado','Nombres','Apellidos','Inicio','Fin','Estado'])
    for row in permits.values_list('empleado_id','nombres','apellidos','fecha_inicio','fecha_fin','estado').iterator():
        ws.append([str(v) if v is not None else '' for v in row])
    for sheet in wb:
        sheet.freeze_panes = 'A2'
        for row in sheet.iter_rows():
            for cell in row:
                if cell.data_type == 'f': cell.data_type = 's'
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="NETTPLUS_reporte.xlsx"'
    wb.save(response)
    return response