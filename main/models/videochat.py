from django.contrib.auth.models import User
from django.db import models
from main.models.base import BaseModel


class VideoChat(BaseModel):
    session = models.IntegerField(default=1,blank=True,null=True)
    date_link_sent = models.DateField(auto_now_add=True)
    formation_session = models.ForeignKey(to='main.FormationSession', on_delete=models.DO_NOTHING, default=None)

    created_by = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, default=None, blank=True, null=True)
    date_start = models.DateField(default=None, blank=False, null=False)
    time_start = models.TimeField(default=None, blank=False, null=False)
    date_end = models.DateField(default=None, blank=False, null=False)
    time_end = models.TimeField(default=None,blank=False,null=False)
    title = models.CharField(max_length=200, unique=True, default="", null=True, blank=True)

    finished_session = models.BooleanField(default=False)

    def __str__(self):
        return 'video session {} for  {}'.format(self.session, self.formation_session.name)

    def get_last(formation):
        result = VideoChat.objects.filter(formation_session=formation).last()
        return result
