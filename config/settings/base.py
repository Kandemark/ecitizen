import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders',
]

LOCAL_APPS = [
    'core',
    'apps.accounts',
    'apps.onboarding',
    'apps.counties',
    'apps.ministries',
    'apps.services',
    'apps.applications',
    'apps.workflow',
    'apps.appointments',
    'apps.documents',
    'apps.verification',
    'apps.licenses',
    'apps.land',
    'apps.immigration',
    'apps.transport',
    'apps.health',
    'apps.education',
    'apps.judiciary',
    'apps.taxes',
    'apps.civil_registry',
    'apps.constitution',
    'apps.legislature',
    'apps.authorities',
    'apps.elections',
    'apps.procurement',
    'apps.payments',
    'apps.notifications',
    'apps.messaging',
    'apps.feedback',
    'apps.analytics',
    'apps.reports',
    'apps.audit',
    'apps.search',
    'apps.api_gateway',
    'apps.developer_portal',
    'apps.integration',
    'apps.news',
    'apps.emergency',
    'apps.public_participation',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'core.middleware.SecurityHeadersMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RequestIDMiddleware',
    'core.middleware.AuditLogMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.contexts.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('sw', 'Kiswahili'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

FIXTURE_DIRS = [BASE_DIR / 'fixtures']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.StandardCursorPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.environ.get('API_ANON_RATE_LIMIT', '60/minute'),
        'user': os.environ.get('API_USER_RATE_LIMIT', '1000/hour'),
        'login': os.environ.get('LOGIN_RATE_LIMIT', '5/minute'),
        'registration': os.environ.get('REGISTRATION_RATE_LIMIT', '3/hour'),
        'search': os.environ.get('SEARCH_RATE_LIMIT', '30/minute'),
    },
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'e-Citizen API',
    'DESCRIPTION': 'Kenya Government e-Citizen Platform API. '
                   'Digital access to government services for all citizens.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {'name': 'e-Citizen Support', 'email': 'support@ecitizen.go.ke'},
    'LICENSE': {'name': 'Government of Kenya'},
}

# Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_BEAT_SCHEDULE = {
    'fetch-news-every-30-minutes': {
        'task': 'apps.news.tasks.fetch_all_news_sources',
        'schedule': 1800.0,
    },
    'cleanup-old-news-daily': {
        'task': 'apps.news.tasks.cleanup_old_articles',
        'schedule': 86400.0,
    },
    'refresh-economic-data-hourly': {
        'task': 'apps.integration.tasks.refresh_economic_data',
        'schedule': 3600.0,
    },
    'refresh-exchange-rates-2hourly': {
        'task': 'apps.integration.tasks.fetch_cbk_exchange_rates',
        'schedule': 7200.0,
    },
    'refresh-all-weather-30min': {
        'task': 'apps.integration.tasks.refresh_all_weather',
        'schedule': 1800.0,
    },
    'check-workflow-escalations-hourly': {
        'task': 'workflow.check_escalations',
        'schedule': 3600.0,
    },
    'sync-parliament-data-daily': {
        'task': 'legislature.sync_all_parliament_data',
        'schedule': 86400.0,
    },
    'sync-parliament-bills-6hourly': {
        'task': 'legislature.sync_bills',
        'schedule': 21600.0,
    },
    'sync-parliament-hansards-12hourly': {
        'task': 'legislature.sync_hansards',
        'schedule': 43200.0,
    },
}

# Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
    }
}

# Session with Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 'http://localhost:9000,http://127.0.0.1:9000'
).split(',')

# Africa's Talking SMS
AT_USERNAME = os.environ.get('AT_USERNAME', '')
AT_API_KEY = os.environ.get('AT_API_KEY', '')
AT_SENDER_ID = os.environ.get('AT_SENDER_ID', 'eCitizen')

# M-Pesa Daraja
MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', '')
MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', '')
MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', '')
MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE', '')
MPESA_ENV = os.environ.get('MPESA_ENV', 'sandbox')

# File storage
DEFAULT_FILE_STORAGE = os.environ.get(
    'DEFAULT_FILE_STORAGE',
    'django.core.files.storage.FileSystemStorage'
)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', '')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# Email
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@ecitizen.go.ke')
SUPPORT_EMAIL = os.environ.get('SUPPORT_EMAIL', 'support@ecitizen.go.ke')

# CSRF / Session Security
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS', 'http://localhost:9000,http://127.0.0.1:9000'
).split(',')
SESSION_COOKIE_AGE = int(os.environ.get('SESSION_COOKIE_AGE', '1209600'))
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 0  # Set to 31536000 in production with HTTPS
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Feature Flags (read from env, default True for core features)
FEATURE_LIVE_NEWS = os.environ.get('FEATURE_LIVE_NEWS', 'True') == 'True'
FEATURE_LIVE_WEATHER = os.environ.get('FEATURE_LIVE_WEATHER', 'True') == 'True'
FEATURE_LIVE_ECONOMIC_DATA = os.environ.get('FEATURE_LIVE_ECONOMIC_DATA', 'True') == 'True'
FEATURE_MPESA_PAYMENTS = os.environ.get('FEATURE_MPESA_PAYMENTS', 'False') == 'True'
FEATURE_SMS_NOTIFICATIONS = os.environ.get('FEATURE_SMS_NOTIFICATIONS', 'False') == 'True'
FEATURE_PUSH_NOTIFICATIONS = os.environ.get('FEATURE_PUSH_NOTIFICATIONS', 'False') == 'True'
FEATURE_BIOMETRIC_AUTH = os.environ.get('FEATURE_BIOMETRIC_AUTH', 'False') == 'True'

# Rate Limiting scopes (used by DRF throttles above, values are read inline)

# Firebase
FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', '')
FIREBASE_CREDENTIALS_JSON = os.environ.get('FIREBASE_CREDENTIALS_JSON', '')

# Default weather county
DEFAULT_WEATHER_COUNTY = os.environ.get('DEFAULT_WEATHER_COUNTY', '047')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
