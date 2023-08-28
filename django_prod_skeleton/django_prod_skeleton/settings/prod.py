# HERE ARE THE SETTINGS DEFINED FOR THE PRODUCTION ENVIRONMENT

import os
from .base import *

# DEBUG is set to False in the production environment since if there is an error it will show sensitive configuration information to everyone!
DEBUG = False 


# This setting is used with DEBUG = False since, if a view raises an exception, it will send an email to the people listed in the tuples
ADMINS = [
    ('Francesco F', os.environ.get('ADMIN_EMAIL'))
]

ALLOWED_HOSTS = ['your-website.com', 'www.your-website.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # here you are specifying that the db that you are using is postgresql
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db', # here we need to specify the name that is used to specify the service of the database in the yaml file 
        'PORT': 5432,
    }
}

REDIS_URL = 'redis://cache:6379' # cache is the name that we used to define the cache service and 6379 is the default port used by Redis!
CACHES['default']['LOCATION'] = REDIS_URL


# Settings added to remove the security problems that you can see passing python manage.py check --deploy --settings=django_prod_skeleton.settings.prod
CSRF_COOKIE_SECURE = True 
SESSION_COOKIE_SECURE = True 
SECURE_SSL_REDIRECT = True 



