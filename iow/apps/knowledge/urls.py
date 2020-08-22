from django.urls import path

from .views import index, detail

urlpatterns = [
    path('', index, name='knowledge_index'),
    path('detail/<str:slug>/<int:pk>/', detail, name='knowledge_detail'),
]
