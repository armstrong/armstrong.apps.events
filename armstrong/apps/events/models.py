from datetime import datetime, time, timedelta
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from armstrong.core.arm_content.mixins.publication import PublicationMixin
from .managers import EventManager, CurrentSiteEventManager


class BaseEvent(PublicationMixin):

    slug = models.SlugField()
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    all_day = models.BooleanField(default=False)
    website = models.URLField(blank=True)
    has_rsvp = models.BooleanField(default=False)

    objects = EventManager()
    on_site = CurrentSiteEventManager()

    class Meta:
        abstract = True
        ordering = ['start_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.all_day:
            self.start_date = datetime.combine(self.start_date.date(), time())
            self.end_date = datetime.combine(self.end_date.date(),
                    time(23, 59))

        super(BaseEvent, self).save(*args, **kwargs)

        if not self.sites.exists():
            self.sites.add(Site.objects.get_current())

    @property
    def has_passed(self):
        return datetime.now() > self.end_date


class Event(BaseEvent):
    pass


class BaseRSVP(models.Model):

    event = models.ForeignKey(Event, related_name='events')
    email = models.EmailField()
    name = models.CharField(max_length=50)
    guests = models.PositiveSmallIntegerField(blank=True, null=True,
            choices=[(i, i) for i in range(11)], default=0)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s - %s' % (self.event.start_date, self.email)


class RSVP(BaseRSVP):
    pass
