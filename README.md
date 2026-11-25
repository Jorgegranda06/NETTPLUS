# NETTPLUS — adaptación académica preliminar
No es una entrega verificada. Conserva el frontend original y adapta parte de su API a Django/MySQL. No contiene datos reales ni credenciales. No sustituye el original Flask/PostgreSQL.

## Windows
1. En MySQL Workbench ejecutar database/crear.sql. Usar una base vacía de pruebas.
2. Abrir PowerShell en esta carpeta. Ejecutar `powershell -ExecutionPolicy Bypass -File .\INSTALAR.ps1`. Introducir usuario y contraseña MySQL y crear superusuario Django. Requiere Internet para dependencias.
3. En dos terminales: `powershell -ExecutionPolicy Bypass -File .\INICIAR_BACKEND.ps1` y `powershell -ExecutionPolicy Bypass -File .\INICIAR_FRONTEND.ps1`.
4. Abrir http://localhost:4200, iniciar sesión con el superusuario creado. Admin: http://127.0.0.1:8000/admin/ ; Swagger: http://127.0.0.1:8000/api/docs/ .
5. En frontend: `npx cap open android`. Ejecutar en emulador. Backend debe seguir activo. Si Android no permite HTTP, revisar manifest y configuración de red de desarrollo. No se incluye APK.

## Pruebas y evidencias
En Gestión CRUD crear departamento o colaborador ficticio, listar, abrir detalle, editar y eliminar. En Swagger autenticar con token Bearer obtenido en POST /api/login (si Swagger no ofrece autorización, usar Postman). Comprobar GET 200, POST 201, PUT/PATCH 200, DELETE 204, GET de ID eliminado 404, POST inválido 400. Capturar tablas MySQL, Swagger, web y Android. Completar matriz solo con pruebas realizadas.

## Limitaciones
No se ejecutaron Django, MySQL, npm build ni Android en este entorno. Migraciones se generan localmente. No se migró el backup PostgreSQL. Importación auxiliar, reportes, ausencias, roles CRUD, relaciones FK completas, rutas Angular por entidad y auditoría completa pendientes. El cálculo de atrasos es provisional. No presentar como funcionalidades verificadas. El documento de requisitos original se incluye. El frontend conserva estructura monolítica original con una página CRUD compartida. Android se genera localmente mediante Capacitor. No usar datos personales reales para pruebas.
