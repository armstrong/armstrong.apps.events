from datetime import datetime, date, time, timedelta
from django.db import models
from django.db.models import Q


class EventManager(models.Manager):

    def upcoming(self, days=None):

        today = datetime.combine(date.today(), time())
        tmrw = today + timedelta(days=1)

        if days is None:
            query = Q(end_date__gte=today)
        else:
            query = Q(end_date__range=(today, tmrw + timedelta(days=days)))

        return self.filter(query, active=True)
