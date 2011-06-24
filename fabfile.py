from armstrong.dev.tasks import *

pip_install_first = True

settings = {
    'INSTALLED_APPS': (
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.auth',
        'django.contrib.sites',
        'armstrong.apps.events',
        'armstrong.apps.events.tests.events_support',
        'armstrong.core.arm_content',
    ),
    'TEMPLATE_CONTEXT_PROCESSORS': (
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',
    ),
    'ROOT_URLCONF': 'armstrong.apps.events.urls',
    'SITE_ID': 1,
}

main_app = 'events'
tested_apps = (main_app,)
