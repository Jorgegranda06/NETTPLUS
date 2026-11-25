# NETTPLUS

Proyecto academico de Ingenieria Web - UTPL.

## Tecnologias
- Django y Django REST Framework
- MySQL
- Angular e Ionic
- Capacitor y Android Studio
- Swagger / OpenAPI

## Funcionalidades
- Autenticacion y roles de usuario.
- Gestion de departamentos, colaboradores, horarios,
  marcaciones, permisos y usuarios.
- Importacion de archivos Excel.
- Indicadores y reportes de asistencia.
- Exportacion de reportes Excel.
- Auditoria de operaciones.

## Instalacion
1. Crear la base MySQL utilizando database/crear_base_academica.sql.
2. Ejecutar INSTALAR.ps1 desde PowerShell.
3. Configurar las credenciales MySQL solicitadas.
4. Crear el superusuario Django.
5. Ejecutar INICIAR_BACKEND.ps1 e INICIAR_FRONTEND.ps1
   en terminales independientes.

## Accesos
- Web: http://localhost:4200
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/api/docs/
- Django Admin: http://127.0.0.1:8000/admin/

## Android
Desde frontend ejecutar:
npm run build
npx cap sync android
npx cap open android

Ejecutar la aplicacion NETTPLUS en el emulador.
La API utiliza http://10.0.2.2:8000.

## Pruebas
Desde backend, activar el entorno virtual y ejecutar:
python manage.py check
python manage.py test

Resultado comprobado: 11 pruebas automatizadas exitosas.

## Seguridad y limitaciones
Las credenciales se almacenan en .env y no se publican.
Los calculos laborales son provisionales y requieren
validacion oficial de Recursos Humanos.
Configuracion HTTP y DEBUG exclusiva para desarrollo.
No utilizar datos personales reales para demostraciones.
La descarga Excel en Android y algunas pruebas
funcionales permanecen pendientes de verificacion.

Adaptacion academica independiente del sistema original.
