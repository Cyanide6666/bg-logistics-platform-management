import os
from pathlib import Path
import dj_database_url
import json
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hgnaf+gmk=v$w=f)=crauj6gf+xq1jdg2ij#1&nvz(^xxo2o&q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_host:
    ALLOWED_HOSTS.append(render_host)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',  # Para la weaita de my.sirv porque firebase no me conectó
    'web_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'web_app', 'templates')], # <--- Ruta absoluta
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database NEON.TECH
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Neon DB
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://neondb_owner:npg_9P4pmFZANRfw@ep-polished-cloud-aprowmse.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require'
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

# Esto le dice a Django que busque en las carpetas 'static' de cada app
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Si pusiste la carpeta static en la raíz del proyecto (al lado de manage.py)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

LOGIN_URL = 'home'
LOGIN_REDIRECT_URL = 'panel_cliente'
LOGOUT_REDIRECT_URL = 'home'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#Para trabajar en el PC (localhost)
#DOMAIN = 'http://127.0.0.1:8000'

# Si existe la variable RENDER, estamos en la nube, si no, estamos local.
if os.environ.get('RENDER'):
    DOMAIN = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"
else:
    DOMAIN = 'http://127.0.0.1:8000'

# CONFIGURACIÓN DE FIREBASE STORAGE
if not DEBUG:  # Esto se activa cuando estés en Render
    # Intentamos leer la variable de entorno que crearemos en Render
    firebase_json = os.environ.get('FIREBASE_JSON_DATA')
    
    if firebase_json:
        info = json.loads(firebase_json)
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(info)
        DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
        GS_BUCKET_NAME = 'tu-proyecto.appspot.com' # <--- CAMBIA ESTO POR TU BUCKET
        
        # Esto es para que los archivos sean públicos y se puedan ver con el QR
        GS_DEFAULT_ACL = 'publicRead' 
else:
    # En tu PC local, sigue usando la carpeta media normal
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración de Sirv (vía S3)
AWS_ACCESS_KEY_ID = 'contacto@brokergroup.cl'
AWS_SECRET_ACCESS_KEY = 'cZoRi4MGlbv4j22I7KPrBmFo3s8A15wUkyXdboXjpPZug7n7'
AWS_STORAGE_BUCKET_NAME = 'brokergroup'
AWS_S3_ENDPOINT_URL = 'https://s3.sirv.com'
AWS_S3_REGION_NAME = 'eu-west-1' # Sirv suele usar esta por defecto

# Para que los archivos se suban a Sirv y no a tu PC
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Para que los archivos sean públicos y se puedan ver
AWS_QUERYSTRING_AUTH = False