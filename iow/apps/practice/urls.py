from django.urls import path

from iow.apps.practice.views import (
    PracticeDetail, PracticePlayView, fetch_sub_cats,
    fetch_affirmations, fetch_affirmation_text,
    DiscoverView, set_seconds, remove_from_pack
)

urlpatterns = [
    path('discover/packs/', DiscoverView.as_view(), name='discover'),

    path('detail/<str:slug>/<int:pk>/', PracticeDetail.as_view(), name='practice_detail'),
    path('detail/<str:slug>/<int:pk>/play/', PracticePlayView.as_view(), name='practice_play'),
    path('detail/<str:slug>/<int:pk>/play/count/', PracticePlayView.as_view(), name='count_play_session'),
    path('detail/<str:slug>/<int:pk>/play/fulfilment/', PracticePlayView.as_view(), name='count_fulfilment'),

    path('remove_from_pack/<int:practice_id>/', remove_from_pack, name='remove_from_pack'),

    # ajax stuff
    path('set_seconds/<int:practice_id>/', set_seconds, name='set_seconds'),
    path('fetch_sub_cats/<int:cat_id>/', fetch_sub_cats, name='fetch_sub_cats'),
    path('fetch_affirmations/<int:sub_cat_id>/', fetch_affirmations, name='fetch_affirmations'),
    path('fetch_affirmation_text/<int:affirmation_id>/', fetch_affirmation_text, name='fetch_affirmation_text')
]
