from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from .models import Event, RSVP
from .forms import RSVPCreateForm


class RSVPCreateView(CreateView):

    model = RSVP
    form_class = RSVPCreateForm

    def get_success_url(self):

        return reverse('rsvp_success',
                kwargs={'slug': self.kwargs['event_slug']})

    def get_initial(self):

        event = get_object_or_404(Event, slug=self.kwargs['event_slug'],
                sites__in=[Site.objects.get_current()])

        self.initial['event'] = event.id

        if self.request.user.is_authenticated():
            self.initial['email'] = self.request.user.email
            self.initial['name'] = self.request.user.get_full_name()

        return self.initial
