from django.contrib.auth.models import User
from django.db import models
from main.models import EventAbstract, Event


class EventMember(EventAbstract):
    """ Event member model """
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='events'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='event_members'
    )

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.user)
