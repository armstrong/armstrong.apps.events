from datetime import datetime, timedelta, date, time
import random
from django.test import TestCase as DjangoTestCase
from django.test.client import RequestFactory
from ..models import Event

def hours_ago(num):
    return datetime.now() - timedelta(hours=num)

def hours_ahead(num):
    return datetime.now() + timedelta(hours=num)

def start_of_day():
    return datetime.combine(date.today(), time())

def end_of_day():
    return datetime.combine(date.today(), time(23, 59))

def generate_random_event(start_date, end_date):
    slug = 'random-slug-%s' % random.randint(100,1000)
    title = 'Random title %s' % random.randint(100,1000)
    location = 'Random lugar %s' % random.randint(100,1000)
    return Event.objects.create(slug=slug, title=title, start_date=start_date,
            end_date=end_date, location=location)

class TestCase(DjangoTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def assertInContext(self, var_name, other, template_or_context):
        # TODO: support passing in a straight "context" (i.e., dict)
        context = template_or_context.context_data
        self.assertTrue(var_name in context,
                msg="`%s` not in provided context" % var_name)
        self.assertEqual(context[var_name], other)
