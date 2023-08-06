import logging
import os

from bitfield import BitField
from django.conf import settings
from django.db.models import UniqueConstraint, Q

from isc_common import delete_drive_leter
from isc_common.fields.related import ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditModel, AuditManager
from kaf_pas.ckk.models.item import Item
from kaf_pas.kd.models.documents_thumb import Documents_thumb
from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10

logger = logging.getLogger(__name__)


class Item_image_refsManager(AuditManager):
    @staticmethod
    def props():
        return BitField(flags=(
            ('useinprint', 'Выводим в печатную форму'),  # 1
        ), default=0, db_index=True)

    @staticmethod
    def getRecord(record):
        if settings.ENABLE_FILE_VIEW:

            file_document_names = os.path.split(record.thumb.document.file_document) if record.thumb is not None and record.thumb.document is not None else None
            if file_document_names is None:
                file_document_names = os.path.split(record.thumb.lotsman_document.document.file_document) if record.thumb is not None and record.thumb.lotsman_document is not None and record.thumb.lotsman_document.document else None

            file_document_name = file_document_names[len(file_document_names) - 1]
            file_names = delete_drive_leter(record.thumb.path).split('\\')
            file_name = file_names[len(file_names) - 1]

            file_document_path = record.thumb.document.file_document if record.thumb is not None and record.thumb.document is not None else None
            if file_document_path is None:
                file_document_path = record.thumb.lotsman_document.document.file_document if record.thumb is not None and record.thumb.lotsman_document is not None and record.thumb.lotsman_document.document is not None else None

            res = {
                'attfile_path': record.thumb.attfile.path,
                'deliting': record.deliting,
                'editing': record.editing,
                'file_document_name': file_document_name,
                'file_document_path': file_document_path,
                'file_document_thumb_url': f'/logic/DocumentsThumb/Download/{record.thumb.id}/' if record.thumb else None,
                'file_name': file_name,
                'file_path': delete_drive_leter(record.thumb.path),
                'id': record.thumb.id if record.thumb else None,
                'item_id': record.item.id,
                'path': record.thumb.path if record.thumb else None,
            }
            return res
        else:
            res = {
                'deliting': record.deliting,
                'editing': record.editing,
                'file_document_thumb_url': f'/logic/DocumentsThumb/Download/{record.thumb.id}/' if record.thumb else None,
                'id': record.thumb.id if record.thumb else None,
                'item_id': record.item.id,
                'path': record.thumb.path if record.thumb else None,
            }
            return res

    def deleteFromRequest(self, request, removed=None, ):
        from django.db import transaction

        request = DSRequest(request=request)
        res = 0

        _transaction = request.json.get('transaction')
        if _transaction:
            with transaction.atomic():
                for operation in _transaction.get('operations'):
                    data = operation.get('data')
                    for id in data.get('ids'):
                        for item in data.get('items'):
                            res += Item_image_refs.objects.filter(item_id=item.get('id'), thumb_id=id).delete()[0]
        else:
            data = request.json.get('data')
            for id in data.get('ids'):
                for item in data.get('items'):
                    if item.get('child_id'):
                        item_id = item.get('child_id')
                    else:
                        item_id = item.get('id')
                    res += Item_image_refs.objects.filter(item_id=item_id, thumb_id=id).delete()[0]
        return res


class Item_image_refs(AuditModel):
    item = ForeignKeyCascade(Item)
    thumb = ForeignKeyCascade(Documents_thumb, null=True, blank=True)
    thumb10 = ForeignKeyCascade(Documents_thumb10, null=True, blank=True)
    props = Item_image_refsManager.props()

    objects = Item_image_refsManager()

    def __str__(self):
        return f"item: {self.item}, thumb: {self.thumb}, thumb10: {self.thumb10}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['item'], condition=Q(thumb10=None) & Q(thumb=None), name='Item_image_refs_unique_constraint_0'),
            UniqueConstraint(fields=['item', 'thumb'], condition=Q(thumb10=None), name='Item_image_refs_unique_constraint_1'),
            UniqueConstraint(fields=['item', 'thumb10'], condition=Q(thumb=None), name='Item_image_refs_unique_constraint_2'),
            UniqueConstraint(fields=['item', 'thumb', 'thumb10'], name='Item_image_refs_unique_constraint_3'),
        ]
        verbose_name = 'Кросс таблица на местоположения графических элементов'
