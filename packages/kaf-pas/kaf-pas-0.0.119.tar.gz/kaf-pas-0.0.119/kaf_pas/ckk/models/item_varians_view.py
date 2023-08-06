import logging

from django.conf import settings
from django.db.models import BooleanField, PositiveIntegerField, BigIntegerField

from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditManager, AuditQuerySet, AuditModel
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_refs import Item_refsManager

logger = logging.getLogger(__name__)


class Item_varians_viewQuerySet(AuditQuerySet):
    def get_range_rows1(self, request, function=None, distinct_field_names=None, remove_fields=None):
        request = DSRequest(request=request)
        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            distinct_field_names=distinct_field_names,
            json=request.json,
            criteria=request.get_criteria()
        )
        return res

class Item_varians_viewManager(AuditManager):

    @staticmethod
    def fullRows(suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_item_variant_view_grid}{suffix}')

    @staticmethod
    def refreshRows(ids):
        if isinstance(ids, int):
            ids = [ids]
        records = [Item_varians_viewManager.getRecord(record) for record in Item_varians_view.objects.filter(id__in=ids)]
        WebSocket.row_refresh_grid(grid_id=settings.GRID_CONSTANTS.refresh_item_variant_view_grid_row, records=records)

    @staticmethod
    def getRecord(record):
        from kaf_pas.ckk.models.item_line import Item_lineManager
        res = {
            "child_id": record.child.id,
            "confirmed": record.confirmed,
            "deliting": record.deliting,
            "editing": record.editing,
            "id": record.id,
            "isLotsman": record.isLotsman,
            "item_id": record.item.id,
            "item_props": record.item.props,
            "lastmodified": record.lastmodified,
            "parent_id": record.parent.id,
            "qty_operations": record.qty_operations,
            "refs_props": record.refs_props,
            "relevant": record.relevant,
            "section": record.section,
            "section_num": record.section_num,
            "STMP_1_value_str": record.STMP_1_value_str,
            "STMP_1_id": record.STMP_1_id,
            "STMP_2_value_str": record.STMP_2_value_str,
            "STMP_2_id": record.STMP_2_id,
            "version": record.version,
            "where_from": record.where_from,
            'icon': Item_lineManager.getIcon(record),
        }
        return res

    def get_queryset(self):
        return Item_varians_viewQuerySet(self.model, using=self._db)


class Item_varians_view(AuditModel):
    child = ForeignKeyCascade(Item, related_name='Item_varians_view_child')
    confirmed = NameField()
    isFolder = BooleanField()
    isLotsman = BooleanField()
    item = ForeignKeyCascade(Item, related_name='Item_varians_view_item')
    parent = ForeignKeyCascade(Item, related_name='Item_varians_view_parent')
    qty_operations = PositiveIntegerField()
    refs_props = Item_refsManager.props()
    relevant = NameField()
    section = CodeField(null=True, blank=True)
    section_num = PositiveIntegerField(default=0)
    STMP_1_value_str = NameField()
    STMP_1_id = BigIntegerField()
    STMP_2_value_str = NameField()
    STMP_2_id = BigIntegerField()
    version = PositiveIntegerField(null=True, blank=True)
    where_from = NameField()

    objects = Item_varians_viewManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Варианты для конфигуратора'
        managed = False
        db_table = 'ckk_item_varians_view'
