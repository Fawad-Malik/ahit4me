from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from iow.apps.core.models import Base
from iow.apps.practice.models import PracticeSession


class UserStats(Base):
    practice_session = models.ForeignKey(
        PracticeSession, related_name='ps_stats', null=True, on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        User, related_name='user_stats', null=True, on_delete=models.CASCADE)
    number_of_repetitions = models.IntegerField(default=0)
    spent_seconds = models.IntegerField(default=0)
    fulfilment = models.IntegerField(null=True)

    def __str__(self):
        return 'user stats: %s' % self.id

    @classmethod
    def get_or_create_user_stats(cls, user, now, practice_id):
        """
        a user has only one stats instance per day
        """

        query_ = {
            'idate__day': now.day,
            'idate__month': now.month,
            'idate__year': now.year,
            'practice_session_id': practice_id
        }

        if not user.user_stats.filter(**query_).count():
            user_stats = user.user_stats.create(
                idate=now, practice_session_id=practice_id)
        else:
            user_stats = user.user_stats.filter(**query_).last()

        return user_stats


def count_practice_repetitions(self, practice_id):
    user_stats = UserStats.get_or_create_user_stats(
        user=self, now=timezone.now(), practice_id=practice_id)
    user_stats.number_of_repetitions = models.F('number_of_repetitions') + 1
    user_stats.save()


def update_fulfilment(self, practice_id, fulfilment):
    user_stats = UserStats.get_or_create_user_stats(
        user=self, now=timezone.now(), practice_id=practice_id)
    if not user_stats.fulfilment:
        user_stats.fulfilment = fulfilment
    else:
        user_stats.fulfilment = models.F('fulfilment') + fulfilment
    user_stats.save()


def count_spent_seconds(self, practice_id):
    user_stats = UserStats.get_or_create_user_stats(
        user=self, now=timezone.now(), practice_id=practice_id)
    user_stats.spent_seconds = models.F('spent_seconds') + 1
    user_stats.save()


User.add_to_class('count_practice_repetitions', count_practice_repetitions)
User.add_to_class('update_fulfilment', update_fulfilment)
User.add_to_class('count_spent_seconds', count_spent_seconds)
