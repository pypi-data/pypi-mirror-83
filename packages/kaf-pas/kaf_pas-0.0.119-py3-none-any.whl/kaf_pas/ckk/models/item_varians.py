import logging

from django.db import transaction
from django.forms import model_to_dict

from isc_common import delAttr, setAttr
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditManager, AuditQuerySet, AuditModel
from kaf_pas.ckk.models.item import Item
from kaf_pas.ckk.models.item_refs import Item_refsManager
from kaf_pas.ckk.models.item_varians_view import Item_varians_viewManager
from kaf_pas.ckk.models.item_view import Item_viewManager

logger = logging.getLogger(__name__)


class Item_variansQuerySet(AuditQuerySet):
    pass


class Item_variansManager(AuditManager):

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        child_id = _data.get('child_id')
        parent_id = _data.get('parent_id')

        items = _data.get('items')
        delAttr(_data, 'items')

        if not isinstance(items, list) or len(items) == 0:
            raise Exception(f'Не сделан выбор')

        with transaction.atomic():
            for item in items:
                # if child_id == item:
                #     continue

                setAttr(_data, 'item_id', item)
                res, _ = super().get_or_create(**_data)
                res = model_to_dict(res)

        # data.update(DelProps(res))
        Item_viewManager.refreshRows(dict(id=child_id, parent_id=parent_id))
        Item_varians_viewManager.fullRows()
        return res

    def deleteFromRequest(self, request):
        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_olds_tuple_ids()
        ids = request.get_old_ids()
        ids = list(map(lambda x: dict(id=x.child_id, parent_id=x.parent_id), Item_varians.objects.filter(id__in=ids)))

        with transaction.atomic():
            for id, mode in tuple_ids:
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                    res += 1
                elif mode == 'visible':
                    super().filter(id=id).soft_restore()
                else:
                    qty, _ = super().filter(id=id).delete()
                    res += qty

            Item_viewManager.refreshRows(ids)
        return res

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return Item_variansQuerySet(self.model, using=self._db)


class Item_varians(AuditModel):
    item = ForeignKeyCascade(Item, related_name='Item_varians_item')
    child = ForeignKeyProtect(Item, related_name='Item_varians_child')
    parent = ForeignKeyProtect(Item, related_name='Item_varians_parent')
    refs_props = Item_refsManager.props()

    objects = Item_variansManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Варианты для конфигуратора'
        unique_together = (('item', 'child', 'parent', 'refs_props'),)
