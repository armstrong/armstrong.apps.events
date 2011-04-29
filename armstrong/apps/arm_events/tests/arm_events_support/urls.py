from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^profiles/', include('armstrong.core.arm_profiles.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
