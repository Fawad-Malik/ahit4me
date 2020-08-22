import json

from django.shortcuts import HttpResponse, redirect, render, reverse
from django.utils.text import slugify, mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date

from .models import Affirmation, Image, PracticeSession
from iow.apps.categories.models import Category, SubCategory
from iow.apps.user.models import UserSettings
from iow.apps.numbers.models import UserStats
from iow.apps.text.models import DiscoverPage


def fetch_sub_cats(request, cat_id):
    category = Category.objects.get(id=cat_id)

    subcats = list(category.category_subcats.order_by('order').values_list('id', 'name'))

    subcats_list = []
    for subcat in subcats:
        d_ = {
            'id': subcat[0],
            'name': subcat[1]
        }
        subcats_list.append(d_)

    return HttpResponse(json.dumps(subcats_list), content_type='application/json')


@login_required(login_url='/user/login/')
def remove_from_pack(request, practice_id):
    try:
        _ = PracticeSession.objects.get(id=practice_id)
    except PracticeSession.DoesNotExist:
        return redirect('%s?not_found=1' % reverse('dashboard'))

    user_pack = request.user.user_packs.last()
    if not user_pack:
        return redirect('%s?not_found=1' % reverse('dashboard'))

    user_pack.practice_sessions.remove(practice_id)

    return redirect('%s?removed=1' % reverse('dashboard'))


def fetch_affirmations(request, sub_cat_id):
    subcategory = SubCategory.objects.get(id=sub_cat_id)

    affirmations = list(subcategory.subcategory_affirmations.order_by('order').values_list('id', 'title'))

    affirmations_list = []
    for affirmation in affirmations:
        d_ = {
            'id': affirmation[0],
            'title': affirmation[1]
        }
        affirmations_list.append(d_)

    return HttpResponse(json.dumps(affirmations_list), content_type='application/json')


def fetch_affirmation_text(request, affirmation_id):
    affirmation = Affirmation.objects.get(id=affirmation_id)

    affirmation_texts = list(affirmation.affirmation_texts.order_by('order').values_list('id', 'text'))

    affirmations_list = []
    for affirm_text in affirmation_texts:
        d_ = {
            'id': affirm_text[0],
            'text': mark_safe(affirm_text[1])
        }
        affirmations_list.append(d_)

    return HttpResponse(json.dumps(affirmations_list), content_type='application/json')


def set_seconds(request, practice_id):
    response = 'untouched'

    if request.is_ajax():
        user_settings = UserSettings.objects.get(user=request.user)

        seconds = request.GET.get('seconds', 6)
        font_size = request.GET.get('font_size', 24)
        brightness = request.GET.get('brightness', 100)
        ps_cycles = request.GET.get('ps_cycles', 1)
        ismantra = request.GET.get('isMantra', "false")
        ps_ismantra = False

        if user_settings.duration_in_secs != int(seconds):
            user_settings.duration_in_secs = int(seconds)

        if user_settings.font_size != int(font_size):
            user_settings.font_size = int(font_size)

        if user_settings.brightness != int(brightness):
            user_settings.brightness = int(brightness)

        if user_settings.ps_cycles != int(ps_cycles):
            user_settings.ps_cycles = int(ps_cycles)

        if ismantra:
            if ismantra == 'false':
                ps_ismantra = False
            else:
                ps_ismantra = True

        user_settings.ps_ismantra = ps_ismantra

        user_settings.save()
        response = 'second saved to %s, font_size saved to %s and brightness saved to %s' % (
        seconds, font_size, brightness)

    return HttpResponse(response)


def practice_sessions(self):
    affirmations = list(Affirmation.objects.filter(category_id=self).values_list('id', flat=True))
    return PracticeSession.objects.filter(affirmation_id__in=affirmations).order_by('order')


class DiscoverView(CreateView):

    def get(self, request, *args, **kwargs):

        all_categories = Category.objects.order_by('order')

        for cat in all_categories:
            cat.practice_sessions = practice_sessions(cat.id)

        return render(request, 'practice/practice_exercises.html', {
            'all_categories': all_categories,
            # 'page_text': DiscoverPage.objects.last()
        })

    def post(self, request, *args, **kwargs):

        if request.is_ajax() and request.user.is_authenticated:
            user = request.user

            ps_session = PracticeSession.objects.get(pk=request.POST.get('session_id'))

            if not user.user_packs.count():
                user_pack = user.user_packs.create()
            else:
                user_pack = user.user_packs.last()

            user_practice_session_ids = list(user_pack.practice_sessions.values_list('id', flat=True))

            if ps_session not in user_practice_session_ids:
                user_pack.practice_sessions.add(ps_session)

            return HttpResponse('ja ajax')

        return HttpResponse('no ajax', status=401)


class PracticeDetail(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        practice_id = kwargs.get('pk')
        practice = PracticeSession.objects.get(pk=practice_id)
        total_secs = 0
        today_secs = 0
        total_reps = 0
        practice.affirmation.category.dreams = DiscoverPage.objects.filter(category_id=practice.affirmation.category.id).order_by('order')

        try:
            user_stats = UserStats.objects.filter(user=request.user, practice_session=practice_id)
            for log in user_stats:
                if log.spent_seconds:
                    total_secs += log.spent_seconds
                if log.number_of_repetitions:
                    total_reps += log.number_of_repetitions
            today_secs = UserStats.objects.filter(user=request.user, practice_session=practice_id,
                                                  idate__date=date.today()).aggregate(Sum('spent_seconds'))
            if today_secs['spent_seconds__sum']:
                today_secs = "%.1f" % (today_secs['spent_seconds__sum'] / 60)
            else:
                today_secs = 0
        except UserSettings.DoesNotExist:
            total_secs = 0
            today_secs = 0
            total_reps = 0

        try:
            user_settings = UserSettings.objects.get(user=request.user)
        except UserSettings.DoesNotExist:
            user_settings = {
                "duration_in_secs": 3,
                "font_size": 24,
                "brightness": 100,
                "ps_cycles": 1,
                "ps_ismantra": False
            }

        images = Image.objects.filter(default=False)

        return render(request, 'practice/detail.html', {
            'practice': practice,
            'images': images,
            'user_settings': user_settings,
            'reps_done': total_reps,
            'today_secs': today_secs,
            'total_time': "%.1f" % (total_secs / 60 / 60)
        })

    def post(self, request, *args, **kwargs):
        selected_images = request.POST.getlist('ps_images')
        practice_id = kwargs.get('pk')

        practice = PracticeSession.objects.get(pk=practice_id)

        selected_images = [int(img_id) for img_id in selected_images]

        practice.practice_session_images.clear()

        practice.practice_session_images.add(*selected_images)

        return redirect('%s?created=1' % reverse('practice_detail', kwargs={
            'slug': slugify(practice.title),
            'pk': practice_id
        }))


class PracticePlayView(LoginRequiredMixin, CreateView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        practice_id = kwargs.get('pk')

        practice = PracticeSession.objects.get(pk=practice_id)
        user_settings = UserSettings.objects.get(user=request.user)

        request.user.count_practice_repetitions(practice_id=practice_id)

        practice_images = practice.practice_session_images.all()

        if not practice_images.count():
            practice_images = Image.objects.filter(default=True)

        return render(request, 'practice/play.html', {
            'practice': practice,
            'duration_in_secs': user_settings.duration_in_secs * 1000,
            'practice_images': practice_images,
            'user_settings': user_settings,
            'ps_cycles': range(user_settings.ps_cycles)
        })

    def post(self, request, *args, **kwargs):
        practice_id = kwargs.get('pk')
        fulfilment = request.POST.get('fulfilment', 3)
        view_name = request.resolver_match.view_name

        if view_name == 'count_play_session':
            request.user.count_spent_seconds(practice_id=practice_id)

        if view_name == 'count_fulfilment':
            request.user.update_fulfilment(practice_id=practice_id, fulfilment=fulfilment)

        return HttpResponse('ok')
