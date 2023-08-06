from django.urls import path

from kaf_pas.ckk.views import item_varians

urlpatterns = [

    path('Item_variants/Fetch/', item_varians.Item_varians_Fetch),
    path('Item_variants/Add', item_varians.Item_varians_Add),
    path('Item_variants/Update', item_varians.Item_varians_Update),
    path('Item_variants/Remove', item_varians.Item_varians_Remove),
    path('Item_variants/Lookup/', item_varians.Item_varians_Lookup),
    path('Item_variants/Info/', item_varians.Item_varians_Info),
    path('Item_variants/Copy', item_varians.Item_varians_Copy),

]
