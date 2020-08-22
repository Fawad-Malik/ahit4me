from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from .models import Want, InstructionVideos, Settings, FirstLevelContent, SecondLevelContent, ThirdLevelContent

import pdb
import os
import xlrd
from django.core.files.storage import FileSystemStorage
from iow.apps.categories.models import Category, SubCategory
from iow.apps.causalforces.models import Current_Reality
from django.conf import settings
class CauseAndEffects(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('order')
        sub_cats_len = []

        for category in categories:
            sub_cats_len.append(len(category.get_sub_categories()))

        max_len = max(sub_cats_len)

        table_rows = []
        for i in range(max_len):
            row = []
            for category in categories:
                try:
                    row.append({"category": category.name,
                                "sub_cat": category.get_sub_categories()[i]})
                except IndexError:
                    row.append({"category": None, "sub_cat": None})
            table_rows.append(row)

        return render(request, 'causeandeffects/index.html', {
            'categories': categories,
            'table_rows': table_rows,
        })


class DetailPage(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category')
        sub_cat = kwargs.get('sub_cat')
        want_id = kwargs.get('want_id')
        user_benefits = None

        try:
            category = Category.objects.get(name=category)
        except Category.DoesNotExist:
            category = None

        try:
            sub_cat = SubCategory.objects.get(name=sub_cat, category=category)
        except SubCategory.DoesNotExist:
            sub_cat = None

        if sub_cat:
            want = None
            why_wants = None
            current_ability = None

            try:
                instruction_videos = InstructionVideos.objects.all()
                instruction_videos = instruction_videos[0]
            except InstructionVideos.DoesNotExist:
                instruction_videos = None
            except IndexError:
                instruction_videos = None

            try:
                settings = Settings.objects.all()
                settings = settings[0]
            except Settings.DoesNotExist:
                settings = None
            except IndexError:
                settings = None

            try:
                wants = Want.objects.filter(
                    category=category, subcategory=sub_cat)
            except Want.DoesNotExist:
                wants = None

            if want_id:
                try:
                    want = Want.objects.get(pk=want_id)
                except Want.DoesNotExist:
                    want = None

            if want:
                try:
                    current_reality = Current_Reality.objects.get(
                        related_want=want)
                except Current_Reality.DoesNotExist:
                    current_reality = None
            else:
                current_reality = None

            return render(request, 'causeandeffects/detail.html', {
                "area_of_life": category,
                "sub_area_of_life": sub_cat,
                "wants": wants,
                "want_details": want,
                "instruction_videos": instruction_videos,
                "settings": settings,
                'current_reality': current_reality
            })
        else:
            return render(request, 'causeandeffects/detail.html', {})



