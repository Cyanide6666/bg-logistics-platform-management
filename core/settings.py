import os
from pathlib import Path
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv  # <--- Esta librería es la magia

# Carga las variables del archivo .env
load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_host:
    ALLOWED_HOSTS.append(render_host)

# Si estás en DigitalOcean, esta variable se llama APP_DOMAIN, así que la agregamos también
do_host = os.environ.get('APP_DOMAIN') 
if do_host:
    ALLOWED_HOSTS.append(do_host)

# Dominio personalizado
ALLOWED_HOSTS.append('brokerflow.cl')


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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        default=os.environ.get('DATABASE_URL')    )
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


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
elif os.environ.get('APP_DOMAIN'): # Esta es la de DigitalOcean
    DOMAIN = f"https://{os.environ.get('APP_DOMAIN')}"
else:
    DOMAIN = 'http://127.0.0.1:8000'

# CONFIGURACIÓN DE ALMACENAMIENTO (SIRV via S3)
if os.environ.get('RENDER'):
    # Configuramos Sirv para la nube
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = 'https://s3.sirv.com'
    
    # Esto indica a Django que use Sirv en lugar del disco duro
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # Para que los links sean públicos (necesario para el QR)
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = 'public-read'
else:
    # En tu PC local (localhost), seguimos usando la carpeta media
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Para que los archivos se suban a Sirv y no a tu PC
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Para que los archivos sean públicos y se puedan ver
AWS_QUERYSTRING_AUTH = False