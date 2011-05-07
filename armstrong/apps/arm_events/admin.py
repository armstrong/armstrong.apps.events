from django.contrib import admin
from armstrong.apps.arm_events.models import Event, RSVP

admin.site.register(Event)
admin.site.register(RSVP)
