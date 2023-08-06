import logging
from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import EmptyResultSet
from django.db import transaction, connection
from django.db.models import DecimalField, DateTimeField, TextField, BooleanField, BigIntegerField, PositiveIntegerField, SmallIntegerField
from django.forms import model_to_dict

from isc_common import setAttr, Stack, StackElementNotExist, Wrapper
from isc_common.auth.models.user import User
from isc_common.bit import TurnBitOn
from isc_common.common import blinkString, started, new, doing, red
from isc_common.common.functions import ExecuteStoredProc
from isc_common.datetime import DateTimeToStr, DateToStr
from isc_common.fields.code_field import CodeField, JSONFieldIVC
from isc_common.fields.related import ForeignKeyProtect, ForeignKeyCascade
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_manager import CommonManager
from isc_common.models.audit import AuditModel, AuditQuerySet
from isc_common.models.tree_audit import TreeAuditModelManager
from isc_common.number import DecimalToStr, ToDecimal, Set, model_2_dict
from isc_common.progress import managed_progreses, ProgressDroped, progress_deleted
from isc_common.ws.webSocket import WebSocket
from kaf_pas.ckk.models.item import Item
from kaf_pas.planing.models.operation_types import Operation_types
from kaf_pas.planing.models.operations import Operations
from kaf_pas.planing.models.production_ext import Production_ext, Operation_executor_stack
from kaf_pas.planing.models.production_order_values_ext import Production_orderWrapper
from kaf_pas.planing.models.rouning_ext import Routing_ext
from kaf_pas.planing.views.production_order_opers import production_order_opers_opers_types
from kaf_pas.production.models.launches import Launches

logger = logging.getLogger(__name__)


class ProductionOrderStack(Stack):
    def push(self, item, exists_function=None, logger=None):
        super().push(item=item, exists_function=exists_function, logger=logger)
        key = f'ProductionOrderStack_{item.id}'
        settings.LOCKS.acquire(key)

    def lock_release(self):
        for item in self.stack:
            key = f'ProductionOrderStack_{item.id}'
            settings.LOCKS.release(key)


class ProductionOrderErrorStack(Stack):
    def push(self, item, error, exists_function=None, logger=None):
        from django.db.models import Model

        if not isinstance(error, str):
            raise Exception(f'{error} must be str.')

        if not isinstance(item, Model):
            raise Exception(f'{error} must be str.')

        try:
            item_error = self.find_one(lambda x: x[0].id == item.id)
            item_error[1].append(error)
        except StackElementNotExist:
            super().push(item=(item, [error]), exists_function=exists_function, logger=logger)

    def has_not_error(self, item):
        return not self.exists(lambda x: x[0].id == item.id)


class Production_orderQuerySet(AuditQuerySet):
    production_ext = Production_ext()

    @staticmethod
    def get_user_locations(user):
        from kaf_pas.ckk.models.locations_users import Locations_users
        if not user.is_admin and not user.is_develop:
            return list(map(lambda x: x.location.id, Locations_users.objects.filter(user=user).distinct()))
        else:
            return None

    def check_state(self):
        for this in self:
            if ToDecimal(this.value_odd) > 0 and ToDecimal(this.value_start) > 0:
                status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(started)
            elif ToDecimal(this.value_start) == 0:
                status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(new)
            else:
                if ToDecimal(this.value_start) >= ToDecimal(this.value_sum):
                    status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(doing)
                else:
                    status = settings.OPERS_TYPES_STACK.PRODUCTION_TASK_STATUSES.get(started)

            updated = super().filter(id=this.id).update(status=status)
            logger.debug(f'updated: {updated}')
            updated = Operations.objects.filter(id=this.id).update(status=status)
            logger.debug(f'updated: {updated}')

    def get_range_rows(self, start=None, end=None, function=None, json=None, distinct_field_names=None, user=None, *args, **kwargs):
        queryResult = self._get_range_rows(*args, start=start, end=end, function=function, json=json, distinct_field_names=distinct_field_names)

        try:
            logger.debug(f'\n\n{queryResult.query}\n')
        except EmptyResultSet:
            pass

        if function:
            location_ids = Production_orderQuerySet.get_user_locations(user=user)
            res = [function(record, location_ids) for record in queryResult]
            return res
        else:
            res = [model_to_dict(record) for record in queryResult]
            return res

    def get_range_rows1(self, request, function=None, distinct_field_names=None, remove_fields=None, *args, **kwargs):
        request = DSRequest(request=request)
        data = request.get_data()

        _data = data.copy()
        if _data.get('criteria') is not None:

            criteria = list(filter(lambda x: x.get('fieldName') not in ['location_id', 'arranged'], _data.get('criteria')))
            criteria1 = list(filter(lambda x: x.get('fieldName') == 'parent_item_id' and x.get('value') == None and x.get('operator') == 'notEqual', criteria))

            if len(criteria1) > 0:
                criteria = list(filter(lambda x: x.get('fieldName') != 'parent_item_id', criteria))
            #     criteria.append(dict(fieldName='parent_item_id', value=None, operator='equals'))

            setAttr(_data, 'criteria', criteria)

        request.set_data(_data)

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            distinct_field_names=distinct_field_names,
            json=request.json,
            criteria=request.get_criteria(),
            user=request.user,
        )
        return res

    # def get_info(self, request, *args):
    #     request = DSRequest(request=request)
    #     data = request.get_data()
    #
    #     launch_id = data.get('launch_id')
    #     delAttr(data, 'launch_id')
    #
    #     location_id = data.get('location_id')
    #     delAttr(data, 'location_id')
    #
    #     arranged = data.get('arranged')
    #     delAttr(data, 'arranged')
    #
    #     json_all = dict()
    #     executor = None
    #
    #     if not request.is_admin and not request.is_develop:
    #         executor = request.user
    #
    #     if launch_id is not None:
    #         for launch in Launches.objects.filter(id=launch_id):
    #             if launch.parent is not None:
    #                 items = [operation_item_view.item for operation_item_view in Operation_item_view.objects.filter(
    #                     opertype_id=settings.OPERS_TYPES_STACK.ROUTING_TASK.id,
    #                     launch=launch).distinct()]
    #                 setAttr(request.json.get('data'), 'launch_id', launch.parent.id)
    #                 setAttr(request.json.get('data'), 'item', items)
    #
    #                 json_all = copy.deepcopy(request.json)
    #                 delAttr(json_all.get('data'), 'location_id')
    #                 delAttr(json_all.get('data'), 'arranged')
    #
    #     request.set_data(data)
    #     criteria = self.get_criteria(json=request.json)
    #     criteria_all = self.get_criteria(json=json_all)
    #     if executor is not None:
    #         if arranged:
    #             cnt = super(). \
    #                 filter(arranges_exucutors__overlap=[executor.id]).filter(*args, criteria). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #             cnt_all = super().filter(arranges_exucutors__overlap=[executor.id]).filter(*args, criteria_all). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #         else:
    #             cnt = super().filter(exucutors__overlap=[executor.id]).filter(*args, criteria). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #             cnt_all = super().filter(exucutors__overlap=[executor.id]).filter(*args, criteria_all). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #     else:
    #         if arranged:
    #             cnt = super(). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #             cnt_all = super(). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #         else:
    #             cnt = super().filter(*args, criteria). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #             cnt_all = super().filter(*args, criteria_all). \
    #                 filter(location_ids__overlap=[location_id]).filter(*args, criteria). \
    #                 count()
    #
    #     return dict(qty_rows=cnt, all_rows=cnt_all)

    def get_setStartStatus(self, request):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.operation_typesStack import DETAIL_OPERS_PRD_TSK
        from kaf_pas.ckk.models.locations_users import Locations_users
        from kaf_pas.ckk.models.locations_view import Locations_view
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        request = DSRequest(request=request)

        data = request.get_data()

        location_id = data.get('location_id')
        qty = data.get('qty')
        records = data.get('records')

        if qty is None:
            raise Exception('Не введено количество.')

        _res = []

        production_order_ids = Stack()

        with transaction.atomic():
            operation_executor_stack = Operation_executor_stack()
            for record in records:

                record = Production_orderWrapper(**record)

                if record.launch.parent is None:
                    model = Production_order
                else:
                    model = Production_order_per_launch

                parent_item_ref_query = model.tree_objects.get_descendants(
                    id=record.item.id,
                    child_id='item_id',
                    parent_id='parent_item_id',
                    where_clause=f'where location_ids && array [{location_id}::bigint] and launch_id={record.launch.id} and "isFolder" = {record.isFolder}',
                    where_clause1=f'where launch_id={record.launch.id}',
                )
                for parent_item_ref in parent_item_ref_query:

                    if not production_order_ids.exists(lambda x: x == parent_item_ref.id):
                        if len(set(map(lambda x: x.user.id, Locations_users.objects.filter(location=Locations_view.objects.get(id=parent_item_ref.location_sector_ids[0]).workshop))).intersection([request.user.id])) == 0:
                            production_order_ids.push(record.id)
                            if not request.is_admin and not request.is_develop:
                                continue
                    else:
                        continue

                    _res.extend(self.production_ext.start(
                        _data=self.delete_underscore_element(model_2_dict(parent_item_ref)),
                        qty=qty,
                        user=request.user,
                        operation_executor_stack=operation_executor_stack
                    ))

            if len(_res) > 0:
                ids = map(lambda x: x.get('id'), _res)
                for operation_executor in operation_executor_stack:
                    if operation_executor.executor != request.user:
                        settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
                            message=blinkString(f'<h4>Вам направлено: {operation_executor.qty} новых заданий на производство.</h4>', bold=True),
                            users_array=[operation_executor.executor],
                        )
                        Production_orderManager.refresh_all(
                            ids=ids,
                            suffix=f'''_user_id_{operation_executor.executor.id}''',
                            production_order_opers_refresh=True,
                            production_order_opers_ids=map(lambda x: x.child.id, Operation_refs.objects.filter(parent_id__in=ids, child__opertype__code__in=[DETAIL_OPERS_PRD_TSK])),
                            user=request.user
                        )

                if len(_res) > 1:
                    Production_orderManager.refresh_all(
                        ids=ids,
                        production_order_opers_refresh=True,
                        production_order_opers_ids=map(lambda x: x.child.id, Operation_refs.objects.filter(parent_id__in=ids, child__opertype__code__in=[DETAIL_OPERS_PRD_TSK])),
                        user=request.user
                    )

        return _res

    def check_selected_order_4_finish(self, request, production_order_ids, errors):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch
        from kaf_pas.ckk.models.locations_users import Locations_users
        from kaf_pas.ckk.models.locations_view import Locations_view
        from kaf_pas.planing.models.production_order_opers import Production_order_opers
        from kaf_pas.planing.models.production_order_opers_per_launch import Production_order_opers_per_launch

        data = request.get_data()

        location_id = data.get('location_id')
        qty = data.get('qty')
        records = data.get('records')

        if qty is None:
            raise Exception('Не введено количество.')

        for record in records:

            record = Production_orderWrapper(**record)

            if record.launch.parent is None:
                order_model = Production_order
                order_opers_model = Production_order_opers
            else:
                order_model = Production_order_per_launch
                order_opers_model = Production_order_opers_per_launch

            parent_item_ref_query = order_model.tree_objects.get_descendants(
                id=record.item.id,
                child_id='item_id',
                parent_id='parent_item_id',
                where_clause=f'where location_ids && array [{location_id}::bigint] and launch_id={record.launch.id} and "isFolder" = {record.isFolder}',
                where_clause1=f'where launch_id={record.launch.id}',
                order_by_clause='order by level desc'
            )
            for parent_item_ref in parent_item_ref_query:
                item = None
                if not production_order_ids.exists(lambda x: x == parent_item_ref.id):
                    if len(set(map(lambda x: x.user.id, Locations_users.objects.filter(location=Locations_view.objects.get(id=parent_item_ref.location_sector_ids[0]).workshop))).intersection([request.user.id])) == 0:
                        if not request.is_admin and not request.is_develop:
                            continue
                        else:
                            item = parent_item_ref
                    else:
                        item = parent_item_ref
                else:
                    continue

                if item is not None:
                    if item.value_start is None:
                        errors.push(item, 'Не запущено.')
                    elif item.value_odd < qty:
                        errors.push(item, f'Не хватает остатка ({item.value_odd}), затребовано {qty}')
                    else:
                        for order_oper in order_opers_model.objects.select_related(
                                'creator',
                                'item',
                                'launch',
                                'location',
                                'location_fin',
                                'operation_operation',
                                'production_operation_color',
                                'production_operation_edizm',
                                'resource',
                                'resource_fin',
                                'status'
                        ).filter(
                            opertype__in=production_order_opers_opers_types,
                            parent_id=item.id,
                            launch=item.launch,
                        ).order_by('production_operation_num'):
                            if order_oper.production_operation_attrs is not None and 'color' in order_oper.production_operation_attrs:
                                errors.push(item, f'Операция: {order_oper.production_operation.full_name} предпологает выбор цвета')

                            if order_oper.production_operation_is_launched:
                                errors.push(item, f'Операция: {order_oper.production_operation.full_name} предпологает выбор запуска')

                    if errors.has_not_error(item):
                        production_order_ids.push(item)

    def get_setFinishStatus(self, request):
        from kaf_pas.planing.models.production_order_values_ext import Production_order_values_ext

        request = DSRequest(request=request)
        production_order_ids = ProductionOrderStack()
        errors = ProductionOrderErrorStack()

        data = request.get_data()
        qty = data.get('qty')

        if qty is None:
            raise Exception('Не введено количество.')

        self.check_selected_order_4_finish(
            request=request,
            production_order_ids=production_order_ids,
            errors=errors
        )

        if errors.size() > 0:
            errors_strs = []
            for error in errors:
                s1 = '\n' + "\n".join(error[1])
                s = f'Для {error[0].item.item_name} выявлены следующие ошибки: {s1}'
                errors_strs.append(s)

            s = '\n\n'.join(errors_strs)
            raise Exception(f'<pre>{s}</pre>')

        with transaction.atomic():
            production_order_values_ext = Production_order_values_ext()

            res = production_order_values_ext.blockMakeAll1(
                data=dict(records=production_order_ids.stack),
                user=request.user
            )

            return res

    def getLoocationUsers(self, request):
        from kaf_pas.ckk.models.locations_users import Locations_users
        from isc_common.auth.managers.user_manager import UserManager

        request = DSRequest(request=request)
        data = request.get_data()

        location_sector_ids = set()
        for record in data.get('location_sector_ids'):
            for location_sector_id in record:
                location_sector_ids.add(location_sector_id)
                break

        if len(location_sector_ids) != 1:
            location_sector_ids = []
        else:
            location_sector_ids = list(location_sector_ids)

        location_id = data.get('location_id')

        parent_query = Locations_users.objects.filter(location_id__in=location_sector_ids, user=request.user)
        parent = None
        if parent_query.count() > 0:
            parent = parent_query[0]

        if parent is None:
            parent_query = Locations_users.objects.filter(location_id=location_id, user=request.user)
            if parent_query.count() > 0:
                parent = parent_query[0]

        res = [UserManager.getRecord1(item.user).get('id') for item in Locations_users.objects.filter(location_id=location_id, parent=parent)]
        res1 = [UserManager.getRecord1(item.user).get('id') for item in Locations_users.objects.filter(location_id__in=location_sector_ids)]

        res2 = list(set(res).intersection(res1))
        return [UserManager.getRecord1(User.objects.get(id=id)) for id in res2]


class Production_orderManager(CommonManager):
    production_ext = Production_ext()
    routing_ext = Routing_ext()

    @staticmethod
    def ids_list_2_opers_list(ids):
        from isc_common.models.audit import AuditModel

        if ids is None:
            return []

        ls_res = []

        if not isinstance(ids, list):
            ids = [ids]

        for id in ids:
            if isinstance(id, int):
                ls_res.append(Operations.objects.get(id=id))
            elif isinstance(id, AuditModel):
                ls_res.append(id)
            else:
                raise Exception(f'{id} must be int or Operation')
        return ls_res

    @staticmethod
    def ids_list_2_int_list(ids):
        from isc_common.models.audit import AuditModel

        if ids is None:
            return []

        if isinstance(ids, map):
            ids = list(ids)

        if not isinstance(ids, list):
            ids = [ids]

        ls_res = []
        for id in ids:
            if isinstance(id, int):
                ls_res.append(id)
            elif isinstance(id, AuditModel):
                ls_res.append(id.id)
            else:
                raise Exception(f'{id} must be int or Operation')

        return ls_res

    @staticmethod
    def refresh_all(
            ids,
            buffer_refresh=False,
            item_operations_refresh=False,
            production_order_values_refresh=False,
            production_order_opers_refresh=False,
            production_order_opers_ids=None,
            user=None,
            suffix=None
    ):
        from kaf_pas.planing.models.production_order_values import Production_order_valuesManager
        from kaf_pas.accounting.models.buffers import BuffersManager
        from kaf_pas.ckk.models.item_operations_view import Item_operations_viewManager
        from kaf_pas.planing.models.production_order_opers import Production_order_opersManager

        if ids is None:
            return

        if isinstance(ids, map):
            ids = list(ids)

        Production_orderManager.update_redundant_planing_production_order_table(ids=Production_orderManager.ids_list_2_opers_list(ids))
        Production_order.objects.filter(id__in=Production_orderManager.ids_list_2_int_list(ids)).check_state()

        if suffix is None:
            Production_orderManager.refreshRows(ids=ids, user=user)
        else:
            Production_orderManager.fullRows(suffix=suffix)

        if buffer_refresh == True:
            BuffersManager.fullRows()

        if item_operations_refresh == True:
            Item_operations_viewManager.fullRows()

        if production_order_values_refresh == True:
            Production_order_valuesManager.fullRows()

        if production_order_opers_refresh == True:
            if production_order_opers_ids is not None:
                Production_order_opersManager.refreshRows(ids=production_order_opers_ids, user=user)
            else:
                Production_order_opersManager.fullRows()

    @staticmethod
    def get_use_4_grouping_message(location_id):
        from kaf_pas.ckk.models.locations_users import Locations_users
        users = list(map(lambda x: x.user, Locations_users.objects.filter(location_id=location_id)))
        users1 = list(User.objects.filter(usergroup__code='administrators'))
        users.extend(users1)
        users = list(set(users))
        return users

    @staticmethod
    def ungrouping(location_id, users, launch_id=None):
        from kaf_pas.ckk.models.locations import Locations
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        location = Locations.objects.get(id=location_id)

        key = f'ungrouping_{location_id}_{launch_id}'
        settings.LOCKS.acquire(key)

        launch = Production_orderManager.get_launch(launch_id=launch_id)
        if launch is not None:
            message = f'Расгруппировка: {location.full_name}  {launch.code} от {DateToStr(launch.date)}'
        else:
            message = f'Расгруппировка: {location.full_name}'

        qty = 0

        while True:

            if launch is None:
                model = Production_order
                parent_query = model.objects.filter(location_ids__overlap=[location_id]).exclude(level_grouping=1).union(model.objects.filter(location_ids__overlap=[location_id], created_on_grouping=1))
            else:
                if launch.parent is None:
                    model = Production_order
                    parent_query = model.objects.filter(location_ids__overlap=[location_id], launch=launch).exclude(level_grouping=1).union(model.objects.filter(location_ids__overlap=[location_id], created_on_grouping=1))
                else:
                    model = Production_order_per_launch
                    parent_query = model.objects.filter(location_ids__overlap=[location_id], launch=launch).exclude(level_grouping=1).union(model.objects.filter(location_ids__overlap=[location_id], created_on_grouping=1))

            _qty = parent_query.count()
            if _qty == 0:
                settings.LOCKS.release(key)
                break

            with managed_progreses(
                    id=key,
                    qty=_qty,
                    users=users,
                    message=message,
                    title='Выполнено',
                    props=TurnBitOn(0, 0)
            ) as progreses:

                def except_func():
                    settings.LOCKS.release(key)

                progreses.except_func = except_func

                for parent_item in parent_query:
                    parent_item_ref_query = model.tree_objects.get_descendants(
                        id=parent_item.item.id,
                        child_id='item_id',
                        parent_id='parent_item_id',
                        where_clause=f'where location_ids && array [{location_id}::bigint] and launch_id={parent_item.launch.id}',
                        # where_clause1=f'where location_ids && array [{location_id}::bigint] and launch_id={parent_item.launch.id}',
                        order_by_clause='order by level desc'
                    )
                    for parent_item_ref in parent_item_ref_query:
                        if parent_item_ref.parent_item is not None:
                            if parent_item_ref.props.for_grouped.is_set:
                                res = model.objects.filter(
                                    id=parent_item_ref.id,
                                    item=parent_item_ref.item,
                                    parent_item=parent_item_ref.parent_item,
                                    location_ids=parent_item_ref.location_ids,
                                    launch=parent_item_ref.launch,
                                ).delete()
                            else:
                                model.objects.filter(
                                    id=parent_item_ref.id,
                                    item=parent_item_ref.item,
                                    parent_item=parent_item_ref.parent_item,
                                    location_ids=parent_item_ref.location_ids,
                                    launch=parent_item_ref.launch,
                                ).update(
                                    parent_item=None
                                )
                        else:
                            if parent_item_ref.props.for_grouped.is_set:
                                res = model.objects.filter(
                                    id=parent_item_ref.id,
                                    item=parent_item_ref.item,
                                    parent_item=None,
                                    location_ids=parent_item_ref.location_ids,
                                    launch=parent_item_ref.launch,
                                ).delete()
                            else:
                                model.objects.filter(
                                    id=parent_item_ref.id,
                                    item=parent_item_ref.item,
                                    parent_item=None,
                                    location_ids=parent_item_ref.location_ids,
                                    launch=parent_item_ref.launch,
                                ).update(
                                    isFolder=False,
                                    level_grouping=1,
                                    exucutors=parent_item_ref.exucutors_old
                                )
                    qty += 1
                    if progreses.step() != 0:
                        settings.LOCKS.release(key)
                        raise ProgressDroped(progress_deleted)

                settings.LOCKS.release(key)
        return qty

    @staticmethod
    def get_launch(launch_id=None):
        if isinstance(launch_id, int):
            return Launches.objects.get(id=launch_id)
        elif isinstance(launch_id, Launches):
            return launch_id
        else:
            return None

    @staticmethod
    def grouping(location_id, level_grouping, launch_id=None):
        from kaf_pas.ckk.models.locations import Locations
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        def check_child(clone_child_item):
            if clone_child_item.parent_item is None:
                raise Exception(f'{model_2_dict(clone_child_item)} {blinkString("не привязан родительский элеиент", color=red)}')

        users = Production_orderManager.get_use_4_grouping_message(location_id=location_id)

        launch = Production_orderManager.get_launch(launch_id=launch_id)

        location = Locations.objects.get(id=location_id)
        location.level_grouping = level_grouping
        location.save()

        _level = 1

        key = f'grouping_{location_id}_{launch_id}'
        settings.LOCKS.acquire(key)

        # grouped_item = Stack()

        with transaction.atomic():
            qty = Production_orderManager.ungrouping(location_id=location_id, launch_id=launch_id, users=users)

            while True:
                if _level > level_grouping:
                    break

                if launch is not None:
                    message = f'Группировка: {location.full_name}  {launch.code} от {DateToStr(launch.date)}, уровень вложенности: {_level}'
                else:
                    message = f'Группировка: {location.full_name} , уровень вложенности: {_level}'

                if launch is None:
                    model = Production_order
                    query = model.objects.filter(location_ids__overlap=[location_id], level_grouping__lte=_level).exclude(max_level__gt=_level + 1).order_by('-max_level')
                else:
                    if launch.parent is None:
                        model = Production_order
                        query = model.objects.filter(location_ids__overlap=[location_id], launch=launch, level_grouping__lte=_level).exclude(max_level__gt=_level + 1).order_by('-max_level')
                    else:
                        model = Production_order_per_launch
                        query = model.objects.filter(location_ids__overlap=[location_id], launch=launch, level_grouping__lte=_level).exclude(max_level__gt=_level + 1).order_by('-max_level')

                # query = query.filter(id__in=[438518, 426453, 437054, 439610, 430933, 439381])
                # query = query.filter(id__in=[438518])
                # query = query.filter(id__in=[428220])
                # query = query.filter(id__in=[445913])
                _qty = query.count()
                qty += _qty
                if query.count() > 0:
                    with managed_progreses(
                            id=key,
                            qty=_qty,
                            users=users,
                            message=message,
                            title='Выполнено',
                            props=TurnBitOn(0, 0)
                    ) as progreses:

                        def except_func():
                            settings.LOCKS.release(key)

                        progreses.except_func = except_func

                        for child_item in query:
                            step = 1
                            # if grouped_item.exists(lambda x: x.item.id == child_item.item.id and x.level_grouping > _level):
                            #     continue

                            for parent_item in model.objects.filter(
                                    item_id__in=child_item.parent_item_ids,
                                    launch=child_item.launch
                            ).exclude(max_level__gt=_level + 1):

                                # Создаем групировочный - корневой элемент
                                exs = location_id in parent_item.location_ids
                                if not exs:

                                    parent_item_dict = dict(
                                        id=parent_item.id,
                                        item=parent_item.item,
                                        launch=parent_item.launch,
                                        parent_item=parent_item.parent_item,
                                        location_ids=[location_id],
                                    )
                                    clone_parent_item_query = model.objects.filter(**parent_item_dict)
                                    cnt = clone_parent_item_query.count()
                                    if cnt > 1:
                                        for clone_parent_item in clone_parent_item_query:
                                            logger.debug(model_2_dict(clone_parent_item))
                                    elif cnt == 1:
                                        clone_parent_item = clone_parent_item_query[0]
                                    else:
                                        parent_item_dict = model_2_dict(parent_item)

                                        setAttr(parent_item_dict, 'location_ids', [location_id])
                                        setAttr(parent_item_dict, 'isFolder', True)

                                        props = parent_item.props
                                        props |= Production_order.props.for_grouped

                                        setAttr(parent_item_dict, 'props', props)
                                        setAttr(parent_item_dict, 'level_grouping', child_item.level_grouping + 1)
                                        setAttr(parent_item_dict, 'created_on_grouping', 1)

                                        clone_parent_item = model.objects.create(**parent_item_dict)
                                else:
                                    parent_item_dict = dict(
                                        id=parent_item.id,
                                        item=parent_item.item,
                                        launch=parent_item.launch,
                                        parent_item=parent_item.parent_item,
                                        location_ids=parent_item.location_ids,
                                    )

                                    clone_parent_item_query = model.objects.filter(**parent_item_dict)

                                    if clone_parent_item_query.count() > 1:
                                        for clone_parent_item in clone_parent_item_query:
                                            logger.debug(model_2_dict(clone_parent_item))

                                    clone_parent_item_query.update(
                                        isFolder=True,
                                        level_grouping=child_item.level_grouping + 1
                                    )
                                    clone_parent_item = clone_parent_item_query[0]

                                exucutors = list(set(child_item.exucutors).union(set(clone_parent_item.exucutors)))
                                clone_parent_item_query.update(
                                    exucutors=exucutors,
                                )
                                logger.debug(f'clone_parent_item: {clone_parent_item}\n\n')

                                # Создаем сгруппированный элемент
                                if step == 1:

                                    check_child_item_dict = dict(
                                        id=child_item.id,
                                        item=child_item.item,
                                        launch=child_item.launch,
                                        parent_item=clone_parent_item.item,
                                        location_ids=child_item.location_ids,
                                    )
                                    clone_child_item_query = model.objects.filter(**check_child_item_dict)
                                    cnt = clone_child_item_query.count()

                                    if cnt > 1:
                                        for clone_child_item in clone_child_item_query:
                                            logger.debug(model_2_dict(clone_child_item))
                                    elif cnt == 1:
                                        clone_child_item = clone_child_item_query[0]
                                    else:
                                        check_child_item_dict = dict(
                                            id=child_item.id,
                                            item=child_item.item,
                                            launch=child_item.launch,
                                            parent_item=child_item.parent_item,
                                            location_ids=child_item.location_ids,
                                        )

                                        clone_child_item_query = model.objects.filter(**check_child_item_dict)

                                        clone_child_item_query.update(
                                            parent_item=clone_parent_item.item,
                                        )
                                        check_child_item_dict = dict(
                                            id=child_item.id,
                                            item=child_item.item,
                                            launch=child_item.launch,
                                            parent_item=clone_parent_item.item,
                                            location_ids=child_item.location_ids,
                                        )
                                        clone_child_item_query = model.objects.filter(**check_child_item_dict)
                                        clone_child_item = clone_child_item_query[0]

                                else:
                                    check_child_item_dict = dict(
                                        id=child_item.id,
                                        item=child_item.item,
                                        launch=child_item.launch,
                                        parent_item=clone_parent_item.item,
                                        location_ids=child_item.location_ids,
                                    )

                                    clone_child_item_query = model.objects.filter(**check_child_item_dict)

                                    cnt = clone_child_item_query.count()
                                    if cnt > 1:
                                        for clone_child_item in clone_child_item_query:
                                            logger.debug(model_2_dict(clone_child_item))
                                    elif cnt == 1:
                                        clone_child_item = clone_child_item_query[0]
                                    else:

                                        props = child_item.props
                                        props |= Production_order.props.for_grouped
                                        child_item_dict = model_2_dict(child_item)

                                        setAttr(child_item_dict, 'parent_item_id', clone_parent_item.item.id)
                                        setAttr(child_item_dict, 'props', props)
                                        setAttr(child_item_dict, 'created_on_grouping', 1)

                                        clone_child_item = model.objects.create(**child_item_dict)

                                check_child(clone_child_item=clone_child_item)
                                logger.debug(f'clone_child_item: {model_2_dict(clone_child_item)}\n\n')

                                step += 1
                                logger.debug('\n\n')

                            if progreses.step() != 0:
                                settings.LOCKS.release(key)
                                raise ProgressDroped(progress_deleted)

                _level += 1

        settings.LOCKS.release(key)
        if qty > 0:
            for user in users:
                Production_orderManager.fullRows(f'_user_id_{user.id}')

    @staticmethod
    def update_redundant_planing_production_order_table(
            ids,
            batch_mode=False,
            batch_stack=None,
    ):

        if ids is None:
            raise Exception('id must be not None')

        settings.LOCKS.acquire(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)

        try:
            ids = Production_orderManager.ids_list_2_opers_list(ids)

            for id in ids:
                if id.opertype != settings.OPERS_TYPES_STACK.PRODUCTION_TASK:
                    raise Exception(f'Операция: {id.opertype} не должна попадать во временные таблицы')

                if batch_mode == True and isinstance(batch_stack, Stack):
                    batch_stack.push(id.id)
                    continue

                ExecuteStoredProc('update_planing_production_order', [id.id])
                # Production_orderManager.grouping(operation=id, model=Production_order)

                with connection.cursor() as cursor:
                    cursor.execute('''select distinct launch_id from planing_production_order_per_launch_view where id=%s''', [id.id])
                    rows = cursor.fetchall()
                    for row in rows:
                        launch_id, = row
                        ExecuteStoredProc('update_planing_production_order_per_launch', [id.id, launch_id])
                        logger.debug(f'id: {id}, launch_id: {launch_id}')

                        # Production_orderManager.grouping(operation=id, launch_id=launch_id, model=Production_order_per_launch)

            settings.LOCKS.release(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)
        except Exception as ex:
            settings.LOCKS.release(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)
            raise ex

    @staticmethod
    def delete_redundant_planing_production_order_table(id):
        if id is None:
            raise Exception('id must be not None')

        settings.LOCKS.acquire(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)

        try:
            ids = Production_orderManager.ids_list_2_int_list(id)

            for id in ids:
                with connection.cursor() as cursor:
                    cursor.execute('''select distinct launch_id from planing_production_order_per_launch_view where id=%s''', [id])
                    rows = cursor.fetchall()
                    for row in rows:
                        launch_id, = row
                        res = ExecuteStoredProc('delete_planing_production_order_per_launch', [id, launch_id])
                        logger.debug(f'id: {res}')

                ExecuteStoredProc('delete_planing_production_order', [id])

            settings.LOCKS.release(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)
        except Exception as ex:
            settings.LOCKS.release(settings.GRID_CONSTANTS.lock_insert_update_delete_function_of_table)
            logger.error(ex)

    def updateFromRequestUpdateForwarding(self, request):
        from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch

        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)

        data = request.get_data()
        executors = data.get('executors')

        idx = 0
        with transaction.atomic():
            operation_executor_stack = Operation_executor_stack()
            while True:
                _data = data.get(str(idx))
                if _data is None:
                    break
                idx += 1

                operation_id = _data.get('id')
                description = _data.get('description')

                Operations.objects.update_or_create(id=operation_id, defaults=dict(description=description))
                self.production_ext.set_executors(
                    executors=[User.objects.get(id=id) for id in executors],
                    operation=Operations.objects.get(id=operation_id),
                    user=request.user,
                    operation_executor_stack=operation_executor_stack
                )

                Production_order.objects.filter(id=operation_id).check_state()
                Production_order_per_launch.objects.filter(id=operation_id).check_state()

            for operation_executor in operation_executor_stack:
                settings.EVENT_STACK.EVENTS_PRODUCTION_ORDER_CREATE.send_message(
                    message=blinkString(f'<h4>Вам направлено: {operation_executor.qty} новых заданий на производство.</h4>', bold=True),
                    users_array=[operation_executor.executor],
                )
                Production_orderManager.fullRows(suffix=f'''_user_id_{operation_executor.executor.id}''')

        return data

    def createFromRequest(self, request):

        request = DSRequest(request=request)
        data = request.get_data()

        production_ext = Production_ext()
        production_ext.make_production_order_by_hand(data=data, user=request.user)

        return data

    def get_queryset(self):
        return Production_orderQuerySet(self.model, using=self._db)

    @staticmethod
    def refreshRows(ids, user):

        if user is None:
            return

        ids = Production_orderManager.ids_list_2_int_list(ids)
        location_ids = Production_orderQuerySet.get_user_locations(user=user)
        records = [Production_orderManager.getRecord(record=record, location_ids=location_ids) for record in Production_order.objects.filter(id__in=ids)]
        WebSocket.row_refresh_grid(grid_id=settings.GRID_CONSTANTS.refresh_production_order_grid_row, records=records)

    @staticmethod
    def fullRows(suffix=''):
        WebSocket.full_refresh_grid(grid_id=f'{settings.GRID_CONSTANTS.refresh_production_order_grid}{suffix}')

    @staticmethod
    def getRecord(record, location_ids):

        value_sum = ToDecimal(record.value_sum)
        if value_sum != 0:
            percents = round(ToDecimal(record.value_made) * 100 / ToDecimal(record.value_sum), 2)
        else:
            percents = 0

        percents_str = "%.2f" % percents
        if location_ids is not None:
            ls_set = set(location_ids)
            s_set = set(record.location_sector_ids)

            if len(s_set.intersection(ls_set)) > 0:
                status__name_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.location_statuses.get(str(location_id)), location_ids)))
                status__color_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.location_status_colors.get(str(location_id)), location_ids)))
                status_id_arr = list(filter(lambda x: x is not None, map(lambda location_id: record.location_status_ids.get(str(location_id)), location_ids)))

                if len(status__name_arr) > 0:
                    status__name = status__name_arr[0]
                else:
                    status__name = record.status.name

                if len(status__color_arr) > 0:
                    status__color = status__color_arr[0]
                else:
                    status__color = record.status.color

                if len(status_id_arr) > 0:
                    status_id = status_id_arr[0]
                else:
                    status_id = record.status.id
            else:
                status_id = record.status.id
                status__name = record.status.name
                status__color = record.status.color
        else:
            status_id = record.status.id
            status__name = record.status.name
            status__color = record.status.color

        if isinstance(record.value1_sum, Decimal):
            value1_sum = DecimalToStr(record.value1_sum)
            value1_sum_len = 0
        elif isinstance(record.value1_sum, list):
            value1_sum = ' / '.join([DecimalToStr(v) for v in record.value1_sum]) if record.value1_sum is not None else None
            value1_sum_len = len(record.value1_sum) if record.value1_sum is not None else None,
        else:
            value1_sum = '???'
            value1_sum_len = 0

        res = {
            'cnt_opers': record.cnt_opers,
            'creator__short_name': record.creator.get_short_name,
            'date': record.date,
            'demand_codes_str': record.demand_codes_str,
            'description': record.description,
            'edizm__name': ' / '.join(record.edizm_arr) if record.edizm_arr is not None else None,
            'exucutors': record.exucutors,
            'exucutors_old': record.exucutors_old,
            'id': record.id,
            'isDeleted': record.isDeleted,
            'isFolder': record.isFolder if record.isFolder is not None else False,
            'item__STMP_1__value_str': record.item.STMP_1.value_str if record.item.STMP_1 else None,
            'item__STMP_2__value_str': record.item.STMP_2.value_str if record.item.STMP_2 else None,
            'item_id': record.item.id,
            'launch__code': record.launch.code,
            'launch__date': record.launch.date,
            'launch_id': record.launch.id,
            'level_grouping': record.level_grouping,
            'location_ids': record.location_ids,
            'location_sector_ids': Set(record.location_sector_ids).get_set_sorted_as_original,
            'location_sectors_full_name': '<br>'.join(Set(record.location_sectors_full_name).get_set_sorted_as_original),
            'max_level': record.max_level,
            'num': record.num,
            'opertype__full_name': record.opertype.full_name,
            'opertype_id': record.opertype.id,
            'parent_item_id': record.parent_item.id if record.parent_item is not None else None,
            'parent_item_ids': record.parent_item_ids,
            'props': record.props,
            'status__code': record.status.code,
            'status__name': blinkString(text=status__name, blink=False, color=status__color, bold=False),
            'status_id': status_id,
            'value1_sum': value1_sum,
            'value1_sum_len': value1_sum_len,
            'value_made': DecimalToStr(record.value_made),
            'value_made_str': f'''{blinkString(DecimalToStr(record.value_made), blink=True if percents >= 100 else False, color="blue", bold=True)}({percents_str}%)''',
            'value_odd': DecimalToStr(record.value_odd),
            'value_start': DecimalToStr(record.value_start),
            'value_sum': DecimalToStr(record.value_sum),
        }
        return res

    @staticmethod
    def getRecordLevels(record):
        return dict(id=record.get('level_id'), title=record.get('level__name'))

    def makeProdOrderFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        setAttr(_data, 'user', request.user)

        self.routing_ext.make_routing(data=_data)
        self.production_ext.make_production_order(data=_data, batch_mode=True)
        Production_orderManager.update_redundant_planing_production_order_table(ids=self.production_ext.batch_stack.stack)
        self.production_ext.batch_stack.clear()
        WebSocket.send_info_message(
            host=settings.WS_HOST,
            port=settings.WS_PORT,
            channel=f'common_{request.user.username}',
            message='Формирование завершено.',
            logger=logger
        )
        return data

    def deleteProdOrderFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        setAttr(_data, 'user', request.user)
        self.production_ext.delete_production_order(data=_data)

        routing_ext = Routing_ext()
        routing_ext.clean_routing(data=_data)
        return data

    def refreshRowsProdOrderFromRequest(self, request):
        from kaf_pas.planing.models.operation_refs import Operation_refs
        from kaf_pas.planing.operation_typesStack import DETAIL_OPERS_PRD_TSK

        request = DSRequest(request=request)

        data = request.get_data()
        records = data.get('records')
        expandedRecords = data.get('expandedRecords')

        if isinstance(records, list):
            ids = list(map(lambda x: x.get('id'), records))
            expanded_ids = list(map(lambda x: x.get('id'), expandedRecords)) if expandedRecords is not None else None

            production_order_opers_ids = list(map(lambda x: x.child.id, Operation_refs.objects.filter(parent_id__in=expanded_ids, child__opertype__code__in=[DETAIL_OPERS_PRD_TSK]))) if expanded_ids is not None else None

            Production_orderManager.update_redundant_planing_production_order_table(ids=Production_orderManager.ids_list_2_opers_list(ids))

            Production_orderManager.refresh_all(
                ids=ids,
                production_order_opers_refresh=True,
                production_order_opers_ids=production_order_opers_ids,
                user=request.user
            )

        return data

    def groupingFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        location_id = data.get('location_id')
        launch_id = data.get('launch_id')
        level_grouping = data.get('level_grouping')

        Production_orderManager.grouping(location_id=location_id, level_grouping=level_grouping, launch_id=launch_id)

        return data


class Production_order(AuditModel):
    from kaf_pas.planing.models.status_operation_types import Status_operation_types
    from kaf_pas.planing.models.operation_refs import Operation_refsManager

    arranges_exucutors = ArrayField(BigIntegerField(), default=list)
    cnt_opers = PositiveIntegerField()
    created_on_grouping = SmallIntegerField()
    creator = ForeignKeyProtect(User, related_name='Production_order_creator')
    date = DateTimeField(default=None)
    demand_codes_str = CodeField()
    description = TextField(null=True, blank=True)
    edizm_arr = ArrayField(CodeField(null=True, blank=True), default=list)
    exucutors = ArrayField(BigIntegerField(), default=list)
    exucutors_old = ArrayField(BigIntegerField(), default=list)
    isDeleted = BooleanField()
    isFolder = BooleanField()
    item = ForeignKeyProtect(Item, related_name='Production_order_item')
    launch = ForeignKeyCascade(Launches)
    level_grouping = SmallIntegerField(null=True, blank=True)
    location_ids = ArrayField(BigIntegerField(), default=list)
    location_sector_ids = ArrayField(BigIntegerField(), default=list)
    location_sectors_full_name = ArrayField(TextField(), default=list)
    location_status_colors = JSONFieldIVC()
    location_status_ids = JSONFieldIVC()
    location_statuses = JSONFieldIVC()
    max_level = SmallIntegerField()
    num = CodeField()
    opertype = ForeignKeyProtect(Operation_types, related_name='Production_order_opertype')
    parent_item = ForeignKeyProtect(Item, null=True, blank=True, related_name='Production_order_parent_item')
    parent_item_ids = ArrayField(BigIntegerField(), default=list)
    props = Operation_refsManager.props()
    status = ForeignKeyProtect(Status_operation_types)
    value1_sum = ArrayField(DecimalField(decimal_places=4, max_digits=19))
    value_made = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_odd = DecimalField(verbose_name='Количество  Выпущено', decimal_places=4, max_digits=19)
    value_start = DecimalField(verbose_name='Количество Запущено', decimal_places=4, max_digits=19, null=True, blank=True)
    value_sum = DecimalField(verbose_name='Количество по документации', decimal_places=4, max_digits=19)

    objects = Production_orderManager()
    tree_objects = TreeAuditModelManager()

    started = Status_operation_types.objects.get(code='started')

    def __str__(self):
        return f'id: {self.id}, ' \
               f'date: {DateTimeToStr(self.date)}, ' \
               f'num: {self.num}, ' \
               f'description: {self.description}, ' \
               f'opertype: [{self.opertype}], ' \
               f'creator: [{self.creator}], ' \
               f'exucutors: [{self.exucutors}], ' \
               f'status: [{self.status}], ' \
               f'launch: [{self.launch}], ' \
               f'edizm: [{self.edizm_arr}], ' \
               f'item: [{self.item}], ' \
               f'parent_item: [{self.parent_item}], ' \
               f'cnt_opers: {self.cnt_opers}, ' \
               f'value_sum: {self.value_sum},' \
               f'value1_sum: {self.value1_sum},' \
               f'value_start: {self.value_start},' \
               f'value_made: {self.value_made},' \
               f'value_odd: {self.value_odd}, ' \
               f'props: {self.props},'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Заказы на производство'
        managed = False
        # db_table = 'planing_production_order_view'
        db_table = 'planing_production_order_tbl'
