from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from negocio.models import Departamento, Colaborador


class PruebasNETTPLUS(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin_pruebas', email='admin@example.test', password='PruebaSegura123!')
        self.client.force_authenticate(user=self.admin)
        self.dep = Departamento.objects.create(nombre='Departamento TEST')
        self.col = Colaborador.objects.create(empleado_id='TEST001', nombre='Empleado TEST', departamento=self.dep.nombre)

    def ciclo(self, entidad, datos, cambio, invalidos=None):
        url = f'/api/{entidad}/'
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200, r.data)
        r = self.client.post(url, datos, format='json')
        self.assertEqual(r.status_code, 201, r.data)
        pk = r.data['id']
        detalle = f'{url}{pk}/'
        r = self.client.get(detalle)
        self.assertEqual(r.status_code, 200, r.data)
        actualizados = dict(datos, **cambio)
        r = self.client.put(detalle, actualizados, format='json')
        self.assertEqual(r.status_code, 200, r.data)
        r = self.client.patch(detalle, cambio, format='json')
        self.assertEqual(r.status_code, 200, r.data)
        r = self.client.get(detalle)
        for campo, valor in cambio.items():
            self.assertEqual(r.data[campo], valor)
        if invalidos is not None:
            r = self.client.post(url, invalidos, format='json')
            self.assertEqual(r.status_code, 400, r.data)
        r = self.client.delete(detalle)
        self.assertEqual(r.status_code, 204, r.data)
        self.assertEqual(self.client.get(detalle).status_code, 404)

    def test_departamentos(self):
        self.ciclo('departamentos', {'nombre':'Temporal TEST'}, {'nombre':'Editado TEST'}, {'nombre':''})

    def test_colaboradores(self):
        d = dict(empleado_id='TEST002', nombre='Temporal TEST', empresa='NETTPLUS', departamento=self.dep.nombre, cargo='Tecnico', activo=True)
        self.ciclo('colaboradores', d, {'cargo':'Supervisor'}, dict(d, empleado_id=''))

    def test_marcaciones(self):
        d = dict(empleado_id=self.col.empleado_id, nombre=self.col.nombre, departamento=self.dep.nombre, fecha='2026-10-12', hora='08:00:00', tipo_marcacion='Entrada', tipo='Manual')
        self.ciclo('marcaciones', d, {'tipo':'Prueba'}, dict(d, tipo_marcacion='Invalido'))

    def test_horarios(self):
        d = dict(empleado_id=self.col.empleado_id, dia_semana=0, hora_entrada='08:00:00', hora_salida='17:00:00', tolerancia_min=5)
        self.ciclo('horarios', d, {'tolerancia_min':10}, dict(d, dia_semana=7))

    def test_permisos(self):
        d = dict(empleado_id=self.col.empleado_id, nombres='Empleado', apellidos='TEST', departamento=self.dep.nombre, fecha_inicio='2026-10-12T08:00:00-05:00', fecha_fin='2026-10-12T10:00:00-05:00', estado='Pendiente', codigo_pago='TEST')
        self.ciclo('permisos', d, {'estado':'Aprobado'}, dict(d, fecha_fin='2026-10-11T10:00:00-05:00'))

    def test_cuentas_listado(self):
        self.assertEqual(self.client.get('/api/cuentas/').status_code, 200)

    def test_acceso_sin_autenticacion(self):
        self.client.force_authenticate(user=None)
        self.assertIn(self.client.get('/api/colaboradores/').status_code, (401,403))
