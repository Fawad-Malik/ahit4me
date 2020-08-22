from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify

from iow.apps.core.models import Base
from iow.apps.categories.models import (
    Category, SubCategory
)


class Knowledge(Base):
    category = models.ForeignKey(Category, related_name='category_knowledge', on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(
        SubCategory, related_name='subcategory_knowledge', on_delete=models.CASCADE, null=True
    )
    user = models.ForeignKey(User, related_name='knowledges_entered_by_user', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '1. Knowledge'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('knowledge_detail', kwargs={'slug': slugify(self.title), 'pk': self.id})


class KnowledgeContent(Base):
    knowledge = models.ForeignKey(Knowledge, related_name='knowledge_contents', on_delete=models.CASCADE)
    content = models.TextField(default='', blank=True)
    image = models.ImageField(upload_to='imgs/%Y/%m/%d', blank=True)
    file = models.FileField(upload_to='imgs/%Y/%m/%d', blank=True)
    embed_code = models.TextField(default='', blank=True)

    class Meta:
        verbose_name_plural = '2. Knowledge Content'

    def __str__(self):
        return '%s' % self.id


class Help(Base):
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title


