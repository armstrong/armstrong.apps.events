import random
from datetime import date, timedelta, datetime
from django.core.urlresolvers import reverse
from ._utils import generate_random_event, TestCase
from ..models import Event


class EventManagerTestCase(TestCase):
    def setUp(self):
        self.event1 = generate_random_event(date.today() + timedelta(days=5))
        self.event2 = generate_random_event(date.today() - timedelta(days=5))

    def test_upcoming_basic(self):
        self.assertTrue(self.event1 in Event.objects.upcoming())
        self.assertTrue(self.event2 not in Event.objects.upcoming())

    def test_upcoming_ignore_times(self):
        # start times shouldn't matter
        self.event1.start_time = (datetime.now() - timedelta(hours=2)).time()
        self.event1.save()
        self.assertEqual(len(Event.objects.upcoming()), 1)

        self.event2.start_time = (datetime.now() + timedelta(hours=1)).time()
        self.event2.save()
        self.assertEqual(len(Event.objects.upcoming()), 1)

        # end times shouldn't matter
        self.event1.end_time = (datetime.now() - timedelta(hours=1)).time()
        self.event1.save()
        self.assertEqual(len(Event.objects.upcoming()), 1)

        self.event2.end_time = (datetime.now() + timedelta(hours=2)).time()
        self.event2.save()
        self.assertEqual(len(Event.objects.upcoming()), 1)

    def test_upcoming_today(self):
        self.event1.start_day = date.today()
        self.event1.save()
        self.assertTrue(self.event1 in Event.objects.upcoming())
        self.assertTrue(self.event1 in Event.objects.upcoming(days=0))

    def test_upcoming_span(self):
        self.event1.start_day = date.today() - timedelta(days=1)
        self.event1.end_day = date.today()
        self.event1.save()
        self.assertTrue(self.event1 in Event.objects.upcoming())

    def test_upcoming_asc_order(self):
        events = [generate_random_event(date.today() + \
                timedelta(days=random.randint(0,10))) for i in range(10)]

        upcoming = list(Event.objects.upcoming())
        self.assertTrue(upcoming == sorted(upcoming, key=lambda e: e.start_day))

    def test_upcoming_days(self):
        self.assertEqual(len(Event.objects.upcoming(days=10)), 1)
        self.assertTrue(self.event1 in Event.objects.upcoming(days=6))
        self.assertTrue(self.event1 in Event.objects.upcoming(days=5))
        self.assertFalse(self.event1 in Event.objects.upcoming(days=4))

