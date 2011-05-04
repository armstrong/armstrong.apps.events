from datetime import datetime, time
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from armstrong.apps.arm_events.managers import EventManager

class BaseEvent(models.Model):

    sites = models.ManyToManyField(Site)
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_day = models.DateField(db_index=True)
    start_time = models.TimeField(null=True, blank=True)
    end_day = models.DateField(db_index=True, null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    website = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    has_rsvp = models.BooleanField(default=False)

    objects = EventManager()

    class Meta:
        abstract = True
        ordering = ['start_day']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug':self.slug})

    @property
    def has_passed(self):
        if self.end_day:
            end = datetime.combine(self.end_day, self.end_time
                    if self.end_time else time(23,59))
        else:
            end = datetime.combine(self.start_day, time(23,59))

        return datetime.now() > end

class Event(BaseEvent):
    pass

class BaseRSVP(models.Model):

    event = models.ForeignKey(Event, related_name='events')
    email = models.EmailField()
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s - %s' % (self.event.start_day, self.email)

class RSVP(BaseRSVP):
    pass
