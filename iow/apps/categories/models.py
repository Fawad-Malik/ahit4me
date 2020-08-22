from django.db import models
# from django.contrib.auth.models import User
# from django.utils.text import slugify
# from django.shortcuts import reverse

from iow.apps.core.models import Base


class Category(Base):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=1)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        verbose_name_plural = '1. Category'

    def get_sub_categories(self):
        return SubCategory.objects.filter(category=self)


class SubCategory(Base):
    category = models.ForeignKey(
        Category, related_name='category_subcats', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=1)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        verbose_name_plural = '2. Sub Category'


class SubCatTextBoxes(Base):
    subcategory = models.ForeignKey(
        SubCategory, related_name='sub_cat_text_boxes', on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=100)
    order = models.IntegerField(default=1)

    def __str__(self):
        return '%s ' % self.text

    class Meta:
        verbose_name_plural = 'Text Boxes'
        verbose_name = 'Text Box'
