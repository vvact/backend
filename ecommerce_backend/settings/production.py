# ecommerce_backend/settings/production.py
from .base import *
import os
from dotenv import load_dotenv
load_dotenv()

# production.py
from decouple import config  # or use os.getenv if you prefer

DEBUG = False

# Always load this from .env in production
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split()





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("PG_HOST", "db"),
        'PORT': os.getenv("PG_PORT", "5432"),
    }
}



DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}