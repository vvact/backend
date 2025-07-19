# ecommerce_backend/settings/production.py
from .base import *
# production.py
from decouple import config  # or use os.getenv if you prefer

DEBUG = False

# Always load this from .env in production
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split()



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'db', 
        'PORT': '5432',
    }
}


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}