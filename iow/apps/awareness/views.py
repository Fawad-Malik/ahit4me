from django.shortcuts import render, HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView

from .models import RecommendedPS, Answer, Question, QuestionAnswers, Space, SpaceQuestions, SpaceAnswers, \
    SpaceQuestionAnswers, SpaceRecommendedPS, SpaceTextBoxes, AwarenessTextBoxes, Timeline, UserTimeline
from ..practice.models import PracticeSession
from ..categories.models import Category, SubCategory, SubCatTextBoxes
from ..user.models import UserSettings


class Categories:
    category = ''
    subCategories = []

    def __init__(self, category):
        self.category = category


class Table:
    row = []


def convert_timeline_option(starttime, endtime):
    s = starttime.hour
    e = endtime.hour+1
    return '{"starttime": %d, "endtime": %d}' % (s, e)


class Questions(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        subCategories = SubCategory.objects.all()
        categories = Category.objects.all().order_by('order')
        spaces = Space.objects.all()

        count = 0

        CategoriesList = []
        for category in categories:
            CategoriesList.append(Categories(category.name))
            CategoriesList[count].subCategories = []
            for sub in subCategories:
                if category.name == sub.category.name:
                    CategoriesList[count].subCategories.append(sub.name)
            count = count + 1

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
                    subCategoriesList.append({'sub_cat': y.subCategories[x], 'cat': CategoriesList[index].category})
                else:
                    subCategoriesList.append([])
            tableList[x].row.extend(subCategoriesList)

        try:
            textboxes = AwarenessTextBoxes.objects.filter().order_by('order')
        except AwarenessTextBoxes.DoesNotExist:
            textboxes = []

        try:
            activities = Timeline.objects.filter().order_by('name')
        except Timeline.DoesNotExist:
            activities = []

        try:
            usertimelines = UserTimeline.objects.filter(user=request.user.id).order_by('starttime')
            for usertimeline in usertimelines:
                usertimeline.string_start_time = usertimeline.starttime.strftime("%H:%M")
                usertimeline.string_end_time = usertimeline.endtime.strftime("%H:%M")
                usertimeline.string_start_time_hour = usertimeline.starttime.strftime("%H")
                usertimeline.string_start_time_mints = usertimeline.starttime.strftime("%M")
                usertimeline.string_end_time_hour = usertimeline.endtime.strftime("%H")
                usertimeline.string_end_time_mints = usertimeline.endtime.strftime("%M")
        except UserTimeline.DoesNotExist:
            usertimelines = []

        try:
            tempuserprofile = UserSettings.objects.get(user_id=request.user.id)
            userprofile = {
                "timeline_starttime": tempuserprofile.timeline_starttime,
                "timeline_endtime": tempuserprofile.timeline_endtime,
                "timline_s_starttime": tempuserprofile.timeline_starttime.strftime("%H:%M"),
                "timline_s_endtime": tempuserprofile.timeline_endtime.strftime("%H:%M"),
            }
        except UserSettings.DoesNotExist:
            stime = datetime.strptime('00:00', "%H:%M")
            etime = datetime.strptime('23:59', "%H:%M")
            userprofile = {
                "timeline_starttime": datetime.time(stime),
                "timeline_endtime": datetime.time(etime),
                "timline_s_starttime": '00:00',
                "timline_s_endtime": '23:59',
            }

        timeline_option = convert_timeline_option(userprofile["timeline_starttime"], userprofile["timeline_endtime"])

        return render(request, 'awareness/index.html', {
            'categories': CategoriesList,
            'subCategories': tableList,
            'spaces': spaces,
            'text_boxes': textboxes,
            'activities': activities,
            'usertimelines': usertimelines,
            'userprofile': userprofile,
            'timeline_option': timeline_option,
            'allcategories': categories
        })

    def post(self, request, *args, **kwargs):
        """
        This post will save the answer to the question.
        """
        return HttpResponse('ok')


class DailyTasksView(FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        start_time = kwargs.get('start_time')
        end_time = kwargs.get('end_time')

        stime = datetime.strptime(start_time, "%H:%M").time()
        etime = datetime.strptime(end_time, "%H:%M").time()

        categories = Category.objects.all()
        temptasks = UserTimeline.objects.filter(user=request.user)
        # starttime__gte = stime, endtime__lte = etime

        tasks = []
        for task in temptasks:
            if task.starttime >= stime and task.endtime <= etime:
                tasks.append(task)
            elif task.starttime <= stime <= task.endtime:
                tasks.append(task)
            elif task.starttime <= etime <= task.endtime:
                tasks.append(task)

        return render(request, 'awareness/daily-tasks.html', {
            'categories': categories,
            'tasks': tasks,
            'start_time': stime.strftime("%I:%M %p"),
            'end_time': etime.strftime("%I:%M %p")
        })


class Answers(FormView):

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        answers = Answer.objects.all()
        return render(request, 'awareness/answers.html', {
            'questions': questions,
            'answers': answers
        })


class QuestionAns:
    question = {}
    answers = []
    db_answers = []

    def __init__(self, question, q_id):
        self.question = {'text': question, 'id': q_id}


class QuestionAnsObject:
    question = dict()
    answers = dict()
    db_answers = dict()


class DBAns:
    question = {}
    answers = []

    def __init__(self, question, q_id):
        self.question = {'text': question, 'id': q_id}


@login_required(login_url='/user/login/')
def fetch_answers(request, cat_name, sub_cat_name):
    category = Category.objects.filter(name=cat_name).values_list('id', flat=True)
    subcategory = SubCategory.objects.filter(name=sub_cat_name, category_id__in=category).values_list('id', flat=True)
    # subcategoryimage = SubCategory.objects.filter(name=sub_cat_name, category_id__in=category).values_list('image', flat=True)
    # subcategoryimagetext = SubCategory.objects.filter(name=sub_cat_name, category_id__in=category).values_list('ImageText', flat=True)

    try:
        textboxes = SubCatTextBoxes.objects.filter(subcategory_id__in=subcategory).order_by('order')
    except SubCatTextBoxes.DoesNotExist:
        textboxes = []

    questions = Question.objects.filter(subcategory_id__in=subcategory).values_list('id', flat=True)
    questionstext = Question.objects.filter(subcategory_id__in=subcategory).values_list('text', 'id')
    answers = Answer.objects.filter(question_id__in=questions).values_list('text', 'id', 'question_id')

    db_data = QuestionAnswers.objects.filter(user=request.user)

    db_data_arr = []
    for i, x in enumerate(db_data):
        db_data_arr.append(DBAns(x.question.text, x.question.id))
        db_data_arr[i].answers = []

        all_ans = x.answer.all()

        for ans in all_ans:
            db_data_arr[i].answers.append({'text': ans.text, 'id': ans.id})

    datalist = []
    for i, x in enumerate(questionstext):
        datalist.append(QuestionAns(x[0], x[1]))
        datalist[i].answers = []
        for y, ans in enumerate(answers):
            if questionstext[i][1] == ans[2]:
                ansid = ans[1]
                datalist[i].answers.append({'text': ans[0], 'id': ansid})

    for i, ele in enumerate(datalist):
        datalist[i].db_answers = []
        for j, db_ele in enumerate(db_data_arr):
            if ele.question == db_ele.question:
                datalist[i].db_answers.append(db_ele.answers)

    return render(request, 'awareness/answers.html', {
        'list': datalist,
        'answer_type': 'category',
        'cat_name': cat_name,
        'sub_cat_name': sub_cat_name,
        'text_boxes': textboxes
    })


@login_required(login_url='/user/login/')
def fetch_spaces(request, space_name):
    space = Space.objects.filter(name=space_name).values_list('id', flat=True)
    try:
        spacetextboxes = SpaceTextBoxes.objects.filter(space_id__in=space).order_by('order')
    except SpaceTextBoxes.DoesNotExist:
        spacetextboxes = []

    questions = SpaceQuestions.objects.filter(space_id__in=space).values_list('id', flat=True)
    questionstext = SpaceQuestions.objects.filter(space_id__in=space).values_list('question', 'id')
    answers = SpaceAnswers.objects.filter(question_id__in=questions).values_list('answer', 'id', 'question_id')

    db_data = SpaceQuestionAnswers.objects.filter(user=request.user)

    db_data_arr = []
    for i, x in enumerate(db_data):
        db_data_arr.append(DBAns(x.question.question, x.question.id))
        db_data_arr[i].answers = []

        all_ans = x.answer.all()

        for ans in all_ans:
            db_data_arr[i].answers.append({'text': ans.answer, 'id': ans.id})

    datalist = []
    for i, x in enumerate(questionstext):
        datalist.append(QuestionAns(x[0], x[1]))
        datalist[i].answers = []
        for y, ans in enumerate(answers):
            if questionstext[i][1] == ans[2]:
                ansid = ans[1]
                datalist[i].answers.append({'text': ans[0], 'id': ansid})

    for i, ele in enumerate(datalist):
        datalist[i].db_answers = []
        for j, db_ele in enumerate(db_data_arr):
            if ele.question == db_ele.question:
                datalist[i].db_answers.append(db_ele.answers)
    return render(request, 'awareness/answers.html', {
        'list': datalist,
        'answer_type': 'space',
        'display_image': 'none',
        'cat_name': space_name,
        'text_boxes': spacetextboxes
    })


def saveanswers(request):
    if request.is_ajax() and request.user.is_authenticated:
        user = request.user
        if request.POST['answer_type'] == 'category':
            questionid = request.POST['question']
            question = Question.objects.get(id=questionid)

            answerid = request.POST['answer']
            answer = Answer.objects.get(id=answerid)

            db_data = QuestionAnswers.objects.all()

            checkDb = QuestionAnswers.answer.through.objects.filter(answer_id=answerid)

            length = len(checkDb)
            if length == 0:
                q_exists = False

                for obj in db_data:
                    if question == obj.question:
                        q_exists = True
                        break
                if q_exists:
                    q_a_exists = QuestionAnswers.objects.get(question_id=questionid)
                    q_a_exists.answer.add(answer)
                    q_a_exists.save()
                else:
                    model = QuestionAnswers()
                    model.user = user
                    model.question = question
                    model.save()
                    model.answer.add(answer)
                return HttpResponse('{"status": 200}', status=200)
            else:
                response = '{"status": 201, "answer": "%s", "question_id": "%s"}' % (answer, questionid)
                return HttpResponse(response, status=201)
        else:
            questionid = request.POST['question']
            question = SpaceQuestions.objects.get(id=questionid)

            answerid = request.POST['answer']
            answer = SpaceAnswers.objects.get(id=answerid)

            db_data = SpaceQuestionAnswers.objects.all()

            checkDb = SpaceQuestionAnswers.answer.through.objects.filter(spaceanswers_id=answerid)

            length = len(checkDb)
            if length == 0:
                q_exists = False

                for obj in db_data:
                    if question == obj.question:
                        q_exists = True
                        break
                if q_exists:
                    q_a_exists = SpaceQuestionAnswers.objects.get(question_id=questionid)
                    q_a_exists.answer.add(answer)
                    q_a_exists.save()
                else:
                    model = SpaceQuestionAnswers()
                    model.user = user
                    model.question = question
                    model.save()
                    model.answer.add(answer)
                return HttpResponse('{"status": 200}', status=200)
            else:
                response = '{"status": 201, "answer": "%s", "question_id": "%s"}' % (answer, questionid)
                return HttpResponse(response, status=201)

    return HttpResponse('no ajax', status=401)


class AnswerView(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        answer_id = kwargs.get('answer_id')
        answer_type = kwargs.get('answer_type')
        # ps = list(PracticeSessions.objects.filter(answer_id=answer_id).values_list('practicesessions_id', flat=True))
        if answer_type == 'category':
            try:
                answer = Answer.objects.get(pk=answer_id)
                recommendedps = list(
                    RecommendedPS.objects.filter(answer=answer_id).values_list('practicesessions', flat=True))
                practicesessions = PracticeSession.objects.filter(id__in=recommendedps).order_by('order')
                question = Question.objects.get(pk=answer.question_id)
                category = Category.objects.get(pk=question.category_id)
                subcategory = SubCategory.objects.get(pk=question.subcategory_id)
                return render(request, 'awareness/answer.html', {
                    'practiceSessions': practicesessions,
                    'answer': answer,
                    'category_name': category.name,
                    'subcategory_name': subcategory.name,
                    'answer_type': 'category'
                })
            except Answer.DoesNotExist:
                return render(request, 'awareness/answer.html', {
                    'practiceSessions': [],
                    'answer': {},
                    'category_name': '',
                    'subcategory_name': '',
                    'answer_type': 'category'
                })

        elif answer_type == 'space':
            try:
                answer = SpaceAnswers.objects.get(pk=answer_id)
                recommendedps = list(
                    SpaceRecommendedPS.objects.filter(answer=answer_id).values_list('practicesessions', flat=True))
                practicesessions = PracticeSession.objects.filter(id__in=recommendedps).order_by('order')
                question = SpaceQuestions.objects.get(pk=answer.question_id)
                space = Space.objects.get(pk=question.space_id)
                return render(request, 'awareness/answer.html', {
                    'practiceSessions': practicesessions,
                    'answer': answer,
                    'space_name': space.name,
                    'answer_type': 'space'
                })
            except SpaceAnswers.DoesNotExist:
                return render(request, 'awareness/answer.html', {
                    'practiceSessions': [],
                    'answer': {},
                    'space_name': '',
                    'answer_type': 'space'
                })


def add_new_timeline(request):

    if request.is_ajax() and request.user.is_authenticated:
        start_time = datetime.strptime(request.POST['start_time']+':00', "%H:%M:%S")
        end_time = datetime.strptime(request.POST['end_time']+':00', "%H:%M:%S")
        timeline_id = request.POST['timeline_id']
        category_id = request.POST['category_id']

        timeline = Timeline.objects.get(pk=timeline_id)
        category = Category.objects.get(pk=category_id)

        model = UserTimeline()
        model.starttime = start_time.time()
        model.endtime = end_time.time()
        model.user = request.user
        model.timeline = timeline
        model.category = category
        model.save()
        response = '{"status": 200, "msg": "Successfully added.."}'
        return HttpResponse(response, status=200)

    response = '{"status": 400, "msg": "Not authenticated"}'
    return HttpResponse(response, status=400)


def update_user_activity(request):

    if request.is_ajax() and request.user.is_authenticated:
        start_time = datetime.strptime(request.POST['start_time']+':00', "%H:%M:%S")
        end_time = datetime.strptime(request.POST['end_time']+':00', "%H:%M:%S")
        timeline_id = request.POST['timeline_id']
        category_id = request.POST['category_id']
        activity_id = request.POST['activity_id']

        timeline = Timeline.objects.get(pk=timeline_id)
        category = Category.objects.get(pk=category_id)

        model = UserTimeline.objects.get(pk=activity_id)
        model.starttime = start_time.time()
        model.endtime = end_time.time()
        model.timeline = timeline
        model.category = category
        model.save()
        response = '{"status": 200, "msg": "Successfully added.."}'
        return HttpResponse(response, status=200)

    response = '{"status": 400, "msg": "Not authenticated"}'
    return HttpResponse(response, status=400)


def update_user_timeline(request):

    if request.is_ajax() and request.user.is_authenticated:
        start_time = datetime.strptime(request.POST['start_time']+':00', "%H:%M:%S")
        end_time = datetime.strptime(request.POST['end_time']+':00', "%H:%M:%S")

        model = UserSettings.objects.get(user_id=request.user.id)
        model.timeline_starttime = start_time.time()
        model.timeline_endtime = end_time.time()
        model.save()
        response = '{"status": 200, "msg": "Successfully added.."}'
        return HttpResponse(response, status=200)

    response = '{"status": 400, "msg": "Not authenticated"}'
    return HttpResponse(response, status=400)


def delete_user_activity(request):

    if request.is_ajax() and request.user.is_authenticated:
        activity_id = request.POST['activity_id']

        model = UserTimeline.objects.get(id=activity_id)
        model.delete()
        response = '{"status": 200, "msg": "Successfully deleted.."}'
        return HttpResponse(response, status=200)

    response = '{"status": 400, "msg": "Not authenticated"}'
    return HttpResponse(response, status=400)
