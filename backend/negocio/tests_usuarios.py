from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class PruebasUsuarios(APITestCase):
    def setUp(self):
        self.U = get_user_model()
        self.admin = self.U.objects.create_superuser(username='admin_test', password='ClaveSegura!782x')
        self.client.force_authenticate(user=self.admin)
        self.url = '/api/cuentas/'
        self.datos = dict(username='cuenta_test', first_name='Persona', last_name='Prueba', email='cuenta@example.test', is_active=True, password='ClaveDistinta!927x')

    def test_crud_usuarios(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        r = self.client.post(self.url, self.datos, format='json')
        self.assertEqual(r.status_code, 201, r.data)
        self.assertNotIn('password', r.data)
        pk = r.data['id']
        self.assertTrue(self.U.objects.get(pk=pk).check_password(self.datos['password']))
        url = f'{self.url}{pk}/'
        self.assertEqual(self.client.get(url).status_code, 200)
        datos = dict(self.datos, first_name='Editado')
        datos.pop('password')
        r = self.client.put(url, datos, format='json')
        self.assertEqual(r.status_code, 200, r.data)
        self.assertEqual(r.data['first_name'], 'Editado')
        r = self.client.patch(url, {'is_active': False}, format='json')
        self.assertEqual(r.status_code, 200, r.data)
        self.assertFalse(self.U.objects.get(pk=pk).is_active)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_validaciones(self):
        datos = dict(self.datos)
        datos.pop('password')
        self.assertEqual(self.client.post(self.url, datos, format='json').status_code, 400)
        self.assertEqual(self.client.post(self.url, dict(self.datos, password='123'), format='json').status_code, 400)
        self.assertEqual(self.client.post(self.url, dict(self.datos, username=self.admin.username), format='json').status_code, 400)

    def test_proteccion_administrador(self):
        url = f'{self.url}{self.admin.pk}/'
        self.assertEqual(self.client.patch(url, {'is_active': False}, format='json').status_code, 400)
        self.assertEqual(self.client.delete(url).status_code, 400)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_acceso_restringido(self):
        usuario = self.U.objects.create_user(username='consulta_test', password='ClaveSegura!927x')
        self.client.force_authenticate(user=usuario)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertEqual(self.client.post(self.url, self.datos, format='json').status_code, 403)
