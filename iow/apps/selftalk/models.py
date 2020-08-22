from django.db import models
from iow.apps.core.models import Base
from django.contrib.auth.models import User
from iow.apps.categories.models import Category, SubCategory
# Create your models here.

class SelfTalk(Base):
    order = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, related_name='category_st', verbose_name="Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, related_name='subcategory_st', verbose_name="SubCategory", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="name")
    low_low = models.CharField(max_length=200, verbose_name="low first")
    low_high = models.CharField(max_length=200, verbose_name="low second")
    low_medium = models.CharField(max_length=200, verbose_name="low third")
    high_low = models.CharField(max_length=200, verbose_name="high first")
    high_high = models.CharField(max_length=200, verbose_name="high second")
    high_medium = models.CharField(max_length=200, verbose_name="high third")
    medium_low = models.CharField(max_length=200, verbose_name="medium first")
    medium_high = models.CharField(max_length=200, verbose_name="medium second")
    medium_medium = models.CharField(max_length=200, verbose_name="medium third")
    polarity_self_talk = models.CharField(max_length=200, verbose_name="polarity", null=True)
    function_self_talk = models.CharField(max_length=200, verbose_name="function", null=True)
    emotion_self_talk = models.CharField(max_length=200, verbose_name="emotion", null=True)

class UserST(Base):
    userId = models.ForeignKey(User, verbose_name="User", related_name='user_fk',  on_delete=models.CASCADE,null=True)
    selftalk=models.ForeignKey(SelfTalk, verbose_name="Selftalk", related_name='selftalk_fk',  on_delete=models.CASCADE,null=True)
    before = models.CharField(max_length=50, verbose_name="Before",null=True)
    during = models.CharField(max_length=50, verbose_name="During",null=True)
    after = models.CharField(max_length=50, verbose_name="After",null=True)
    who_am_i_talking_to = models.CharField(max_length=50, verbose_name="Who am i talking to",null=True)
    is_now_a_good_time_to_talk = models.CharField(max_length=50, verbose_name="Is now a good time to talk to this person in my head",null=True)
    times_a_day = models.CharField(max_length=50, verbose_name="Times a day",null=True)
    times_it_last = models.CharField(max_length=50, verbose_name="Times it Last",null=True)
    how_intense = models.CharField(max_length=50, verbose_name="How intense",null=True)
    polarity = models.CharField(max_length=50, verbose_name="Polarity",null=True)
    function = models.CharField(max_length=50, verbose_name="Function",null=True)
    emotion = models.CharField(max_length=50, verbose_name="Emotion",null=True)