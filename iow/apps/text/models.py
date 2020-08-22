from django.db import models
from iow.apps.categories.models import Category
from iow.apps.practice.models import PracticeSession


class LandingPage(models.Model):
    headline = models.TextField(default='Ability & Habit Improving Technology 4 Me')
    text = models.TextField(default='Technology to Improve Your Habits of Abilities to Improve Your life. '
                                    'Use Your Thoughts to Create the Habits You Need to Enjoy the Life You Desire')

    def __str__(self):
        return self.headline


class DiscoverPage(models.Model):
    category = models.ForeignKey(Category, related_name='discover_category', verbose_name='Category',
                                 on_delete=models.CASCADE)
    practice_session = models.ForeignKey(PracticeSession, related_name='discover_category',
                                         verbose_name='Practice Session', on_delete=models.CASCADE)
    dream = models.CharField(max_length=350, verbose_name='Dream')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.dream


class DashboardPage(models.Model):
    headline = models.TextField(default='My Packs')
    text = models.TextField(default='Program your nervous system with what you want in your life. '
                                    'Imagination will strengthen your ability to think & live! '
                                    'Remember Best Effort = Best Results!')

    def __str__(self):
        return self.headline


class KnowledgePage(models.Model):
    headline = models.TextField(default='Knowledge')
    text = models.TextField(default='')

    def __str__(self):
        return self.headline
