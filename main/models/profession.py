from django.db import models
from django.utils.functional import cached_property

from main.models.activity import Activity
from main.models.activity_type import ActivityType


class ProfessionManager(models.Manager):
    @cached_property
    def activity_type_profession(self):
        try:
            return ActivityType.objects.get(name=ActivityType.PROFESSION_TYPE)
        #   except ActivityType.DoesNotExist:
        #   return None
        # It's ugly, but when doing migrations if ActivityType is not created
        # there's an exception only known by psycopg2...
        # -> uncomment this instead for the time of migrations *ONLY*:
        except:
           return None

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(activity_type=self.activity_type_profession)
        )


class Profession(Activity):
    class Meta:
        proxy = True

    objects = ProfessionManager()

    def __str__(self):
        return f"{self.str_clean(self.name)}"

