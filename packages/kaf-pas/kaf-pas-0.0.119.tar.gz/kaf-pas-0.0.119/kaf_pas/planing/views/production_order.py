from django.conf import settings
from django.db import connection

from isc_common import dictinct_list
from isc_common.common.mat_views import refresh_mat_view
from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException, JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.operation_resources_view import Operation_resources_view
from kaf_pas.planing.models.production_order import Production_order, Production_orderManager
from kaf_pas.planing.models.production_order_per_launch import Production_order_per_launch


@JsonResponseWithException()
def Production_order_Fetch(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)

    criteria = _request.get_criteria()

    arranged_lst = list(filter(lambda x: x.get('fieldName') == 'arranged', criteria))
    if len(arranged_lst) > 0:
        arranged = arranged_lst[0].get('value')
    else:
        arranged = False

    location_id_lst = list(filter(lambda x: x.get('fieldName') == 'location_id', criteria))
    if len(location_id_lst) > 0:
        location_id = location_id_lst[0].get('value')
    else:
        location_id = None

    if _request.is_admin or _request.is_develop:
        if arranged == False:
            if location_id is not None:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    filter(location_ids__overlap=[location_id]). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )
            else:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )
        else:
            if location_id is not None:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    filter(arranges_exucutors__isnull=False). \
                    filter(location_ids__overlap=[location_id]). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )
            else:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    filter(arranges_exucutors__isnull=False). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )

        return JsonResponse(DSResponse(request=request, data=data, status=RPCResponseConstant.statusSuccess).response)
    else:
        if arranged == False:
            if location_id is not None:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    filter(exucutors__overlap=[_request.user_id]). \
                    filter(location_ids__overlap=[location_id]). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )
            else:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    filter(exucutors__overlap=[_request.user_id]). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )

        else:
            if location_id is not None:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    filter(arranges_exucutors__overlap=[_request.user_id]). \
                    filter(location_ids__overlap=[location_id]). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )
            else:
                data = Production_order.objects. \
                    select_related('opertype', 'creator', 'status', 'launch', 'item'). \
                    filter(opertype__in=opers_types). \
                    filter(arranges_exucutors__overlap=[_request.user_id]). \
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecord
                )

        return JsonResponse(DSResponse(request=request, data=data, status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_per_launch_Fetch(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)
    criteria = _request.get_criteria()

    location_id_lst = list(filter(lambda x: x.get('fieldName') == 'location_id', criteria))
    if len(location_id_lst) > 0:
        location_id = location_id_lst[0].get('value')
    else:
        location_id = None

    if _request.is_admin or _request.is_develop:
        if location_id is not None:
            return JsonResponse(
                DSResponse(
                    request=request,
                    data=Production_order_per_launch.objects.
                        select_related('opertype', 'creator', 'status', 'launch', 'item').
                        filter(opertype__in=opers_types).
                        filter(location_ids__overlap=[location_id]).
                        get_range_rows1(
                        request=request,
                        function=Production_orderManager.getRecord
                    ),
                    status=RPCResponseConstant.statusSuccess).response)
        else:
            return JsonResponse(
                DSResponse(
                    request=request,
                    data=Production_order_per_launch.objects.
                        select_related('opertype', 'creator', 'status', 'launch', 'item').
                        filter(opertype__in=opers_types).
                        get_range_rows1(
                        request=request,
                        function=Production_orderManager.getRecord
                    ),
                    status=RPCResponseConstant.statusSuccess).response)
    else:
        if location_id is not None:
            return JsonResponse(
                DSResponse(
                    request=request,
                    data=Production_order_per_launch.objects.
                        select_related('opertype', 'creator', 'status', 'launch', 'item').
                        filter(opertype__in=opers_types).
                        filter(exucutors__overlap=[_request.user_id]).
                        filter(location_ids__overlap=[location_id]).
                        get_range_rows1(
                        request=request,
                        function=Production_orderManager.getRecord
                    ),
                    status=RPCResponseConstant.statusSuccess).response)
        else:
            return JsonResponse(
                DSResponse(
                    request=request,
                    data=Production_order_per_launch.objects.
                        select_related('opertype', 'creator', 'status', 'launch', 'item').
                        filter(opertype__in=opers_types).
                        filter(exucutors__overlap=[_request.user_id]).
                        get_range_rows1(
                        request=request,
                        function=Production_orderManager.getRecord
                    ),
                    status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLocations(request):
    from kaf_pas.production.models.launches import Launches
    from kaf_pas.planing.models.operation_item_view import Operation_item_view

    opers_types = (
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    )

    _request = DSRequest(request=request)
    item_ids = None
    launch = None

    data = _request.get_data()
    launch_id = data.get('launch_id')
    if launch_id is not None:
        launch = Launches.objects.get(id=launch_id)
        if launch.parent is not None:
            item_ids = tuple(set(map(lambda item: item.id, Operation_item_view.objects.filter(opertype_id=settings.OPERS_TYPES_STACK.ROUTING_TASK.id, launch=launch).distinct())))

        if launch.code == '000':
            item_ids = tuple(set(map(lambda item: item.id, Operation_item_view.objects.filter(opertype_id=settings.OPERS_TYPES_STACK.ROUTING_TASK.id, launch__in=launch.child_launches).distinct())))

        if item_ids is not None and len(item_ids) == 0:
            item_ids = tuple([0])

    if _request.is_admin or _request.is_develop:
        if item_ids is not None:
            if launch.parent is not None:
                sql_str = f'''select s.location_id,
                               get_full_name(s.location_id, 'ckk_locations') location_full_name,
                               cl.name as                                    location_name,
                               cl.level_grouping 
                        from (
                                 select distinct get_workshop_id(s.location_id_in1, 'ckk_locations') location_id
                                 from (
                                          SELECT distinct choprs.location_id location_id_in1
                                          FROM planing_operation_resources as pors
                                          join planing_operation_launches as polch on polch.operation_id = pors.operation_id
                                          join production_resource as choprs on pors.resource_id = choprs.id
                                          join planing_operations as po on polch.operation_id = po.id
                                          join planing_operation_refs as porf on po.id = porf.child_id
                                          join planing_operation_item as poit on poit.operation_id = pors.operation_id
                                          WHERE po.opertype_id in %s
                                            AND porf.props in %s
                                            AND poit.item_id in %s
                                            AND polch.launch_id = %s
                                      ) as s) as s
                                 join ckk_locations cl on s.location_id = cl.id
                        order by cl.name'''
            else:
                sql_str = f'''select s.location_id,
                                              get_full_name(s.location_id, 'ckk_locations') location_full_name,
                                              cl.name as                                    location_name,
                                              cl.level_grouping  
                                       from (
                                                select distinct get_workshop_id(s.location_id_in1, 'ckk_locations') location_id
                                                from (
                                                         SELECT distinct choprs.location_id location_id_in1
                                                         FROM planing_operation_resources as pors
                                                         join production_resource as choprs on pors.resource_id = choprs.id
                                                         join planing_operations as po on pors.operation_id = po.id
                                                         join planing_operation_refs as porf on po.id = porf.child_id
                                                         join planing_operation_item as poit on poit.operation_id = pors.operation_id
                                                         WHERE po.opertype_id in %s
                                                           AND porf.props in %s
                                                           AND poit.item_id in %s
                                                     ) as s) as s
                                                join ckk_locations cl on s.location_id = cl.id
                                       order by cl.name'''

        else:
            sql_str = f'''select s.location_id,
                               get_full_name(s.location_id, 'ckk_locations') location_full_name,
                               cl.name as                                    location_name,
                               cl.level_grouping 
                        from (
                                 select distinct get_workshop_id(s.location_id_in1, 'ckk_locations') location_id
                                 from (
                                          SELECT distinct choprs.location_id location_id_in1
                                          FROM planing_operation_resources as pors
                                                   join production_resource as choprs on pors.resource_id = choprs.id
                                                   join planing_operations as po on pors.operation_id = po.id
                                                   join planing_operation_refs as porf on po.id = porf.child_id
                                          WHERE po.opertype_id in %s
                                            AND porf.props in %s
                                      ) as s) as s
                                 join ckk_locations cl on s.location_id = cl.id
                                 order by cl.name'''

        with connection.cursor() as cursor:
            res = []
            if item_ids is not None:
                if launch.parent is not None:
                    cursor.execute(sql_str, [opers_types, (Production_order.props.product_order_routing,), item_ids, launch.parent.id])
                else:
                    cursor.execute(sql_str, [opers_types, (Production_order.props.product_order_routing,), item_ids])
            else:
                cursor.execute(sql_str, [opers_types, (Production_order.props.product_order_routing,)])
            rows = cursor.fetchall()
            for row in rows:
                id, prompt, title, level_grouping = row
                res.append(dict(id=id, title=title, prompt=prompt, level_grouping=level_grouping))

        return JsonResponse(
            DSResponse(
                request=request,
                data=res,
                status=RPCResponseConstant.statusSuccess).response)
    else:
        location = tuple(data.get('location', tuple([])))
        if len(location) == 0:
            location = tuple(data.get('location_id', tuple([])))

        if len(location) == 0:
            location = tuple(0)

        if item_ids is not None:
            sql_str = f'''select s.location_id,
                           get_full_name(s.location_id, 'ckk_locations') location_full_name,
                           cl.name as                                    location_name,
                           cl.level_grouping 
                        from (
                                 select distinct get_workshop_id(s.location_id_in1, 'ckk_locations') location_id
                                 from (
                                          SELECT distinct choprs.location_id location_id_in1
                                          FROM planing_operation_resources as pors
                                          join planing_operation_launches as polch on polch.operation_id = pors.operation_id
                                          join production_resource as choprs on pors.resource_id = choprs.id
                                          join planing_operations as po on polch.operation_id = po.id
                                          join planing_operation_executor as poex on poex.operation_id = po.id
                                          join planing_operation_refs as porf on po.id = porf.child_id
                                          join planing_operation_item as poit on poit.operation_id = pors.operation_id
                                          WHERE po.opertype_id in %s
                                            AND porf.props in %s
                                            AND poit.item_id in %s
                                            AND polch.launch_id = %s
                                            AND poex.executor_id in %s
                                      ) as s) as s
                                 join ckk_locations cl on s.location_id = cl.id
                        where s.location_id in %s    
                        order by cl.name'''
        else:
            sql_str = f'''select s.*
                            from (
                                     select s.location_id,
                                            get_full_name(s.location_id, 'ckk_locations') location_full_name,
                                            cl.name as                                    location_name,
                                            cl.level_grouping
                                     from (
                                              select distinct get_workshop_id(s.location_id_in1, 'ckk_locations') location_id
                                              from (
                                                       SELECT distinct choprs.location_id location_id_in1
                                                       FROM planing_operation_resources as pors
                                                                join production_resource as choprs on pors.resource_id = choprs.id
                                                                join planing_operations as po on pors.operation_id = po.id
                                                                join planing_operation_refs as porf on po.id = porf.child_id
                                                                join planing_operation_executor as poex on poex.operation_id = po.id
                                                       WHERE po.opertype_id in %s
                                                         AND porf.props in %s
                                                         AND poex.executor_id in %s
                                                   ) as s) as s
                                              join ckk_locations cl on s.location_id = cl.id
                                     order by cl.name) as s
                            where s.location_id in %s'''

        with connection.cursor() as cursor:
            res = []
            if item_ids is not None:
                cursor.execute(sql_str, [opers_types, (Production_order.props.product_order_routing,), item_ids, launch.parent.id, (_request.user_id,), location])
            else:
                cursor.execute(sql_str, [opers_types, (Production_order.props.product_order_routing,), (_request.user_id,), location])
            rows = cursor.fetchall()
            for row in rows:
                id, prompt, title, level_grouping = row
                res.append(dict(id=id, title=title, prompt=prompt, level_grouping=level_grouping))

        return JsonResponse(
            DSResponse(
                request=request,
                data=res,
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchLevels(request):
    opers_types = [
        settings.OPERS_TYPES_STACK.PRODUCTION_TASK.id,
    ]

    _request = DSRequest(request=request)
    if _request.is_admin or _request.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing,
                    ]
                ).
                    order_by('level__code').
                    values('level_id', 'level__name', 'level__code').
                    distinct().
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLevels
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=dictinct_list(Operation_resources_view.objects.
                    filter(executor__in=[_request.user_id]).
                    filter(
                    opertype__in=opers_types,
                    props__in=[
                        Production_order.props.product_order_routing,
                    ]
                ).
                    order_by('level__code').
                    values('level_id', 'level__name', 'level__code').
                    distinct().
                    get_range_rows1(
                    request=request,
                    function=Production_orderManager.getRecordLevels
                ), True, 'title'),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_FetchExecutorsLocation(request):
    from kaf_pas.ckk.models.locations_users import Locations_users
    from kaf_pas.ckk.models.locations_users import Locations_usersManager
    return JsonResponse(
        DSResponse(
            request=request,
            data=Locations_users.objects.
                filter().
                distinct().
                get_range_rows1(
                request=request,
                function=Locations_usersManager.getRecord1),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)

@JsonResponseWithException()
def Production_order_Grouping(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.groupingFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_UpdateForwarding(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.updateFromRequestUpdateForwarding(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_SetStartStatus(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_setStartStatus(request=request), status=RPCResponseConstant.statusSuccess).response)\

@JsonResponseWithException()
def Production_order_SetFinishStatus(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().get_setFinishStatus(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_getValue_made(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().getValue_made(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException(printing=False)
def User_Fetch4(request):
    return JsonResponse(DSResponse(request=request, data=Production_order.objects.get_queryset().getLoocationUsers(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_MakeProdOrder(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.makeProdOrderFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_DeleteProdOrder(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.deleteProdOrderFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_RefreshRows(request):
    return JsonResponse(DSResponseUpdate(data=Production_order.objects.refreshRowsProdOrderFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Production_order_RefreshMView(request):
    refresh_mat_view('planing_production_order_mview')
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)
