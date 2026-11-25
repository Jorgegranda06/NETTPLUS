import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/'.env')
SECRET_KEY=os.environ['SECRET_KEY']
DEBUG=True
ALLOWED_HOSTS=['localhost','127.0.0.1','10.0.2.2']
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','corsheaders','rest_framework','rest_framework.authtoken','drf_spectacular','negocio']
MIDDLEWARE=['corsheaders.middleware.CorsMiddleware','django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
DATABASES={'default':{'ENGINE':'django.db.backends.mysql','NAME':os.getenv('DB_NAME','nettplus_db'),'USER':os.getenv('DB_USER','root'),'PASSWORD':os.getenv('DB_PASSWORD',''),'HOST':'127.0.0.1','PORT':'3306','OPTIONS':{'charset':'utf8mb4'}}}
STATIC_URL='/static/'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LANGUAGE_CODE='es'
TIME_ZONE='America/Guayaquil'
USE_TZ=True
CORS_ALLOWED_ORIGINS=['http://localhost:4200','http://localhost','https://localhost','capacitor://localhost']
REST_FRAMEWORK={'DEFAULT_AUTHENTICATION_CLASSES':['negocio.authentication.Bearer'],'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated'],'DEFAULT_SCHEMA_CLASS':'drf_spectacular.openapi.AutoSchema'}
SPECTACULAR_SETTINGS={'TITLE':'NETTPLUS API','VERSION':'1.0'}
