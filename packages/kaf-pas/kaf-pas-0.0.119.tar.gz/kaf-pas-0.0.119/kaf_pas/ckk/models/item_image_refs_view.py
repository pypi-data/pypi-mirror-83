import logging
import os

from django.conf import settings
from django.db.models import BooleanField, TextField

from isc_common import delete_drive_leter
from isc_common.fields.related import ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager
from kaf_pas.ckk.models.item import Item
from kaf_pas.kd.models.documents_thumb import Documents_thumb
from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10

logger = logging.getLogger(__name__)


class Item_image_refs_viewManager(AuditManager):
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
                'prompt': record.file_document,
            }
            return res
        else:
            res = {
                'deliting': record.deliting,
                'editing': record.editing,
                'file_document': record.file_document,
                'file_document_thumb_url': f'/logic/DocumentsThumb/Download/{record.thumb.id}/' if record.thumb else None,
                'id': record.thumb.id if record.thumb else None,
                'item_id': record.item.id,
                'path': record.thumb.path if record.thumb else None,
                'prompt': record.file_document,
            }
            return res


class Item_image_refs_view(AuditModel):
    item = ForeignKeyCascade(Item)
    thumb = ForeignKeyCascade(Documents_thumb, null=True, blank=True)
    thumb10 = ForeignKeyCascade(Documents_thumb10, null=True, blank=True)
    useinprint = BooleanField()
    file_document = TextField()

    objects = Item_image_refs_viewManager()

    def __str__(self):
        return f"item: {self.item}, thumb: {self.thumb}, thumb10: {self.thumb10}"

    class Meta:
        verbose_name = 'Графические элементы'
        managed = False
        db_table = 'ckk_item_image_refs_view'
