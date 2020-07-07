import os, json
from django.contrib.messages import constants as messages

with open('/Users/michaelpermyashkin/Desktop/Projects/Cloudland/config/config.json') as config_file:
    config = json.load(config_file)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['*']

# Site url setting
SITE_URL = 'https://cloudlandshop.com'
if DEBUG:
    SITE_URL = 'http://localhost:8000'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'localflavor',
    'storages', # S3 
    'corsheaders',

    'sellers',
    'store',
    'accounts',
    'carts',
    'orders',
]

CORS_ORIGIN_WHITELIST = ['https://cloudland-static.s3.*']

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

ROOT_URLCONF = 'cloudland.urls'

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
                'store.context_processors.add_variables_to_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'cloudland.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/' 
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'store/media')

if not DEBUG:
    ######### S3 Configurations ##########
    AWS_LOCATION = config['AWS_LOCATION']
    AWS_ACCESS_KEY_ID = config['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = config['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = config['AWS_STORAGE_BUCKET_NAME']
    AWS_FILE_OVERWRITE = False
    AWS_DEFAULT_NONE = None
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_CUSTOM_DOMAIN = config['AWS_CLOUDFRONT_CUSTOM_DOMAIN']

    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


    ######### Media Configurations ##########
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'


######### Crispy Forms Configurations ##########
CRISPY_TEMPLATE_PACK='bootstrap4'


######### Stripe Configurations ##########
STRIPE_SECRET_KEY = config['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY = config['STRIPE_PUBLISHABLE_KEY']
DEFAULT_TAX_RATE = 0.08 # 8% tax


######### Email Configurations ##########
DEFAULT_FROM_EMAIL = 'Cloudland Shop<cloudlandonlineshop@gmail.com>'
EMAIL_BACKEND = config['EMAIL_BACKEND']
EMAIL_HOST = config['EMAIL_HOST']
EMAIL_HOST_USER = config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
EMAIL_PORT = config['EMAIL_PORT']
EMAIL_USE_TLS = config['EMAIL_USE_TLS']