import logging

from django.conf import settings
from django.db.models import BigIntegerField, BooleanField, PositiveIntegerField

from isc_common import setAttr, delAttr
from isc_common.auth.models.user import User
from isc_common.datetime import DateToStr
from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditQuerySet, AuditManager
from isc_common.models.base_ref import Hierarcy
from isc_common.number import DelProps
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.item import Item_add, ItemManager, Item
from kaf_pas.ckk.models.item_line import Item_lineManager
from kaf_pas.ckk.models.item_refs import Item_refsManager, Item_refs
from kaf_pas.kd.models.document_attributes import Document_attributes
from kaf_pas.kd.models.documents import Documents

logger = logging.getLogger(__name__)


class Item_operations_viewQuerySet(AuditQuerySet):
    def raw(self, raw_query, params=None, translations=None, using=None, function=None):
        queryResult = super().raw(raw_query=raw_query, params=params, translations=translations, using=using)
        if function:
            res = [function(record) for record in queryResult]
            return res
        else:
            return queryResult


class Item_operations_viewManager(AuditManager):
    @staticmethod
    def refreshRows(ids):
        if isinstance(ids, int):
            ids = [ids]
        records = [Item_operations_viewManager.getRecord(record) for record in Item_operations_view.objects.filter(id__in=ids)]
        WebSocket.row_refresh_grid(grid_id=settings.GRID_CONSTANTS.refresh_production_order_item_grid_row, records=records)

    @staticmethod
    def fullRows(suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_production_order_item_grid}{suffix}')

    def updateFromRequest(self, request, removed=None, function=None):
        request = DSRequest(request=request)

        data = request.get_data()
        refs_id = data.get('refs_id')
        launch_detail_id = data.get('launch_detail_id')
        delAttr(data, 'launch_detail_id')
        refs_props = data.get('refs_props')
        if data.get('used') == True:
            refs_props |= Item_refs.props.used
        else:
            refs_props &= ~Item_refs.props.used

        refs_data = dict()
        setAttr(refs_data, 'props', refs_props)

        Item_refs.objects.update_or_create(id=refs_id, defaults=refs_data)

        _data = ItemManager.rec(data.copy())
        setAttr(_data, 'launch_detail_id', launch_detail_id)
        update_dict = dict(
            STMP_1_id=_data.get('STMP_1_id'),
            STMP_2_id=_data.get('STMP_2_id'),
            version=_data.get('version'),
            document_id=_data.get('document_id'),
            lotsman_document_id=_data.get('lotsman_document_id'),
            lotsman_type_id=_data.get('lotsman_type_id'),
            creator_id=Item.objects.get(id=_data.get('id')).creator.id,
        )
        Item.objects.filter(id=_data.get('id')).update(**update_dict)

        return data

    @staticmethod
    def getRecord(record):
        res = {
            'confirmed': record.confirmed,
            # 'creator_id': record.creator.id,
            'deliting': record.deliting,
            'document__file_document': record.document.file_document if record.document else None,
            'document_id': record.document.id if record.document else None,
            'editing': record.editing,
            'icon': Item_lineManager.getIcon(record),
            'id': record.id,
            'isFolder': record.isFolder,
            'lastmodified': DateToStr(record.lastmodified, mask='%Y-%m-%dT%H:%M:%S'),
            'parent_id': record.parent_id,
            'props': record.props,
            'qty_operations': record.qty_operations,
            'refs_id': record.refs_id,
            'refs_props': record.refs_props,
            'relevant': record.relevant,
            'section': record.section,
            'STMP_1__value_str': record.STMP_1.value_str if record.STMP_1 else None,
            'STMP_1_id': record.STMP_1.id if record.STMP_1 else None,
            'STMP_2__value_str': record.STMP_2.value_str if record.STMP_2 else None,
            'STMP_2_id': record.STMP_2.id if record.STMP_2 else None,
            'used': record.refs_props.used,
            'version': record.version,
            'where_from': record.where_from,
        }
        # print(res)
        return DelProps(res)

    @staticmethod
    def getRecord1(record):
        item_refs = Item_refs.objects1.get(id=record.refs_id)
        res = {
            'confirmed': record.confirmed,
            # 'creator_id': record.creator.id,
            'deliting': record.deliting,
            'document__file_document': record.document.file_document if record.document else None,
            'document_id': record.document.id if record.document else None,
            'editing': record.editing,
            'icon': Item_lineManager.getIcon(record),
            'id': record.id,
            'isFolder': record.isFolder,
            'lastmodified': DateToStr(record.lastmodified, mask='%Y-%m-%dT%H:%M:%S'),
            'parent_id': record.parent_id,
            'props': record.props,
            'qty_operations': record.qty_operations,
            'refs_id': record.refs_id,
            'refs_props': item_refs.props,
            'relevant': record.relevant,
            'section': record.section,
            'STMP_1__value_str': record.STMP_1.value_str if record.STMP_1 else None,
            'STMP_1_id': record.STMP_1.id if record.STMP_1 else None,
            'STMP_2__value_str': record.STMP_2.value_str if record.STMP_2 else None,
            'STMP_2_id': record.STMP_2.id if record.STMP_2 else None,
            'used': item_refs.props.used,
            'version': record.version,
            'where_from': record.where_from,
        }
        # print(res)
        return DelProps(res)

    def get_queryset(self):
        return Item_operations_viewQuerySet(self.model, using=self._db)


class Item_operations_view(Hierarcy):
    confirmed = NameField()
    # creator = ForeignKeyProtect(User)
    document = ForeignKeyProtect(Documents, verbose_name='Документ', null=True, blank=True)
    props = Item_add.get_prop_field()
    qty_operations = PositiveIntegerField()
    refs_id = BigIntegerField()
    refs_props = Item_refsManager.props()
    relevant = NameField()
    section = CodeField(null=True, blank=True)
    STMP_1 = ForeignKeyProtect(Document_attributes, verbose_name='Наименование изделия', related_name='STMP_1_view_operations', null=True, blank=True)
    STMP_2 = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение изделия', related_name='STMP_2_view_operations', null=True, blank=True)
    version = PositiveIntegerField(null=True, blank=True)
    where_from = NameField()

    isFolder = BooleanField()

    objects = Item_operations_viewManager()

    @property
    def item(self):
        from kaf_pas.ckk.models.item import Item
        return Item.objects.get(id=self.id)

    def __str__(self):
        return f'ID: {self.id} \n' \
               f'document: [{self.document}], \n' \
               f'STMP_1: [{self.STMP_1}], \n' \
               f'STMP_2: [{self.STMP_2}], \n' \
               f'relevant: {self.relevant}, \n' \
               f'confirmed: {self.confirmed}, \n' \
               f'where_from: {self.where_from}, \n' \
               f'refs_props: {self.refs_props}, \n' \
               f'props: {self.props}, \n' \
               f'version: {self.version}, \n' \
               f'qty_operations: {self.qty_operations}, \n' \
               f'section: {self.section}, \n' \
               f'refs_id: {self.refs_id}'

    class Meta:
        managed = False
        db_table = 'ckk_item_operations_view'
        verbose_name = 'Товарная позиция'
