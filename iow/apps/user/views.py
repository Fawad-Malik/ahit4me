from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse, HttpResponse
from django.utils import timezone
from calendar import monthrange
from django.db.models import Sum, Avg
from django.views.generic import FormView, DetailView
from django.contrib.auth.decorators import login_required
from djstripe.settings import TEST_API_KEY, STRIPE_PUBLIC_KEY
from djstripe.models import Plan
import stripe
import datetime

from iow.apps.core.models import create_default_hash
from iow.apps.core.utils import send_html_mail, convert_seconds_to_hours

from .forms import LoginForm, RegisterForm, UserForm
from .models import Profile, Promotion
from iow.apps.practice.models import PracticeSession, Pack, Affirmation
from ..categories.models import Category
from iow.apps.text.models import DashboardPage
from iow.apps.numbers.models import UserStats


class Login(FormView):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/sign.html', {
            'login_form': LoginForm(), 'register_form': RegisterForm()
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST or None)

        if login_form.is_valid():
            data = login_form.cleaned_data
            username = data.get('username')
            password = data.get('password')

            username = username.lower()

            user = authenticate(username=username, password=password)
            if user is not None:

                if user.is_active:
                    login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')

                    if request.POST.get('next'):
                        return redirect(request.POST.get('next'))

                    # redirect to user dashboard
                    return redirect(reverse('dashboard'))

                else:
                    # user is not active, user should confirm his registration first
                    return render(request, 'user/sign.html', {
                        'login_form': login_form, 'register_form': RegisterForm(),
                        'login_error': 'Please confirm your registration.'
                    })
            else:
                # bad credentials
                return render(request, 'user/sign.html', {
                    'login_form': login_form, 'register_form': RegisterForm(),
                    'login_error': 'Wrong credentials'
                })

        # bad form data
        return render(request, 'user/sign.html', {
            'login_form': login_form, 'register_form': RegisterForm(),
            'login_error': 'Invalid input'
        })


class Register(FormView):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/sign.html', {
            'login_form': LoginForm(), 'register_form': RegisterForm()
        })

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('new_username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            username = username.lower()
            email = email.lower()

            if password2 != password1:
                return render(request, 'user/sign.html', {
                    'login_form': LoginForm(),
                    'register_form': form,
                    'reg_error': 'Passwords don\'t match'
                })

            if User.objects.filter(email=email).count():
                return render(request, 'user/sign.html', {
                    'login_form': LoginForm(),
                    'register_form': form,
                    'reg_error': 'User with this email exists already. Please sign in instead.'
                })

            new_user = User.objects.create(username=username, email=email, is_active=True)
            new_user.set_password(password2)
            new_user.save()

            # send confirmation link
            confirm_hash = create_default_hash()

            new_user.profile.confirm_hash = confirm_hash
            new_user.profile.save()

            confirm_link = 'https://%s%s' % (
                request.META.get('HTTP_HOST'),
                reverse('confirm_register', kwargs={'confirm_hash': confirm_hash})
            )

            send_html_mail(
                'Your registration in ahit4me.com',
                email,
                **{
                    'text': "Thanks for registering on ahit4me.com. Please confirm your registration by clicking on "
                            "the link below.",
                    'link': confirm_link,
                    'link_name': 'Confirm'
                }
            )

            return redirect('%s?success=1' % reverse('landing_login'))


def confirm_register(request, confirm_hash):
    user_profile = Profile.objects.filter(confirm_hash=confirm_hash).last()

    if not user_profile:
        # either hash is already used or invalid hash
        return redirect('%s?invalid_link=1' % reverse('landing_login'))

    user = user_profile.user

    # login user
    login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')

    if user.is_active:
        return redirect('%s?already_confirmed=1' % reverse('profile'))

    user.is_active = True
    user.save(update_fields=['is_active'])

    return redirect('%s?registration_complete=1' % reverse('profile'))


class ProfileView(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        return render(request, 'user/profile.html')


class ProfileSubscriptionView(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        client_token = ''
        stripe.api_key = TEST_API_KEY
        user_have_subscription = False
        trial = False
        subscription_from = None
        subscription_to = None
        # todo exception handling
        plans = Plan.objects.all()
        stripe_customer = stripe.Customer.retrieve(request.user.profile.stripe_customer_id)
        try:
            stripe_subscription = stripe.Subscription.retrieve(request.user.profile.stripe_subscription_id)
            if stripe_subscription:
                subscription_from = datetime.datetime.fromtimestamp(stripe_subscription.current_period_start).date()
                subscription_to = datetime.datetime.fromtimestamp(stripe_subscription.current_period_end).date()
                user_have_subscription = subscription_to >= datetime.date.today()
        except stripe.error.InvalidRequestError:
            pass

        if not user_have_subscription:
            client_token = 'oweifjowiefj'
        elif (subscription_to - subscription_from).days == 7 and not stripe_customer.sources.data:
            trial = True
            client_token = 'oweifjowiefj'

        return render(request, 'user/profile_subscription.html', {
            'client_token': client_token,
            'plans': plans,
            'first_plan': plans[0],
            'subscription_from': subscription_from,
            'subscription_to': subscription_to,
            'trial': trial,
            'user_have_subscription': user_have_subscription,
            # 'subscribtion_interval': stripe_subscription.interval,
            'stripe_public_key': STRIPE_PUBLIC_KEY
        })


@login_required(login_url='/user/login/')
def delete_profile(request):
    password = request.POST.get('password')

    user = request.user

    if user.check_password(raw_password=password):
        user = request.user

        # first unsubscribe from braintree
        # todo: remove from stripe

        # and then delete in our database
        user.delete()

        return redirect('%s?successfully_deleted=1' % reverse('landing_login'))

    return render(request, 'user/profile_settings.html', {
        'error': 'Your current password is invalid. Please try again.'
    })


@login_required(login_url='/user/login/')
def change_password(request):
    current_password = request.POST.get('current_password')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    user = request.user

    if user.check_password(raw_password=current_password):
        if password1 == password2:
            user.set_password(raw_password=password2)
            user.save()

            login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')

            return render(request, 'user/profile_settings.html', {
                'msg': 'Your new password has been set successfully.'
            })

        return render(request, 'user/profile_settings.html', {
            'error': 'New passwords do not match. Please try again'
        })

    return render(request, 'user/profile_settings.html', {
        'error': 'Your current password is invalid. Please try again.'
    })


class ProfileSettingsView(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })
        return render(request, 'user/profile_settings.html', {
            'user_form': user_form
        })

    def post(self, request, *args, **kwargs):
        """
        mostly profile changes e.g. username, email, ...
        """
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()

            # todo: notify user if he has changed his email
            return redirect('%s?profile_updated=1' % reverse('profile_settings'))

        return redirect('%s?could_not_update=1' % reverse('profile_settings'))


class MyProgressView(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):

        user_pack = request.user.user_packs.last()

        user_stats = request.user.user_stats.filter(idate__year=timezone.now().year)

        # 1. get the hours per month
        months = range(1, 13)
        total_hours = [
            convert_seconds_to_hours(
                user_stats.filter(idate__month=month).aggregate(total_hours=Sum('spent_seconds')).get('total_hours')
            ) for month in months
        ]

        # 2. get the number of practices per month
        total_practices = []
        for month in months:
            practices_of_month = user_stats.filter(idate__month=month).aggregate(
                total_practices=Sum('number_of_repetitions')
            ).get('total_practices')

            if practices_of_month:
                total_practices.append(practices_of_month)
            else:
                total_practices.append(0)

        # 3. get the average fulfilment per month
        average_fulfilments = []
        for month in months:
            fulfilment_of_month = user_stats.filter(idate__month=month).aggregate(
                fulfilment_of_month=Avg('fulfilment')
            ).get('fulfilment_of_month')

            if fulfilment_of_month:
                average_fulfilments.append(fulfilment_of_month)
            else:
                average_fulfilments.append(0)

        if not user_pack:
            return render(request, 'user/my_progress.html', {
                'user_pack': None,
                'total_hours': total_hours,
                'total_practices': total_practices,
                'average_fulfilments': average_fulfilments,
                "extends_template": 'user/empty_template.html'
            })

        year = timezone.now().year
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        userstats = UserStats.objects.filter(idate__year=year, user=request.user)
        categories = Category.objects.all().order_by('order')
        userdata = []

        for i, month in enumerate(months):
            areasoflife = []
            totalminutes = 0
            monthstats = userstats.filter(idate__month=i + 1)

            for cat in categories:
                areasoflife.append({"name": cat.name, "minutes": 0})

            for stats in monthstats:
                if stats.spent_seconds > 0:
                    for area in areasoflife:
                        if area['name'] == stats.practice_session.affirmation.category.name:
                            area['minutes'] += round((stats.spent_seconds / 60))
                            totalminutes += round((stats.spent_seconds / 60))

            areasoflife.append({"name": "Total", "minutes": totalminutes})
            userdata.append({"month": month, "areasoflife": areasoflife})

        return render(request, 'user/my_progress.html', {
            'user_pack': user_pack,
            'total_hours': total_hours,
            'total_practices': total_practices,
            'average_fulfilments': average_fulfilments,
            "user_data": userdata,
            "year": year,
            "extends_template": 'user/empty_template.html'
        })


class PracticeTrackerYearly(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        isyear = True
        if not year:
            year = timezone.now().year
            isyear = False

        if year > timezone.now().year or year < 2015:
            return render(request, 'user/practice_tracker_yearly.html', {
                "user_data": None,
                "year": year,
                "is_year": isyear,
                "extends_template": 'base.html',
                "myprogress": 'False',
                "msg": 'Invalid year entered.. Please select a valid year from above dropdown'
            })

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        userstats = UserStats.objects.filter(idate__year=year, user=request.user)
        categories = Category.objects.all().order_by('order')
        userdata = []

        for i, month in enumerate(months):
            areasoflife = []
            totalminutes = 0
            monthstats = userstats.filter(idate__month=i + 1)

            for cat in categories:
                areasoflife.append({"name": cat.name, "minutes": 0})

            for stats in monthstats:
                if stats.spent_seconds > 0:
                    for area in areasoflife:
                        if area['name'] == stats.practice_session.affirmation.category.name:
                            area['minutes'] += round((stats.spent_seconds / 60))
                            totalminutes += round((stats.spent_seconds / 60))

            areasoflife.append({"name": "Total", "minutes": totalminutes})
            userdata.append({"month": month, "areasoflife": areasoflife})

        return render(request, 'user/practice_tracker_yearly.html', {
            "user_data": userdata,
            "year": year,
            "is_year": isyear,
            "extends_template": 'base.html',
            "myprogress": 'False'
        })


class PracticeTrackerMonthly(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        if not year:
            year = timezone.now().year
        if not month:
            month = timezone.now().month

        if year > timezone.now().year or year < 2015:
            return render(request, 'user/practice_tracker_monthly.html', {
                "user_data": None,
                "msg": 'Please select a valid year'
            })

        if month > 12 or month < 1:
            return render(request, 'user/practice_tracker_monthly.html', {
                "user_data": None,
                "msg": 'Please select a valid month'
            })

        num_days = monthrange(year, month)[1]
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        userstats = UserStats.objects.filter(idate__year=year, idate__month=month, user=request.user)
        categories = Category.objects.all().order_by('order')
        userdata = []

        total_weeks = round(num_days / 7)

        if num_days % 7 > 0:
            total_weeks += 1
        remaining_days = num_days % 7

        for week in range(1, total_weeks + 1):
            areasoflife = []
            days_name = []
            day_start_rang = week * 7 - 6
            day_end_rang = week * 7 + 1

            if week == total_weeks and remaining_days > 0:
                day_end_rang = week * 7 - 6 + remaining_days

            for day in range(day_start_rang, day_end_rang):
                days_name.append({"day": day})

            for cat in categories:
                days = []
                week_minutes = 0
                for day in range(day_start_rang, day_end_rang):
                    days.append({"day": day, "minutes": 0})

                for day in days:
                    daystats = userstats.filter(idate__day=day['day'])
                    for stat in daystats:
                        if stat.spent_seconds > 0:
                            if cat.name == stat.practice_session.affirmation.category.name:
                                day['minutes'] += round(stat.spent_seconds / 60)
                                week_minutes += round(stat.spent_seconds / 60)
                areasoflife.append({"name": cat.name, "days": days, 'week_minutes': week_minutes})

            userdata.append({"week": week, "areasoflife": areasoflife, "days_name": days_name})
            missing_days = []
            if remaining_days > 0:
                missing_days = range(7 - remaining_days)

        return render(request, 'user/practice_tracker_monthly.html', {
            'month_name': months[month - 1] + ' ' + str(year),
            'user_data': userdata,
            'missing_days': missing_days
        })


class PasswordForgot(FormView):

    def get(self, request, *args, **kwargs):
        return render(request, 'user/request_password_reset.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        if not email:
            return render(request, 'user/request_password_reset.html', {
                'error_no_input': 'yes', 'email': email
            })

        if not User.objects.filter(email=email).count():
            return render(request, 'user/request_password_reset.html', {
                'error_user_not_found': 'yes', 'email': email
            })

        user = User.objects.filter(email=email).last()

        pw_onetime_hash = create_default_hash()
        user.profile.pw_onetime_hash = pw_onetime_hash
        user.profile.save()

        send_html_mail(
            'Your new access',
            email,
            **{
                'text': "Remembering all the passwords we have is not easy. But it is not a problem, here you can reset"
                        " your password.",
                'link': 'https://%s%s' % (
                    request.META.get('HTTP_HOST'),
                    reverse('password_reset', kwargs={'onetime_hash': pw_onetime_hash})
                ),
                'link_name': 'Reset my password'
            }
        )
        return redirect(reverse('password_forgot_success'))


class PasswordReset(FormView):

    def get(self, request, *args, **kwargs):
        onetime_hash = kwargs.get('onetime_hash')

        user_profile = Profile.objects.filter(pw_onetime_hash=onetime_hash).last()
        if not user_profile:
            error = 'link is invalid'
            return render(request, 'user/password_reset.html', {
                'error': error, 'link_invalid': 'yes'
            })

        # invalidate the confirm hash
        now = timezone.now()
        user_profile.pw_onetime_hash = '%s-clicked-at-%s' % (
            onetime_hash, '%s_%s_%s_%s_%s' % (now.year, now.month, now.day, now.hour, now.minute)
        )
        user_profile.save()

        return render(request, 'user/password_reset.html', {
            'user_profile_id': user_profile.id
        })

    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_profile_id = request.POST.get('user_profile_id')

        if not Profile.objects.filter(id=user_profile_id).last():
            return render(request, 'user/password_reset.html', {
                'error': 'error while resetting'
            })

        if password1 != password1:
            return render(request, 'user/password_reset.html', {
                'error': 'passwords dont match'
            })

        user_profile = Profile.objects.get(id=user_profile_id)
        user = user_profile.user
        user.set_password(password2)
        user.save()

        login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')

        return redirect('%s?password_changed=1' % reverse('profile'))


class Practice(LoginRequiredMixin, DetailView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def practice_sessions(self, catid):
        affirmations = list(Affirmation.objects.filter(category_id=catid).values_list('id', flat=True))
        return PracticeSession.objects.filter(affirmation_id__in=affirmations).order_by('order')

    def get(self, request, *args, **kwargs):

        user_pack = Pack.objects.filter(user=request.user).last()

        if not user_pack:
            return render(request, 'user/practice-session.html', {
                'user_pack': None,
                'categories_in_use': None,
                'page_text': DashboardPage.objects.last()
            })

        practice_session_ids = list(
            user_pack.practice_sessions.all().values_list('id', flat=True)
        )

        affirmation_ids = list(
            PracticeSession.objects.filter(id__in=practice_session_ids).values_list('affirmation_id', flat=True)
        )

        used_category_ids = list(
            Affirmation.objects.filter(id__in=affirmation_ids).values_list('category_id', flat=True)
        )

        categories_in_use = Category.objects.filter(id__in=used_category_ids).order_by('order')

        for cat in categories_in_use:
            cat.practice_sessions = self.practice_sessions(cat.id)

        return render(request, 'user/practice-session.html', {
            'user_pack': user_pack,
            'categories_in_use': categories_in_use,
            'practice_session_ids': practice_session_ids,
            'page_text': DashboardPage.objects.last()
        })


class Dashboard(LoginRequiredMixin, DetailView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        return render(request, 'user/dashboard.html')


@login_required(login_url='/user/login/')
def process_payment(request):
    user = request.user
    stripeToken = request.POST.get('stripeToken')
    plan_id = request.POST.get('plan_id')

    # remaining_days = 0

    stripe.api_key = TEST_API_KEY
    try:
        customer = stripe.Customer.retrieve(user.profile.stripe_customer_id)
        customer.source = stripeToken
        customer.save()
    except stripe.error.CardError as e:
        return HttpResponse(e, status=400)

    try:
        stripe_subscription = stripe.Subscription.retrieve(user.profile.stripe_subscription_id)
        if stripe_subscription:
            # subscription_from = datetime.datetime.fromtimestamp(stripe_subscription.current_period_start).date()
            # subscription_to = datetime.datetime.fromtimestamp(stripe_subscription.current_period_end).date()
            # remaining_days = (subscription_to - subscription_from).days
            stripe.Subscription.delete(user.profile.stripe_subscription_id)
            user.profile.stripe_subscription_id = ''
            user.profile.save()
    except stripe.error.InvalidRequestError:
        pass

    stripe_subscription = stripe.Subscription.create(
        customer=user.profile.stripe_customer_id,
        items=[{"plan": plan_id}],
        # trial_period_days=remaining_days,
    )
    user.profile.stripe_subscription_id = stripe_subscription.id
    user.profile.save()

    return HttpResponse('ok')


@login_required(login_url='/user/login/')
def delete_subscription(request):
    password = request.POST.get('password')
    user = request.user

    if user.check_password(raw_password=password):
        stripe.api_key = TEST_API_KEY
        stripe.Subscription.delete(user.profile.stripe_subscription_id)
        user.profile.stripe_subscription_id = ''
        user.profile.save()

        return render(request, 'user/profile_settings.html', {
            'msg': 'Your subscription was deleted successfully. To use the service, you need to subscribe again.',
            'isDelete': True
        })

    else:
        return render(request, 'user/profile_settings.html', {
            'error': 'Password is not correct. Please try again.'
        })


@login_required(login_url='/user/login/')
def redeem_code(request):
    code = request.POST.get('code')
    user = request.user

    if Promotion.objects.filter(code=code, expires_at__lt=timezone.now()).count():
        user.profile.promo_code = code
        user.profile.save()

        return render(request, 'user/profile.html', {
            'msg': 'Your promotion code was successfully redeemed. It will be applied in the next billing cycle.'
        })

    return render(request, 'user/profile.html', {
        'error': 'Code is invalid'
    })
