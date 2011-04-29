from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse
from ._utils import generate_random_event, TestCase
from ..models import Event, RSVP


class EventViewTestCase(TestCase):
    def setUp(self):
        self.event1 = generate_random_event(date.today() + timedelta(days=5))
        self.event2 = generate_random_event(date.today() - timedelta(days=5))
        self.c = Client()

    def test_event_detail(self):
        response = self.c.get(self.event1.get_absolute_url())
        self.assertEqual(response.context['event'], self.event1)

    def test_event_list(self):
        response = self.c.get(reverse('event_list'))
        self.assertEqual(list(response.context['event_list']),
                list(Event.objects.upcoming()))

class RSVPViewTestCase(TestCase):
    def setUp(self):
        self.event = generate_random_event(date.today() + timedelta(days=5))

        user = User.objects.create_user('jimi', 'jimi@armstrongcms.org',
               'experience')
        user.first_name = 'jimi'
        user.last_name = 'hendrix'
        user.save()
        self.user = user

        self.c = Client()

    def test_create_form(self):
        response = self.c.get(reverse('rsvp_create',
                kwargs={'slug': self.event.slug}))

        self.assertTrue('form' in response.context)

    def test_create_form_logged_in(self):
        self.c.login(username='jimi', password='experience')
        response = self.c.get(reverse('rsvp_create',
                kwargs={'slug': self.event.slug}))

        self.assertTrue('form' in response.context)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.first_name)

    def test_submit_form(self):
        data = {'name': 'bob dylan', 'email': 'bob@armstrongcms.org',
                'event': self.event.id}
        post = self.c.post(reverse('rsvp_create',
                kwargs={'slug': self.event.slug}), data, follow=True)

        self.assertTrue('rsvp success' in post.content)
        self.assertTrue(self.event.title in post.content)
        self.assertTrue(RSVP.objects.get(email='bob@armstrongcms.org'))
