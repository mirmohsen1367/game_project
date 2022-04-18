
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from decouple import config

databases = {

    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')},


    # 'default': {
    #
    #      'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #      'NAME': config('DB_NAME'),
    #      'USER': config("DB_USER"),
    #      'PASSWORD': config("DB_PASSWORD"),
    #      'HOST': config("DB_HOST"),
    #      'PORT': '5432'},
    }
