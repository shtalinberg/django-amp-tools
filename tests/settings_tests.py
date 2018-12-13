import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
join_to_project = lambda slug: os.path.join(PROJECT_ROOT, slug)

SECRET_KEY = 'amp-tools-key'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'amp_tools',
]


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        join_to_project('templates'),
    ],
    # 'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            "django.contrib.auth.context_processors.auth",
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.request',
            'django.template.context_processors.media',
        ],
        'loaders': [
            'amp_tools.loader.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
    },
}]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'amp_tools.middleware.AMPDetectionMiddleware',
)


TEST_RUNNER = 'django.test.runner.DiscoverRunner'
RUNTESTS_DIR = os.path.abspath(os.path.dirname(__file__))
