from negocio.reportes import reporte
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from negocio.views import *
from negocio.usuarios_api import UsuarioViewSet
router=DefaultRouter()
router.register("cuentas",UsuarioViewSet,basename="cuentas")
for name,model in [('departamentos',Departamento),('colaboradores',Colaborador),('marcaciones',Marcacion),('horarios',Horario),('permisos',Permiso)]:router.register(name,crud(model),basename=name)
urlpatterns=[path('api/auditoria/',auditoria),path('api/reportes/',reporte),path('admin/',admin.site.urls),path('api/schema/',SpectacularAPIView.as_view()),path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema')),path('api/schema/',SpectacularAPIView.as_view(),name='schema'),path('api/login',login),path('api/logout',session),path('api/me',session),path('api/usuarios',usuarios),path('api/resumen',resumen),path('api/importaciones',historial),path('api/importar/<str:categoria>',importar),path('api/sprint2/colaboradores/<str:emp>/laboral',ficha),path('api/sprint2/<str:accion>',sprint),path('api/sprint2/<str:accion>/<int:pk>',sprint),path('api/',include(router.urls))]
