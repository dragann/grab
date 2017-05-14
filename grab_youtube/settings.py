import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'grab_youtube', 'grab', 'static'))
STATIC_URL = '/static/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(cr4)i1tsdfi(7muwspi=&xk+6h6sm)wx9-b+q!bf3k@^lax*0'

DEBUG = True

ALLOWED_HOSTS = []

THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_STORAGE = 'django.core.files.storage.FileSystemStorage'
THUMBNAIL_URL_TIMEOUT = 10

CACHES = {
   'default': {
       # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
       'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       'LOCATION': 'redis://127.0.0.1:6379/4',
       'TIMEOUT': 60*60*24*30
   }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grab_youtube.account',
    'grab_youtube.grab',
    'grab_youtube.videos',
    'social_django',
    'sorl.thumbnail',
    'bootstrap_pagination',
    'cache_tagging.django_cache_tagging',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'grab_youtube.grab.stats_middleware.StatsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'grab_youtube.account.middleware.AccountMiddleware',
    'bootstrap_pagination.middleware.PaginationMiddleware',
    'grab_youtube.grab.middleware.ExceptionMiddleware'
)

ROOT_URLCONF = 'grab_youtube.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'grab_youtube.grab.context_processors.alert_badges'
            ],
            # 'loaders': [
            #     ('django.template.loaders.cached.Loader', (
            #         'django.template.loaders.app_directories.Loader',
            #     )),
            # ]
        },
    },
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
    'grab_youtube.account.pipeline.save_profile',
)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'grab_youtube.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.mysql',
        'NAME': 'grab_dev',
        'USER': 'grab_dev',
        'PASSWORD': 'dev',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': 60
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_friends', 'user_posts']
SOCIAL_AUTH_ALWAYS_ASSOCIATE = True

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'user_detail'

from local_settings import *