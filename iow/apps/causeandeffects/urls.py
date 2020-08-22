from django.urls import path

from .views import CauseAndEffects, DetailPage

urlpatterns = [
path('', CauseAndEffects.as_view(), name='causeandeffects_index'),
path('<str:category>/<str:sub_cat>/',
DetailPage.as_view(), name='causeandeffects_detail'),
path('<str:category>/<str:sub_cat>/<str:want>/<int:want_id>',
     DetailPage.as_view(), name='causeandeffects_detail_specific_want'),
]
