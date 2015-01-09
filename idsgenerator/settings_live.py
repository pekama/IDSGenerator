from settings import *

STATIC_FILES_BUCKET = "idsgenerator-static"
MEDIA_FILES_BUCKET = "idsgenerator-media"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': "NOyGCLCjmj",
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}

STATIC_URL = 'https://d3j11yi9yumry9.cloudfront.net/'
MEDIA_URL = 'http://d1aeaxmvezevkq.cloudfront.net/'
STATICFILES_STORAGE = 'idsgenerator.aws.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'idsgenerator.aws.MediaFilesStorage'