from ._utils import *

@task
def pep8():
    local('find ./armstrong -name "*.py" | xargs pep8', capture=False)


@task
def test():
    settings = {
        'INSTALLED_APPS': (
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.auth',
            'django.contrib.sites',
            'armstrong.apps.arm_events',
            'armstrong.apps.arm_events.tests.arm_events_support',
        ),
        'TEMPLATE_CONTEXT_PROCESSORS': (
            'django.core.context_processors.request',
            'django.contrib.auth.context_processors.auth',
        ),
        'ROOT_URLCONF': 'armstrong.apps.arm_events.urls',
    }
    with html_coverage_report():
        run_tests(settings, 'arm_events', 'arm_events_support')
