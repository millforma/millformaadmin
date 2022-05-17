from .document import DocumentFile
from django.db import models

from ..formationsession import FormationSession


class BillDocument(DocumentFile):
    formation_session=models.ForeignKey(to=FormationSession,on_delete=models.DO_NOTHING)
    num_bill = models.AutoField(primary_key=True)
    date_bill_sent = models.DateField(auto_now=True)
    date_bill_paid = models.DateField(auto_now=False, null=True, blank=True)
    amount_paid = models.IntegerField(default=0)
    bill_paid = models.BooleanField(default=False)
