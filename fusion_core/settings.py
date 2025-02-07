from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from import_export.formats.base_formats import XLSX

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
VERSION = 'deploy'
SECRET_KEY = getenv('SECRET_KEY')
BOT_TOKEN = getenv('BOT_TOKEN')

DEBUG = True
CSRF_COOKIE_SECURE = False
ALLOWED_HOSTS = ['127.0.0.1','nurbot.kz','www.nurbot.kz']
CSRF_TRUSTED_ORIGINS = ['https://nurbot.kz',
                        'http://127.0.0.1',
                        'http://127.0.0.1:8000',
]

FEDOR_ID = 716336613
TELEGRAM_ADMINS = [FEDOR_ID,515207530]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot.apps.BotConfig',
    'django_celery_beat',
    'phrases.apps.PhrasesConfig',
    'services.apps.ServicesConfig',
    'lottery.apps.LotteryConfig',
    'import_export',
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

ROOT_URLCONF = 'fusion_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'fusion_core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('DB_NAME'),
        'USER': getenv('DB_USER'),
        'PASSWORD': getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT'),
    }
}

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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True


if VERSION == 'deploy':
    FORCE_SCRIPT_NAME = '/battery/'
    BASE_URL = '/battery'
    MEDIA_URL = BASE_URL + '/media/'
    STATIC_URL =BASE_URL + '/static/'
elif VERSION == 'development':
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
else:
    raise ValueError('VERSION can be either development or deploy')


STATIC_ROOT = '/var/www/static'
MEDIA_ROOT = '/var/www/media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
BASE_LOCALHOST_URL = 'http://web:8000/'


IMPORT_EXPORT_USE_TRANSACTIONS=True

EXPORT_FORMATS = [XLSX]
IMPORT_FORMATS = []