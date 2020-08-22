from django.urls import path

from .views import CausalForces, DetailPage, detailPage_backforth, detailPage_backforth_positive, connect_excel_file

urlpatterns = [
path('', CausalForces.as_view(), name='causalforces_index'),
path('<str:category>/<str:sub_cat>/',
DetailPage.as_view(), name='causalforces_detail'),
path('detail_backforth/<str:category>/<str:sub_cat>/<str:current_reality>/<int:current_reality_id>/<int:id>',
     detailPage_backforth.as_view(), name='causalforces_detail_backforth'),
path('detail_backforth_positive/<str:category>/<str:sub_cat>/<str:want>/<int:want_id>/<int:id>',
     detailPage_backforth_positive.as_view(), name='causeandeffects_detail_specific_want_positive'),
path('connect_excel_file/', connect_excel_file.as_view(), name='causalforces_connect_csv_file'),
path('<str:category>/<str:sub_cat>/<str:current_reality>/<int:current_reality_id>',
     DetailPage.as_view(), name='causalforces_detail_specific_want'),
     
]
