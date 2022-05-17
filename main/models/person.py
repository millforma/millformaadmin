import uuid

from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

from main.models.base import BaseModel
from main.models.entity import Entity
from main.models.file.image import ImageFile
from main.models.profession import Profession
from main.models.activity import ActivityType



class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_physical=True)


class Person(Entity):
    objects = PersonManager()
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE
    )
    professions = models.ManyToManyField(
        Profession, related_name="persons", through="PersonProfession"
    )
    avatar = models.ForeignKey(
        ImageFile,
        default=None,
        blank=True,
        null=True,
        related_name="persons",
        on_delete=models.SET_NULL,
    )
    language = models.CharField(max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)

    doc_is_valid=models.BooleanField(null=True)


    def avatar_url_thumbnail(self):
        if self.avatar:
            return self.avatar.url_thumbnail()
        return static(settings.IMG_NO_IMAGE_YET)

    description = models.TextField(blank=True, null=True, default=None)

    def as_person_typed(self):
        return self.persontyped if hasattr(self, "persontyped") else None

    def user_informations_simple(self):
        u = self.user
        result = " ".join([u.first_name or "", u.last_name or ""]).strip()
        if not result:
            result = u.username.capitalize()
        return result

    def user_informations(self, email=True, active=False, pk=False):
        u = self.user
        if u is None:
            return str(_("(no user)"))
        if active:
            is_active = _("(active)") if u.is_active else _("(not active)")
        else:
            is_active = ""
        _pk = f"{self.pk} -" if pk else ""
        n = " ".join([u.first_name, u.last_name]).strip()
        if n:
            return f"{_pk} {n} {is_active}".strip()
        if not email:
            return f"{_pk} {u.username} {is_active}".strip()
        email = "({})".format(u.email if u.email else _("no email"))
        return f"{_pk} {u.username} {email} {is_active}".strip()

    def __str__(self):
        def g(value, add_after=None):
            if not add_after:
                return value if value else ""
            return "{}{}".format(
                value if value else "", add_after if value.strip() else ""
            )

        try:
            u = self.user
        except User.DoesNotExist:
            return str(_("(no user)"))

        n = " ".join([g(u.first_name), g(u.last_name)]).strip()
        n = "{}{}{}".format(u.username, " / " if n else "", n).strip()
        return "{}{} - n.{}".format(
            g(n, " - "), u.email if u.email else _("(no email)"), str(self.pk)
        )



class PersonProfession(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person.user_informations()} - ({str(self.profession)})"


class PersonConfirmation(BaseModel):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="person_confirmation"
    )
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    used = models.BooleanField(default=False)





@receiver(post_save, sender=User)
def my_post_save_user_handler(sender, instance, created, **kwargs):
    if created:  # a User = physical -> create the associated person:
        Person.objects.create(user=instance, is_physical=True)
