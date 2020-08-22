from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from iow.apps.user.views import (
    Login, PasswordForgot, PasswordReset, ProfileView,
    Register, confirm_register, Dashboard, MyProgressView, process_payment,
    ProfileSubscriptionView, ProfileSettingsView, delete_subscription, redeem_code,
    change_password, delete_profile, Practice, PracticeTrackerYearly, PracticeTrackerMonthly
)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/subscription/', ProfileSubscriptionView.as_view(), name='profile_subscription'),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile_settings'),


    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('practice-session/', Practice.as_view(), name='practice-session'),
    path('my_progress/', MyProgressView.as_view(), name='my_progress'),
    path('practice_tracker_yearly/', PracticeTrackerYearly.as_view(), name='practice_tracker_yearly'),
    path('practice_tracker_yearly/<int:year>/', PracticeTrackerYearly.as_view(), name='practice_tracker_yearly_w_year'),
    path('practice_tracker_monthly/', PracticeTrackerMonthly.as_view(), name='practice_tracker_monthly'),
    path('practice_tracker_monthly/<int:month>/<int:year>/', PracticeTrackerMonthly.as_view(), name='practice_tracker_monthly_w_month'),

    path('login/', Login.as_view(), name='landing_login'),
    path('logout/', LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('register/confirm/<str:confirm_hash>/', confirm_register, name='confirm_register'),


    path('password_forgot/', PasswordForgot.as_view(), name='password_forgot'),

    path(
        'password_forgot/link_took_off/',
        TemplateView.as_view(template_name='user/request_password_reset_success.html'),
        name='password_forgot_success'
    ),

    path('password_forgot/reset/<str:onetime_hash>/', PasswordReset.as_view(), name='password_reset'),

    path('process_payment/', process_payment, name='process_payment'),

    path('delete_subscription/', delete_subscription, name='delete_subscription'),
    path('redeem_code/', redeem_code, name='redeem_code'),
    path('change_password/', change_password, name='change_password'),
    path('delete_profile/', delete_profile, name='delete_profile'),

]
