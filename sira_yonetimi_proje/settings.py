# sira_yonetimi_proje/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# !!! GİZLİ ANAHTARINIZI BURAYA EKLEYİN !!!
SECRET_KEY = 'django-insecure-@111111111111111111111111111111' 

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    
    # 3. Parti Uygulamalar
    'rest_framework',
    'django_celery_results', 
    
'api',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sira_yonetimi_proje.urls' # Proje adını kullandık

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# MinIO Bağlantı Bilgileri
AWS_ACCESS_KEY_ID = 'minio_admin'       
AWS_SECRET_ACCESS_KEY = 'minio_password' 
AWS_STORAGE_BUCKET_NAME = 'bilet-evraklari'
AWS_S3_ENDPOINT_URL = 'http://minio_storage:9000'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = False # SSL sertifikası (https) kullanmadığımız için False

# Django'ya varsayılan depolama yerinin S3 (MinIO) olduğunu söylüyoruz
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# ********** CLAMAV (VİRÜS TARAMA) AYARLARI **********
# ClamAV konteynerine bağlanmak için
CLAMAV_TCP_ADDR = 'clamav_service' # docker-compose'daki isimle eşleşmeli
CLAMAV_TCP_PORT = 3310

WSGI_APPLICATION = 'sira_yonetimi_proje.wsgi.application' # Proje adını kullandık

# Veritabanı (Postgres Docker Konfigürasyonu)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),       
        'USER': os.environ.get('DB_USER'),       
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'postgres_db',                   
        'PORT': '5432',
    }
}


# Uluslararasılaştırma
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Statik Dosyalar
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ********** CELERY AYARLARI **********
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis_broker:6379/0')
CELERY_RESULT_BACKEND = 'django-db' 
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_EXTENDED = True
CORS_ALLOW_ALL_ORIGINS = True