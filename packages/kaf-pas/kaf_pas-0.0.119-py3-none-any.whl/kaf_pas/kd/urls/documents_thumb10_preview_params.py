from django.urls import path

from kaf_pas.kd.views import documents_thumb10_preview_params

urlpatterns = [

    path('Documents_thumb10_preview_params/Fetch/', documents_thumb10_preview_params.Documents_thumb10_preview_params_Fetch),
    path('Documents_thumb10_preview_params/Add', documents_thumb10_preview_params.Documents_thumb10_preview_params_Add),
    path('Documents_thumb10_preview_params/Update', documents_thumb10_preview_params.Documents_thumb10_preview_params_Update),
    path('Documents_thumb10_preview_params/Remove', documents_thumb10_preview_params.Documents_thumb10_preview_params_Remove),
    path('Documents_thumb10_preview_params/Lookup/', documents_thumb10_preview_params.Documents_thumb10_preview_params_Lookup),
    path('Documents_thumb10_preview_params/Info/', documents_thumb10_preview_params.Documents_thumb10_preview_params_Info),
    path('Documents_thumb10_preview_params/Copy', documents_thumb10_preview_params.Documents_thumb10_preview_params_Copy),

]
