import random
from django.test import TestCase as DjangoTestCase
from django.test.client import RequestFactory
from ..models import Event

def generate_random_event(start_day):
    slug = 'random-slug-%s' % random.randint(100,1000)
    title = 'Random title %s' % random.randint(100,1000)
    location = 'Random lugar %s' % random.randint(100,1000)
    return Event.objects.create(slug=slug, title=title, start_day=start_day,
            location=location)

class TestCase(DjangoTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def assertInContext(self, var_name, other, template_or_context):
        # TODO: support passing in a straight "context" (i.e., dict)
        context = template_or_context.context_data
        self.assertTrue(var_name in context,
                msg="`%s` not in provided context" % var_name)
        self.assertEqual(context[var_name], other)
