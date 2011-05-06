from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from ._utils import generate_random_event, TestCase, hours_ago, hours_ahead
from ..models import Event, RSVP


class EventViewTestCase(TestCase):

    def setUp(self):
        self.c = Client()

    def test_event_detail(self):
        event = generate_random_event(hours_ago(1), hours_ahead(1))
        response = self.c.get(event.get_absolute_url())
        self.assertEqual(response.context['event'], event)

    def test_event_list(self):
        event0 = generate_random_event(hours_ago(1), hours_ahead(1))
        event1 = generate_random_event(hours_ahead(2), hours_ahead(3))
        response = self.c.get(reverse('event_list'))

        self.assertEqual(list(response.context['event_list']),
                list(Event.objects.upcoming()))


class RSVPViewTestCase(TestCase):
    def setUp(self):
        self.event = generate_random_event(hours_ago(1), hours_ahead(1))
        self.c = Client()

    def test_create_form(self):
        response = self.c.get(reverse('rsvp_create',
                kwargs={'event_slug': self.event.slug}))

        self.assertTrue('form' in response.context)

    def test_create_form_logged_in(self):
        user = User.objects.create_user('jimi', 'jimi@armstrongcms.org',
               'experience')
        user.first_name = 'jimi'
        user.last_name = 'hendrix'
        user.save()

        self.c.login(username='jimi', password='experience')
        response = self.c.get(reverse('rsvp_create',
                kwargs={'event_slug': self.event.slug}))

        self.assertTrue('form' in response.context)
        self.assertContains(response, user.email)
        self.assertContains(response, user.first_name)

    def test_submit_form(self):
        data = {'name': 'bob dylan', 'email': 'bob@armstrongcms.org',
                'event': self.event.id}
        post = self.c.post(reverse('rsvp_create',
                kwargs={'event_slug': self.event.slug}), data, follow=True)

        self.assertTrue('rsvp success' in post.content)
        self.assertTrue(self.event.title in post.content)
        self.assertTrue(RSVP.objects.get(email='bob@armstrongcms.org'))
