from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from main.models import EventAbstract
from main.models.formationsession import FormationSession
from main.models.person import Person
from main.models.videochat import VideoChat


class EventManager(models.Manager):
    """ Event manager """
    def get_all_events(self, user):
        events=None
        if user.groups.filter(name='teacher').exists():
            events = Event.objects.filter(
                teacher=user, is_active=True, is_deleted=False)

        elif user.groups.filter(name='learner').exists():
            events = Event.objects.filter(
                trainee__user_id=user.id, is_active=True, is_deleted=False)

        return events

    def get_running_events(self, user):
        running_events=None
        if user.groups.filter(name='teacher').exists():
            running_events = Event.objects.filter(
                teacher=user, is_active=True, is_deleted=False,start_time__lte=datetime.now(),
                end_time__gte=datetime.now()
            ).order_by('start_time')

        elif user.groups.filter(name='learner').exists():
            running_events = Event.objects.filter(
                trainee__user_id=user.id, is_active=True, is_deleted=False,start_time__lte=datetime.now(),
                end_time__gte=datetime.now()
            ).order_by('start_time')

        return running_events

    def get_next_events(self, user):
        next_events=None
        if user.groups.filter(name='teacher').exists():
            next_events = Event.objects.filter(
                teacher=user, is_active=True, is_deleted=False,
                start_time__gte=datetime.now()
            ).order_by('start_time')

        elif user.groups.filter(name='learner').exists():
            now = datetime.now().date()

            next_events = Event.objects.filter(
                trainee__user_id=user.id, is_active=True, is_deleted=False,
                start_time__gt=datetime.now()
            ).order_by('start_time')

        return next_events



class Event(EventAbstract):
    """ Event model """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events'
    )
    trainee = models.ManyToManyField(Person, related_name="trainee")
    teacher = models.ForeignKey(to=User, limit_choices_to={'groups__name': "teacher"}, on_delete=models.DO_NOTHING,
                                default=None, blank=True,null=True)
    title = models.CharField(max_length=200, unique=True,default="",null=True,blank=True)
    description = models.TextField()
    formation_session = models.ForeignKey(FormationSession, on_delete=models.CASCADE)
    video_chat=models.ForeignKey(VideoChat,on_delete=models.DO_NOTHING, default=None, blank=True,null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    objects = EventManager()



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ScheduleCalendar:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('ScheduleCalendar:event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
