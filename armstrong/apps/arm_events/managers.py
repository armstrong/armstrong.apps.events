from datetime import date, timedelta
from django.db import models
from django.db.models import Q


class EventManager(models.Manager):

    def upcoming(self, days=None):

        today = date.today()

        if days is None:
            query = Q(start_day__gte=today) | Q(end_day__gte=today)
        else:
            query = Q(start_day__range=(today, today + timedelta(days=days)))

        return self.filter(query, active=True)
