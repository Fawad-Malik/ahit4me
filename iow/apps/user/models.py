import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from djstripe.settings import TEST_API_KEY
from djstripe.models import Customer, Subscription
from djstripe.models import Plan
from iow.apps.core.models import Base
from iow.apps.core.utils import convert_seconds_to_hours
from datetime import datetime as dtlib
import stripe

def default_time(timetype):
    if timetype == 'start':
        time = dtlib.strptime('00:00:00', "%H:%M:%S")
        return dtlib.time(time)
    else:
        time = dtlib.strptime('23:59:59', "%H:%M:%S")
        return dtlib.time(time)

class User_Subscription(Base):
    ustripe_subscription_id = models.CharField(max_length=60)
    ustripe_subscription_date=models.DateTimeField()
    ustripe_subscription_plan = models.CharField(max_length=60, default='')

class Profile(Base):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    confirm_hash = models.CharField(max_length=60, default='')
    pw_onetime_hash = models.CharField(max_length=60, default='')
    promo_code = models.CharField(max_length=100, default='')

    braintree_customer_id = models.IntegerField(null=True)
    braintree_payment_method_token = models.CharField(max_length=100, default='')
    subscription_id = models.CharField(max_length=100, default='')
    stripe_customer_id = models.CharField(max_length=200, default='', null=True)
    stripe_subscription_id = models.CharField(max_length=200, default='', null=True)

    @property
    def has_active_subscription(self):
        if self.user.profile.stripe_subscription_id:
            user_subscription_check=User_Subscription.objects.filter(ustripe_subscription_id=self.user.profile.stripe_subscription_id).exists()
            if user_subscription_check:
                user_subscription_test=User_Subscription.objects.get(ustripe_subscription_id=self.user.profile.stripe_subscription_id)
            
            if not user_subscription_check:
                stripe_subscription = None
                stripe.api_key = TEST_API_KEY
                stripe_subscription = stripe.Subscription.retrieve(self.user.profile.stripe_subscription_id)
                user_subscription_test=User_Subscription.objects.create(ustripe_subscription_id=self.user.profile.stripe_subscription_id,ustripe_subscription_date=datetime.datetime.fromtimestamp(stripe_subscription.current_period_end).date(), ustripe_subscription_plan=stripe_subscription['items']['data'][0]["plan"]["id"])
              
            if user_subscription_test.ustripe_subscription_date.date()>=datetime.date.today():
                return True
            elif user_subscription_test.ustripe_subscription_date.date()<datetime.date.today():
                stripe_subscription = None
                stripe.api_key = TEST_API_KEY
                stripe_subscription = stripe.Subscription.retrieve(self.user.profile.stripe_subscription_id)
                if datetime.datetime.fromtimestamp(stripe_subscription.current_period_end).date()>= datetime.date.today():
                    User_Subscription.objects.filter(ustripe_subscription_id=self.user.profile.stripe_subscription_id).update(ustripe_subscription_date=datetime.datetime.fromtimestamp(stripe_subscription.current_period_end).date(), ustripe_subscription_plan=stripe_subscription['items']['data'][0]["plan"]["id"])
                    return True
                else:
                    return False
        if not stripe_subscription:
            return False
        
        

    def total_session_hours(self):
        total_seconds = self.user.user_stats.aggregate(total_seconds=models.Sum('spent_seconds'))
        total_seconds = 0 if not total_seconds.get('total_seconds') else total_seconds.get('total_seconds')
        return convert_seconds_to_hours(secs=total_seconds)

    def total_repetitions(self):
        total_repetitions__ = self.user.user_stats.aggregate(total_repetitions=models.Sum('number_of_repetitions'))

        total_repetitions = 0
        if total_repetitions__.get('total_repetitions'):
            total_repetitions = total_repetitions__.get('total_repetitions')

        return total_repetitions

    def total_fulfillment(self):
        total_fulfilment = self.user.user_stats.aggregate(total_fulfilment=models.Avg('fulfilment'))
        return 0 if not total_fulfilment.get('total_fulfilment') else total_fulfilment.get('total_fulfilment')

    def _get_last_month_range(self):
        now = timezone.now()
        last_month = now - datetime.timedelta(weeks=4)

        last_month_days = self.user.user_stats.filter(
            idate__month=last_month.month, idate__year=now.year
        ).order_by('idate__day')[:now.day]

        return last_month_days

    def _get_this_month_range(self):
        now = timezone.now()
        this_month_stats = self.user.user_stats.filter(
            idate__month=now.month, idate__year=now.year
        )
        return this_month_stats

    def __get_range(self, range_type='month', range_mode='last'):
        # per default yesterday data
        time_range = self._get_yesterday_range()

        if range_type == 'day':
            if range_mode == 'last':
                time_range = self._get_yesterday_range()
            else:
                time_range = self._get_today_range()

        if range_type == 'week':
            if range_mode == 'last':
                time_range = self._get_last_week_range()
            else:
                time_range = self._get_this_week_range()

        if range_type == 'month':
            if range_mode == 'last':
                time_range = self._get_last_month_range()
            else:
                time_range = self._get_this_month_range()

        if range_type == 'year':
            if range_mode == 'last':
                time_range = self._get_last_year_range()
            else:
                time_range = self._get_this_year_range()

        return time_range

    def _get_hours_for(self, range_type='month', range_mode='last'):
        time_range = self.__get_range(range_type=range_type, range_mode=range_mode)

        range_seconds = time_range.aggregate(total_seconds=models.Sum('spent_seconds'))

        range_seconds = 0 if not range_seconds.get('total_seconds') else range_seconds.get('total_seconds')
        return convert_seconds_to_hours(secs=range_seconds)

    def _get_repetitions_for(self, range_type='month', range_mode='last'):
        time_range = self.__get_range(range_type=range_type, range_mode=range_mode)

        range_repetitions__ = time_range.aggregate(
            total_repetitions=models.Sum('number_of_repetitions')
        )
        last_month_repetitions = 0
        if range_repetitions__.get('total_repetitions'):
            last_month_repetitions = range_repetitions__.get('total_repetitions')

        return last_month_repetitions

    def _get_fulfilment_for(self, range_type='month', range_mode='last'):
        time_range = self.__get_range(range_type=range_type, range_mode=range_mode)

        range_fulfilment__ = time_range.aggregate(total_fulfilment=models.Sum('fulfilment'))

        range_fulfilment = 0
        if range_fulfilment__.get('total_fulfilment'):
            range_fulfilment = range_fulfilment__.get('total_fulfilment')
        return range_fulfilment

    def weekly_progress(self):
        """
        same as monthly_progress, but just weekly time range
        :return:
        """
        last_week_range_hours = self._get_hours_for(range_type='week', range_mode='last')
        last_week_repetitions = self._get_repetitions_for(range_type='week', range_mode='last')
        last_week_fulfilment = self._get_fulfilment_for(range_type='week', range_mode='last')

        this_week_range_hours = self._get_hours_for(range_type='week', range_mode='this')
        this_week_repetitions = self._get_repetitions_for(range_type='week', range_mode='this')
        this_week_fulfilment = self._get_fulfilment_for(range_type='week', range_mode='this')

        last_week_total = last_week_range_hours + last_week_repetitions + last_week_fulfilment
        this_week_total = this_week_range_hours + this_week_repetitions + this_week_fulfilment

        if not last_week_total:
            # if last time was zero, this time must be the starting time, so give 100%
            return 100

        percentage = this_week_total * 100 / last_week_total

        growth = percentage - 100

        return float("%.2f" % growth)

    def monthly_progress(self):
        """
        progress = total_hours + total number of repetitions + total fulfilment ---> in a given time range
        :return: Decimal number e.g. 97.34%
        """
        last_month_range_hours = self._get_hours_for(range_type='month', range_mode='last')
        last_month_repetitions = self._get_repetitions_for(range_type='month', range_mode='last')
        last_month_fulfilment = self._get_fulfilment_for(range_type='month', range_mode='last')

        this_month_range_hours = self._get_hours_for(range_type='month', range_mode='this')
        this_month_repetitions = self._get_repetitions_for(range_type='month', range_mode='this')
        this_month_fulfilment = self._get_fulfilment_for(range_type='month', range_mode='this')

        last_month_total = last_month_range_hours + last_month_repetitions + last_month_fulfilment
        this_month_total = this_month_range_hours + this_month_repetitions + this_month_fulfilment

        if not last_month_total:
            # if last time was zero, this time must be the starting time, so give 100%
            return 100

        percentage = this_month_total * 100 / last_month_total

        growth = percentage - 100

        return float("%.2f" % growth)

    def annual_progress(self):
        """
        same as monthly_progress, but just annual time range
        :return:
        """

        last_year_range_hours = self._get_hours_for(range_type='year', range_mode='last')
        last_year_repetitions = self._get_repetitions_for(range_type='year', range_mode='last')
        last_year_fulfilment = self._get_fulfilment_for(range_type='year', range_mode='last')

        this_year_range_hours = self._get_hours_for(range_type='year', range_mode='this')
        this_year_repetitions = self._get_repetitions_for(range_type='year', range_mode='this')
        this_year_fulfilment = self._get_fulfilment_for(range_type='year', range_mode='this')

        last_year_total = last_year_range_hours + last_year_repetitions + last_year_fulfilment
        this_year_total = this_year_range_hours + this_year_repetitions + this_year_fulfilment

        if not last_year_total:
            # if last time was zero, this time must be the starting time, so give 100%
            return 100

        percentage = this_year_total * 100 / last_year_total

        growth = percentage - 100

        return float("%.2f" % growth)

    def _get_today_range(self):
        now = timezone.now()
        return self.user.user_stats.filter(idate__day=now.day, idate__month=now.month, idate__year=now.year)

    def _get_yesterday_range(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        return self.user.user_stats.filter(
            idate__day=yesterday.day, idate__month=yesterday.month, idate__year=yesterday.year
        )

    def _get_last_week_range(self):
        now = timezone.now()
        last_week_end_range = now - datetime.timedelta(weeks=1)
        last_week_start_range = last_week_end_range - datetime.timedelta(days=now.weekday())
        return self.user.user_stats.filter(idate__gt=last_week_start_range, idate__lte=last_week_end_range)

    def _get_this_week_range(self):
        now = timezone.now()
        this_week_start_range = now - datetime.timedelta(days=now.weekday())
        return self.user.user_stats.filter(idate__gt=this_week_start_range)

    def _get_last_year_range(self):
        now = timezone.now()
        last_year_end_range = now - datetime.timedelta(weeks=52)
        last_year_start_range = last_year_end_range - datetime.timedelta(weeks=now.isocalendar()[1])
        return self.user.user_stats.filter(idate__gt=last_year_start_range, idate__lte=last_year_end_range)

    def _get_this_year_range(self):
        now = timezone.now()
        return self.user.user_stats.filter(idate__year=now.year)

    def __str__(self):
        return self.user.username

    def last_subscription(self):
        return self.user.user_subscriptions.last()

    @property
    def can_have_more_sessions(self):
        """
        new user can have 1 session for free.
        """
        if not self.user.user_packs.last():
            return True

        user_pack = self.user.user_packs.last()
        if user_pack.practice_sessions.all().count() < 1:
            return True

        return self.has_active_subscription


class Promotion(Base):
    code = models.CharField(max_length=100)
    sale_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    expires_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.code


class Subscription(Base):
    """
    mode can be:
        monthly
        quarterly
        annual
    """
    user = models.ForeignKey(User, related_name='user_subscriptions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    mode = models.CharField(max_length=20)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return 'user [%s] has paid: %s. Date: %s' % (
            self.user.username, self.amount, self.idate.strftime('%m-%d-%Y')
        )


class UserSettings(Base):
    user = models.OneToOneField(User, related_name='user_settings', on_delete=models.CASCADE)
    timeline_starttime = models.TimeField(default=default_time('start'), auto_now=False, auto_now_add=False,
                                          verbose_name="Timeline Start Time")
    timeline_endtime = models.TimeField(default=default_time('end'), auto_now=False, auto_now_add=False,
                                        verbose_name="Timeline End Time")
    duration_in_secs = models.IntegerField(default=3)
    font_size = models.IntegerField(default=24)
    brightness = models.IntegerField(default=100)
    ps_cycles = models.IntegerField(default=1)
    ps_ismantra = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'User Settings'
        verbose_name = 'User Setting'

    def __str__(self):
        return self.user.username


# create user profile on the fly
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        profile = Profile(user=user)
        stripe.api_key = TEST_API_KEY
        try:
            stripe_customer = stripe.Customer.create(email=user.email)
            profile.stripe_customer_id = stripe_customer.id
            Customer.sync_from_stripe_data(stripe_customer)
            stripe_subscription = stripe.Subscription.create(customer=stripe_customer.id,
                                                             items=[{"plan": "iow_monthly_payment"}],
                                                             trial_from_plan=True)
            profile.stripe_subscription_id = stripe_subscription.id
            Subscription.sync_from_stripe_data(stripe_subscription)
        except Exception as e:
            pass
        else:
            profile.save()
            usersettings = UserSettings(user=user)
            usersettings.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        stripe.api_key = TEST_API_KEY
        try:
            stripe.Customer.delete(instance.stripe_customer_id)
        except Exception as e:
            pass
        else:
            instance.user.delete()
