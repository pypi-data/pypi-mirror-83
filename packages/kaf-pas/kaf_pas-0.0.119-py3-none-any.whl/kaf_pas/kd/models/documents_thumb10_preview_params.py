import logging

from django.db.models import TextField, SmallIntegerField, PositiveIntegerField

from isc_common.auth.models.user import User
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10

logger = logging.getLogger(__name__)


class Documents_thumb10_preview_paramsQuerySet(AuditQuerySet):
    pass


class Documents_thumb10_preview_paramsManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Documents_thumb10_preview_paramsQuerySet(self.model, using=self._db)


class Documents_thumb10_preview_params(AuditModel):
    http_user_agent = TextField()
    remote_addr = TextField()
    height = PositiveIntegerField()
    width = PositiveIntegerField()
    thumb10 = ForeignKeyProtect(Documents_thumb10)
    user = ForeignKeyCascade(User)

    objects = Documents_thumb10_preview_paramsManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Параметры просмотров'
        unique_together = (('http_user_agent', 'remote_addr', 'thumb10', 'user'),)
