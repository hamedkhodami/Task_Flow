from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

#from ckeditor_demo.settings import CKEDITOR_UPLOAD_PATH
#from django.conf.global_settings import AUTH_USER_MODEL, AUTHENTICATION_BACKENDS, EMAIL_HOST, EMAIL_PORT, \
#    EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_BACKEND

#---BASE_DIR------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
#-----------------------------------------------------------------



#---ENV-----------------------------------------------------------
load_dotenv(dotenv_path=BASE_DIR / '.env')
#-----------------------------------------------------------------



#---SECURITY------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
#-----------------------------------------------------------------



#---CSRF---------------------------------------------------------
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED', 'http://127.0.0.1',).split(',')
#----------------------------------------------------------------



#---Application definitio-----------------------------------------
INSTALLED_APPS = [
    'channels',
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #apps
    'apps.core.apps.CoreConfig',
    'apps.account.apps.AccountConfig',
    'apps.project.apps.ProjectConfig',
    'apps.task.apps.TaskConfig',
    'apps.notification.apps.NotificationConfig',
    'apps.report.apps.ReportConfig',
    'apps.public.apps.PublicConfig',
    'apps.integration.apps.IntegrationConfig',
    'apps.ai_assistant.apps.AiAssistantConfig',
    'apps.chat.apps.ChatConfig',

    #Django modules

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
#----------------------------------------------------------------



#---ASGI---------------------------------------------------------
ASGI_APPLICATION = 'config.asgi.application'
#----------------------------------------------------------------



#---Password validation------------------------------------------
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
#----------------------------------------------------------------



#---Internationalization-----------------------------------------
LANGUAGES = [
    ('fa', _("Persian")),
]

LOCALE_PATHS = [
    BASE_DIR / os.getenv('LOCALE_PATHS', 'locale'),
    os.getenv('DJANGO_Q_LOCALE_PATH', BASE_DIR / 'locale/django_q'),
]

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = False
#----------------------------------------------------------------



#---Static files-------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT')

STATICFILES_DIRS = [
   os.getenv('STATICFILES_DIRS', BASE_DIR / 'static/assets/'),
]
#----------------------------------------------------------------



#---Media--------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / os.getenv('MEDIA_ROOT', 'static/media')
#----------------------------------------------------------------



#---Production whitenoise----------------------------------------
if int(os.getenv('ENABLE_WHITENOISE', default=0)):
    # Insert Whitenoise Middleware and set as StaticFileStorage
    MIDDLEWARE += [
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ]
    STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
#----------------------------------------------------------------



#Default primary key field type---------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#---------------------------------------------------------------



#---Auth user model---------------------------------------------
AUTH_USER_MODEL = 'account.UserModel'
#---------------------------------------------------------------



#---redis-------------------------------------------------------
REDIS_CONFIG = {
    'active': int(os.getenv('REDIS_ACTIVE', 0)),  # 1 redis is connected, 0 not connected
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379))
}
#---------------------------------------------------------------



#---CHANNEL_LAYERS----------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
#---------------------------------------------------------------