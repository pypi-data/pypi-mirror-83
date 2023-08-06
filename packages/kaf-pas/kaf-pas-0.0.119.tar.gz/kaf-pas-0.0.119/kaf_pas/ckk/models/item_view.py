import logging

from django.conf import settings
from django.core.exceptions import EmptyResultSet
from django.db import transaction
from django.db.models import BigIntegerField, BooleanField, PositiveIntegerField
from django.forms import model_to_dict

from isc_common import delAttr, setAttr
from isc_common.auth.models.user import User
from isc_common.common import blinkString, blue, red
from isc_common.fields.code_field import CodeField
from isc_common.fields.name_field import NameField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.base_ref import Hierarcy
from isc_common.models.tree_audit import TreeAuditModelManager, TreeAuditModelQuerySet
from isc_common.number import DelProps, ToStr, StrToInt, model_2_dict
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.item import Item_add, Item
from kaf_pas.ckk.models.item_line import Item_lineManager
from kaf_pas.ckk.models.item_refs import Item_refsManager
from kaf_pas.kd.models.document_attributes import Document_attributes, Document_attributesManager
from kaf_pas.kd.models.documents import Documents
from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy

logger = logging.getLogger(__name__)


class Item_viewQuerySet(TreeAuditModelQuerySet):
    def get_range_rows_variant(self, request, function=None, distinct_field_names=None, remove_fields=None):
        request = DSRequest(request=request)

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        data = request.get_data()
        ts = data.get('ts')
        parent_id = data.get('parent_id')
        logger.debug(f'data in : {data}')
        data = dict(ts=ts, parent_id=parent_id)
        logger.debug(f'data out : {data}')
        request.set_data(data)
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            distinct_field_names=distinct_field_names,
            json=request.json,
            criteria=request.get_criteria(),
            user=request.user
        )
        return res

    def get_range_rows(self, start=None, end=None, function=None, json=None, distinct_field_names=None, criteria=None, user=None, *args):
        json = self.rearrange_parent(json=json)

        queryResult = self._get_range_rows(*args, start=start, end=end, function=function, json=json, distinct_field_names=distinct_field_names)
        try:
            logger.debug(f'\n\n{queryResult.query}\n')
        except EmptyResultSet as ex:
            logger.warning(ex)

        if function:
            res = [function(record) for record in queryResult]
        else:
            res = [model_to_dict(record) for record in queryResult]

        return res


class Item_viewManager(TreeAuditModelManager):

    @staticmethod
    def fullRows(suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_item_view_grid}{suffix}')

    @staticmethod
    def refreshRows(ids):
        if isinstance(ids, dict):
            ids = [ids]

        if isinstance(ids, list):
            for id in ids:
                if isinstance(id, dict):
                    records = [Item_viewManager.getRecord(record) for record in Item_view.objects.filter(id=id.get('id'), parent_id=id.get('parent_id'))]
                    if len (records) > 0:
                        WebSocket.row_refresh_grid(grid_id=settings.GRID_CONSTANTS.refresh_item_view_grid_row, records=records)

    def updateFromRequest(self, request, removed=None, function=None):
        from kaf_pas.ckk.models.item_refs import Item_refs

        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        with transaction.atomic():

            relevant = data.get('relevant')
            confirmed = data.get('confirmed')

            props = data.get('props', 0)
            refs_props = data.get('refs_props', 0)
            refs_id = data.get('refs_id')

            if relevant == 'Актуален':
                props |= Item.props.relevant
            else:
                props &= ~Item.props.relevant

            if confirmed == 'Подтвержден':
                props |= Item.props.confirmed
            else:
                props &= ~Item.props.confirmed

            where_from = data.get('where_from')
            if where_from == 'Получено из чертежа':
                props |= Item.props.from_cdw
            elif where_from == 'Получено из спецификации':
                props |= Item.props.from_spw
            elif where_from == 'Получено из бумажного архива':
                props |= Item.props.from_pdf
            elif where_from == 'Занесено вручную':
                props |= Item.props.man_input

            delAttr(data, 'relevant')
            delAttr(data, 'confirmed')
            delAttr(data, 'where_from')
            delAttr(data, 'qty_operations')
            delAttr(data, 'refs_props')
            delAttr(data, 'icon')
            setAttr(data, 'props', props)

            Item_refs.objects.filter(id=refs_id).update(props=refs_props)
            res = Item.objects.filter(id=data.get('id')).update(**data)

            return res

    @staticmethod
    def getRecord(record):
        STMP_1_value_str = ToStr(record.STMP_1.value_str) if record.STMP_1 else None
        if STMP_1_value_str is not None and record.haveVariant:
            STMP_1_value_str = blinkString(STMP_1_value_str, color=red, blink=False, bold=True)

        STMP_2_value_str = ToStr(record.STMP_2.value_str) if record.STMP_2 else None
        if STMP_2_value_str is not None and record.haveVariant:
            STMP_2_value_str = blinkString(STMP_2_value_str, color=blue, blink=False, bold=True)

        res = {
            'confirmed': record.confirmed,
            'creator_id': record.creator.id,
            'deliting': record.deliting,
            'document__file_document': record.document.file_document if record.document else None,
            'document_id': record.document.id if record.document else None,
            'editing': record.editing,
            'haveVariant': record.haveVariant,
            'icon': Item_lineManager.getIcon(record),
            'id': record.id,
            'isFolder': record.isFolder,
            'isLotsman': record.isLotsman,
            'lastmodified': record.lastmodified,
            'lotsman_document_id': record.lotsman_document.id if record.lotsman_document else None,
            'parent_id': record.parent_id,
            'props': record.props,
            'qty_operations': record.qty_operations,
            'real_parent_id': record.parent_id,
            'refs_props': record.refs_props,
            'relevant': record.relevant,
            'section': record.section,
            'STMP_1__value_str': STMP_1_value_str,
            'STMP_1_id': record.STMP_1.id if record.STMP_1 else None,
            'STMP_2__value_str': STMP_2_value_str,
            'STMP_2_id': record.STMP_2.id if record.STMP_2 else None,
            'version': record.version,
            'where_from': record.where_from,
        }
        # print(res)
        return DelProps(res)

    def get_queryset(self):
        return Item_viewQuerySet(self.model, using=self._db)

    @staticmethod
    def copy_item(item, parent_item, refs_props, user):
        from kaf_pas.ckk.models.item_refs import Item_refs
        from kaf_pas.ckk.models.item_line import Item_line
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.ckk.models.item_varians import Item_varians
        from kaf_pas.production.models.operations_item import Operations_item

        if not isinstance(item, Item_view) and not isinstance(item, Item):
            raise Exception('item must be a Item type')

        key = 'Item_viewManager.copy_item'
        settings.LOCKS.acquire(key)
        with transaction.atomic():
            dict_item = model_2_dict(Item.objects.get(id=item.id))
            delAttr(dict_item, 'id')
            delAttr(dict_item, 'creator_id')
            setAttr(dict_item, 'creator', user)

            setAttr(dict_item, 'document_id', dict_item.get('document'))
            props = dict_item.get('props') | Item.props.copied
            setAttr(dict_item, 'props', props)

            if item.STMP_2 is None and item.STMP_1 is not None:
                STMP_1_value_str = f'{item.STMP_1.value_str} (Копия)'
                attribute, _ = Document_attributesManager.get_or_create_attribute('STMP_1', STMP_1_value_str)
                setAttr(dict_item, 'STMP_1_id', attribute.id)

            if item.STMP_2 is not None:
                STMP_2_value_str_arr = item.STMP_2.value_str.split('-')
                _STMP_2_value_str = item.STMP_2.value_str

                l = len(STMP_2_value_str_arr)
                _variant = None
                if l > 1:
                    _variant = StrToInt(STMP_2_value_str_arr[l - 1:][0])
                    if _variant is not None:
                        _STMP_2_value_str = '-'.join(STMP_2_value_str_arr[0:l-1])

                while True:
                    if _variant is not None:
                        _variant = StrToInt(_variant)
                        if _variant is not None:
                            if _variant + 1 < 10:
                                variant = f'0{_variant + 1}'
                            else:
                                variant = str(_variant + 1)
                        else:
                            variant = '-01'
                        STMP_2_value_str = f'{_STMP_2_value_str}-{variant}'
                    else:
                        _variant=1
                        variant='01'
                        STMP_2_value_str = f'{_STMP_2_value_str}-{variant}'

                    attribute, created_attr = Document_attributesManager.get_or_create_attribute('STMP_2', STMP_2_value_str)
                    setAttr(dict_item, 'STMP_2_id', attribute.id)

                    new_item, created_item = Item.objects.get_or_create(**dict_item)
                    if not created_item:
                        if new_item.deleted_at is not None:
                            new_item.soft_restore()
                            break
                        else:
                            _variant += 1
                    else:
                        break
            else:
                new_item, created_item = Item.objects.get_or_create(**dict_item)
                if not created_item:
                    new_item.soft_restore()

            item_refs, created_refs = Item_refs.objects.get_or_create(parent=parent_item, child=new_item)
            if not created_refs:
                item_refs.soft_restore()

            for item_refs in Item_refs.objects.filter(parent_id=item.id).exclude(child__props=Item.props.copied):
                _item_refs, created = Item_refs.objects.get_or_create(parent_id=new_item.id, child=item_refs.child)
                if not created:
                    _item_refs.soft_restore()

            for item_line in Item_line.objects.filter(parent_id=item.id):
                dict_item_line = model_2_dict(item_line)

                delAttr(dict_item_line, 'id')
                delAttr(dict_item_line, 'parent_id')
                delAttr(dict_item_line, 'child_id')

                item_line, created = Item_line.objects.get_or_create(
                    parent=new_item,
                    child=item_line.child,
                    defaults=dict_item_line
                )

                if not created:
                    item_line.soft_restore()

            for item_image_refs in Item_image_refs.objects.filter(item_id=item.id):
                dict_item_image_refs = model_2_dict(item_image_refs)
                delAttr(dict_item_image_refs, 'id')
                delAttr(dict_item_image_refs, 'item_id')
                setAttr(dict_item_image_refs, 'item', new_item)
                Item_image_refs.objects.get_or_create(**dict_item_image_refs)

            for item_varians in Item_varians.objects.filter(parent_id=item.id):
                Item_varians.objects.get_or_create(
                    parent=new_item,
                    child=item_varians.child,
                    item=item_varians.item,
                    refs_props=item_varians.refs_props
                )

            for operations_item in Operations_item.objects.filter(item_id=item.id):
                operations_item_dict = model_2_dict(operations_item)
                delAttr(operations_item_dict, 'id')
                setAttr(operations_item_dict, 'item_id', new_item.id)
                Operations_item.objects.create(**operations_item_dict)

        settings.LOCKS.release(key)

        return new_item

    def copyFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        parent_id = data.get('real_parent_id')
        refs_props = data.get('refs_props')
        id = data.get('id')

        if parent_id is None:
            raise Exception('Клонировать верхний уровень нельзя.')
        item = self.get(id=id, parent_id=parent_id)
        parent_item = Item.objects.get(id=parent_id)

        new_item = Item_viewManager.copy_item(item=item, parent_item=parent_item, user=request.user, refs_props=refs_props)
        res = model_to_dict(new_item)
        setAttr(res, 'props', res.get('props')._value)

        return res


class Item_view(Hierarcy):

    confirmed = NameField()
    creator = ForeignKeyProtect(User)
    document = ForeignKeyProtect(Documents, verbose_name='Документ', null=True, blank=True)
    haveVariant = BooleanField()
    isFolder = BooleanField()
    isLotsman = BooleanField()
    lotsman_document = ForeignKeyProtect(Lotsman_documents_hierarcy, verbose_name='Документ из Лоцмана', null=True, blank=True)
    props = Item_add.get_prop_field()
    qty_operations = PositiveIntegerField()
    refs_id = BigIntegerField()
    refs_props = Item_refsManager.props()
    relevant = NameField()
    section = CodeField(null=True, blank=True)
    STMP_1 = ForeignKeyProtect(Document_attributes, verbose_name='Наименование изделия', related_name='STMP_1_view', null=True, blank=True)
    STMP_2 = ForeignKeyProtect(Document_attributes, verbose_name='Обозначение изделия', related_name='STMP_2_view', null=True, blank=True)
    version = PositiveIntegerField(null=True, blank=True)
    where_from = NameField()

    objects = Item_viewManager()

    @property
    def item(self):
        from kaf_pas.ckk.models.item import Item
        return Item.objects.get(id=self.id)

    def __str__(self):
        return f"ID={self.id} STMP_1=[{self.STMP_1}], STMP_2=[{self.STMP_2}], props={self.props}"

    class Meta:
        managed = False
        db_table = 'ckk_item_view'
        verbose_name = 'Товарная позиция'
