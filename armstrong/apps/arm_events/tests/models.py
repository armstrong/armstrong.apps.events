import random
from datetime import date, timedelta, datetime
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from ._utils import generate_random_event, TestCase
from ..models import Event


class EventTestCase(TestCase):
    def setUp(self):
        self.event1 = generate_random_event(date.today() + timedelta(days=5))
        self.event2 = generate_random_event(date.today() - timedelta(days=5))
        self.ONE_HOUR_AGO = (datetime.now() - timedelta(hours=1)).time()
        self.TWO_HOURS_AGO = (datetime.now() - timedelta(hours=2)).time()

    def test_get_absolute_url(self):
        self.assertEqual(self.event1.get_absolute_url(), '/%s/' % self.event1.slug)

    def test_has_passed_without_times(self):
        self.assertFalse(self.event1.has_passed)
        self.assertTrue(self.event2.has_passed)

    def test_has_passed_today(self):
        self.event1.start_day = date.today()
        self.assertFalse(self.event1.has_passed)

    def test_has_passed_ignore_start_time(self):
        self.event1.start_day = date.today()
        self.event1.start_time = self.ONE_HOUR_AGO
        self.assertFalse(self.event1.has_passed)

    def test_has_passed_honor_end_time(self):
        self.event1.start_day = date.today()
        self.event1.start_time = self.TWO_HOURS_AGO
        self.event1.end_day = date.today()
        self.event1.end_time = self.ONE_HOUR_AGO
        self.assertTrue(self.event1.has_passed)
