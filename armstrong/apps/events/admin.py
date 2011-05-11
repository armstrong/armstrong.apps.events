from django.contrib import admin
from armstrong.apps.events.models import Event, RSVP

admin.site.register(Event)
admin.site.register(RSVP)
