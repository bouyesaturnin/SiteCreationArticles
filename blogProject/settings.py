from pathlib import Path
import os
from dotenv import load_dotenv

# 1. Configuration initiale 🏠
load_dotenv() 
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Sécurité et Debug 🛡️
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

# Gestion propre des hôtes
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else:
    # Remplace par ton domaine final plus tard
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com', '.railway.app']

# 3. Définition des Applications 📦
INSTALLED_APPS = [
    'cloudinary_storage', # DOIT être avant staticfiles
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Bibliothèques tierces
  
    'corsheaders',
 
    'rest_framework_simplejwt', # Ajouté car utilisé dans REST_FRAMEWORK

    # Vos applications (Remplace 'api' par le nom exact de ton dossier app)
    'cloudinary',               # Peut être après
    'rest_framework',
    'articles',
]

# 4. Middleware ⚙️
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # INDISPENSABLE pour servir les fichiers CSS/JS en production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogProject.urls'

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

WSGI_APPLICATION = 'blogProject.wsgi.application'

# 5. Base de données 🗄️
# Note: On passera à PostgreSQL plus tard lors du déploiement réel
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 6. REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6
}

# 7. Internationalisation 🌍
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 8. Fichiers Statiques et Médias (Cloudinary) 🖼️
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Où Django collectera les fichiers pour la prod
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration Médias avec Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}



# 2. Assure-toi que ces lignes sont bien présentes AUSSI
# 9. Configuration CORS 🌐
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # Port par défaut de Vite
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'