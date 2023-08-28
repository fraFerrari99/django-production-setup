# THIS IS THE FILE THAT CONTAINS THE SETTINGS FOR THE LOCAL ENVIRONMENT
from .base import *  # import all the common settings defined in the base.py file

DEBUG = True # debug is set to True since it is the local environment 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}