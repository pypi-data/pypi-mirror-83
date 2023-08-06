from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.item_varians import Item_varians
from kaf_pas.ckk.models.item_varians_view import Item_varians_view, Item_varians_viewManager


@JsonResponseWithException()
def Item_varians_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_varians_view.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Item_varians_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_varians_Add(request):
    return JsonResponse(DSResponseAdd(data=Item_varians.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_varians_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item_varians.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_varians_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item_varians.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_varians_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item_varians.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_varians_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_varians.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_varians_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_varians.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
