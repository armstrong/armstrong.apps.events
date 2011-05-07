from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from armstrong.apps.arm_events.models import Event
from armstrong.apps.arm_events.views import RSVPCreateView


urlpatterns = patterns('',

    url(r'^$', ListView.as_view(queryset=Event.on_site.upcoming()),
            name='event_list'),

    url(r'^(?P<slug>[-\w]+)/$', DetailView.as_view(model=Event,
            queryset=Event.on_site.all()), name='event_detail'),

    url(r'^(?P<event_slug>[-\w]+)/rsvp/$', RSVPCreateView.as_view(),
            name='rsvp_create'),

    url(r'^(?P<slug>[-\w]+)/rsvp/success/$', DetailView.as_view(
            queryset=Event.on_site.all(),
            template_name='arm_events/rsvp_success.html'
    ), name='rsvp_success'),

)
