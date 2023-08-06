from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.kd.models.documents_thumb10_preview_params import Documents_thumb10_preview_params, Documents_thumb10_preview_paramsManager


@JsonResponseWithException()
def Documents_thumb10_preview_params_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Documents_thumb10_preview_params.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=Documents_thumb10_preview_paramsManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_thumb10_preview_params_Add(request):
    return JsonResponse(DSResponseAdd(data=Documents_thumb10_preview_params.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_thumb10_preview_params_Update(request):
    return JsonResponse(DSResponseUpdate(data=Documents_thumb10_preview_params.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_thumb10_preview_params_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Documents_thumb10_preview_params.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_thumb10_preview_params_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Documents_thumb10_preview_params.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_thumb10_preview_params_Info(request):
    return JsonResponse(DSResponse(request=request, data=Documents_thumb10_preview_params.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_thumb10_preview_params_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Documents_thumb10_preview_params.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
