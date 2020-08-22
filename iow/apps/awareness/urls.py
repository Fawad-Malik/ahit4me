from django.urls import path

from .views import Questions, AnswerView, fetch_answers, fetch_spaces, saveanswers, add_new_timeline, update_user_timeline, update_user_activity, delete_user_activity, DailyTasksView

urlpatterns = [
    path('', Questions.as_view(), name='awareness_questions'),
    path('questions/<str:cat_name>/<str:sub_cat_name>/', fetch_answers, name='fetch_answers'),
    path('questions/<str:space_name>/', fetch_spaces, name='fetch_spaces'),
    path('daily-tasks/<str:start_time>/<str:end_time>/', DailyTasksView.as_view(), name='daily_tasks'),
    path('<str:answer_type>/answer/<int:answer_id>/', AnswerView.as_view(), name='awareness_answer'),
    path('save/ans', saveanswers, name='awareness_answer'),
    path('add-new-timeline/', add_new_timeline, name='add_new_timeline'),
    path('update-activity/', update_user_activity, name='update_user_activity'),
    path('delete-activity/', delete_user_activity, name='delete_user_activity'),
    path('update-user-time/', update_user_timeline, name='update_user_timeline'),
]

