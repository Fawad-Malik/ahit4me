from django.urls import path

from .views import Questions, add_fundamentals, get_fundamentals

urlpatterns = [
    path('', Questions.as_view(), name='selftalk_detail'),
    path('add_fundamentals', add_fundamentals, name='add_fundamentals'),
    path('get_fundamentals', get_fundamentals, name='get_fundamentals'),
]
