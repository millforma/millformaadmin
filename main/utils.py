import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import uuid
from random import randint
from django.utils.datetime_safe import datetime as datetime_safe


class UidMixin:
    @staticmethod
    def generate_uid(text_to_append="", salt=""):
        # pris ici : http://stackoverflow.com/questions/
        # 6999726/how-can-i-convert-a-datetime-object-to
        # -milliseconds-since-epoch-unix-time-in-p
        #
        epoch = datetime_safe.utcfromtimestamp(0)

        def millis(dt):
            return (dt - epoch).total_seconds() * 1000.0

        nom = str(randint(0, 90000000) + int(millis(datetime_safe.now())))
        return str(uuid.uuid5(uuid.NAMESPACE_OID, nom + salt)) + text_to_append

class VerificationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


generate_token = VerificationTokenGenerator()

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
