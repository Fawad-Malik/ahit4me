from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse

from iow.apps.core.models import Base
from iow.apps.categories.models import (
    Category, SubCategory
)


def order_next_number_affirmation():
    no = Affirmation.objects.count()
    return no + 1 if no else 1


# class Category(Base):
#     name = models.CharField(max_length=100)
#     order = models.IntegerField(default=1)

#     def __str__(self):
#         return 'Category: %s ' % self.name

#     def practice_sessions(self):
#         affirmations = list(self.category_affirmations.values_list('id', flat=True))
#         return PracticeSession.objects.filter(affirmation_id__in=affirmations).order_by('order')

#     class Meta:
#         verbose_name_plural = '1. Category'


# class SubCategory(Base):
#     category = models.ForeignKey(Category, related_name='category_subcats', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     order = models.IntegerField(default=1)

#     def __str__(self):
#         return 'Sub Category: %s ' % self.name

#     class Meta:
#         verbose_name_plural = '2. Sub Category'


class Affirmation(Base):
    category = models.ForeignKey(
        Category, related_name='category_affirmations', on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(
        SubCategory, related_name='subcategory_affirmations', on_delete=models.CASCADE, null=True
    )
    order = models.IntegerField(default=order_next_number_affirmation)
    title = models.CharField(max_length=100, default='')

    def ordered_affirmations(self):
        return self.affirmation_texts.order_by('order')

    class Meta:
        verbose_name_plural = 'Affirmations'

    def __str__(self):
        return '[Cat: %s, Subcat: %s] %s' % (
            self.category.name, self.subcategory.name, self.title
        )


class AffirmationText(Base):
    affirmation = models.ForeignKey(
        Affirmation, related_name='affirmation_texts', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    text = models.TextField(default='')
    mantra = models.TextField(default='')
    repeat = models.BooleanField(verbose_name='Repeat', default=False)
    repetition = models.IntegerField(default=1, verbose_name='Repetitions')
    cells = models.IntegerField(default=1, verbose_name='Cells')

    def get_rep_list(self):
        return list(range(self.repetition))

    def __str__(self):
        return '%s ... ' % self.text[:150]


class PracticeSession(Base):
    name = models.CharField(max_length=100, default='', blank=True)
    user = models.ForeignKey(
        User, related_name='user_practice_sessions', on_delete=models.DO_NOTHING)
    purpose = models.CharField(max_length=100, default='', blank=True)
    affirmation = models.ForeignKey(
        Affirmation, related_name='affirmations_in_practice_sessions', on_delete=models.CASCADE
    )
    music_file = models.FileField(
        upload_to='mp3s/%Y/%m/%d', default='', blank=True)
    order = models.IntegerField(default=0)

    @property
    def title(self):
        return self.affirmation.title

    def get_absolute_url(self):
        return reverse('practice_detail', kwargs={
            'slug': slugify(self.affirmation.title), 'pk': self.id
        })

    def __str__(self):
        return self.affirmation.title

    class Meta(object):
        verbose_name_plural = 'Practice Sessions'
        ordering = ['order']


class Pack(Base):
    user = models.ForeignKey(
        User, related_name='user_packs', on_delete=models.CASCADE)
    practice_sessions = models.ManyToManyField(
        PracticeSession, related_name='ps_in_packs')

    def __str__(self):
        return 'user pack _id: %s' % self.id

    def count_repeated_times(self, practice_id):
        self.repeated = models.F('repeated') + 1
        self.save()

    class Meta:
        verbose_name_plural = 'User Packs'


class Image(Base):
    practice_session = models.ManyToManyField(
        PracticeSession, related_name='practice_session_images')
    related_tags = models.CharField(
        max_length=200, help_text='comma separated words e.g. happy, money')
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.related_tags

    class Meta:
        verbose_name_plural = 'Images for Practice Sessions'
