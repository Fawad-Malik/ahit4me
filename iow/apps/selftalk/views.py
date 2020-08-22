from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from ..awareness.models import RecommendedPS, Answer, Question, QuestionAnswers, Space, SpaceQuestions, SpaceAnswers, \
    SpaceQuestionAnswers, SpaceRecommendedPS, SpaceTextBoxes, AwarenessTextBoxes, Timeline, UserTimeline
from ..practice.models import PracticeSession
from .models import SelfTalk, UserST
from django.contrib.auth.models import User
from ..categories.models import Category, SubCategory, SubCatTextBoxes
from ..user.models import UserSettings
from django.http import JsonResponse
import json


class Categories:
    category = ''
    subCategories = []

    def __init__(self, category):
        self.category = category


class subcategories:
    subcategory = ''
    selftalks = []

    def __init__(self, subcategory):
        self.subcategory = subcategory


class Table:
    row = []

# Create your views here.


def convert_timeline_option(starttime, endtime):
    s = starttime.hour
    e = endtime.hour+1
    return '{"starttime": %d, "endtime": %d}' % (s, e)


class Questions(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        subCategories = SubCategory.objects.all()
        selftalks = SelfTalk.objects.all()
        usersts = None
        categories = Category.objects.all().order_by('order')
        spaces = Space.objects.all()
        count = 0

        try:
            selftalk_first = SelfTalk.objects.get(id=1)
        except SelfTalk.DoesNotExist:
            selftalk_first = None

        try:
            userst_first = UserST.objects.get(selftalk=1, userId=1)
        except UserST.DoesNotExist:
            userst_first = None

        CategoriesList = []
        for category in categories:
            CategoriesList.append(Categories(category.name))
            CategoriesList[count].subCategories = []
            for sub in subCategories:
                if category.name == sub.category.name:
                    CategoriesList[count].subCategories.append(sub.name)
            count = count + 1

        count1 = 0

        subCategoriesList1 = []
        for subCategory in subCategories:
            subCategoriesList1.append(subcategories(subCategory.name))
            subCategoriesList1[count1].selftalks = []
            for selftalk in selftalks:
                if subCategory.name == selftalk.subcategory.name:
                    subCategoriesList1[count1].selftalks.append(selftalk)

            count1 = count1 + 1
        # pdb.set_trace()
        tableList = []
        subCategoriesList = []
        length = 0
        for item in CategoriesList:
            subCategoriesLength = len(item.subCategories)
            if subCategoriesLength > length:
                length = subCategoriesLength

        for x in range(length):
            tableList.append(Table())
            subCategoriesList = []
            tableList[x].row = []
            for index, y in enumerate(CategoriesList):
                if x < len(y.subCategories):
                    subCategoriesList.append(
                        {'sub_cat': y.subCategories[x], 'cat': CategoriesList[index].category})
                else:
                    subCategoriesList.append([])
            tableList[x].row.extend(subCategoriesList)
        return render(request, 'selftalk/detail.html', {
            'categories': CategoriesList,
            'subCategories': tableList,
            'selftalks': selftalks,
            'usersts': usersts,
            'selftalk_first': selftalk_first,
            'userst_first': userst_first,
            'spaces': spaces,
            'allcategories': categories,
            'subCategoriesList1': subCategoriesList1
        })

    def post(self, request, *args, **kwargs):
        """
        This post will save the answer to the question.
        """
        return HttpResponse('ok')


@login_required(login_url='/user/login/')
def add_fundamentals(request):
    if request.is_ajax():
        print('inside add_fundamentals')
        userid = request.user.id
        print(userid)
        selftalk = request.POST.get('selftalk_id')
        before = request.POST.get('before')
        during = request.POST.get('during')
        after = request.POST.get('after')
        who_am_i_talking_to = request.POST.get('who_am_i_talking')
        is_now_a_good_time_to_talk = request.POST.get('is_now_a_good_time')
        times_a_day = request.POST.get('times_a_day')
        times_it_last = request.POST.get('times_it_last')
        how_intense = request.POST.get('how_intense')
        polarity = request.POST.get('polarity')
        function = request.POST.get('function')
        emotion = request.POST.get('emotion')
        try:
            selftalk = SelfTalk.objects.get(id=selftalk)
        except SelfTalk.DoesNotExist:
            selftalk = None
        try:
            fundamental_check = UserST.objects.get(
                userId=userid, selftalk=selftalk)
        except UserST.DoesNotExist:
            fundamental_check = None
        if fundamental_check:
            try:
                fundamental = UserST.objects.filter(userId=userid, selftalk=selftalk).update(selftalk=selftalk, before=before, during=during, after=after, who_am_i_talking_to=who_am_i_talking_to,
                                                                                             is_now_a_good_time_to_talk=is_now_a_good_time_to_talk, times_a_day=times_a_day, times_it_last=times_it_last, how_intense=how_intense, polarity=polarity, function=function, emotion=emotion)
            except UserST.DoesNotExist:
                fundamental = None
        else:
            try:
                fundamental = UserST.objects.create(userId=userid, selftalk=selftalk, before=before, during=during, after=after, who_am_i_talking_to=who_am_i_talking_to,
                                                    is_now_a_good_time_to_talk=is_now_a_good_time_to_talk, times_a_day=times_a_day, times_it_last=times_it_last, how_intense=how_intense, polarity=polarity, function=function, emotion=emotion)
            except UserST.DoesNotExist:
                fundamental = None

    return JsonResponse({'status': True})


@login_required(login_url='/user/login/')
def get_fundamentals(request):
    if request.is_ajax():
        print('inside get_fundamentals')
        userid = request.user.id
        selftalk_value = request.GET.get('selftalk_id')
        try:
            selftalk = SelfTalk.objects.get(id=selftalk_value)
        except SelfTalk.DoesNotExist:
            selftalk = None
        try:
            fundamental = UserST.objects.get(
                userId=userid, selftalk=selftalk_value)
        except UserST.DoesNotExist:
            fundamental = None
        if fundamental:
            print("record found")
            data = json.dumps({
                'id': fundamental.id,
                'before': fundamental.before,
                'during': fundamental.during,
                'after': fundamental.after,
                'who_am_i_talking_to': fundamental.who_am_i_talking_to,
                'is_now_a_good_time_to_talk': fundamental.is_now_a_good_time_to_talk,
                'times_a_day': fundamental.times_a_day,
                'times_it_last': fundamental.times_it_last,
                'how_intense': fundamental.how_intense,
                'polarity': fundamental.polarity,
                'function': fundamental.function,
                'emotion': fundamental.emotion,
            })
        elif not fundamental:
            data = json.dumps({
                'id': '',
                'before': '',
                'during': '',
                'after': '',
                'who_am_i_talking_to': '',
                'is_now_a_good_time_to_talk': '',
                'times_a_day': '',
                'times_it_last': '',
                'how_intense': '',
                'polarity': '',
                'function': '',
                'emotion': '',
            })

    return HttpResponse(data, content_type='application/json')
