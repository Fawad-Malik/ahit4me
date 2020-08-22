from django.db import models
from django.contrib.auth.models import User

from iow.apps.core.models import Base
from ..categories.models import (
    Category, SubCategory
)

from ..practice.models import PracticeSession
from ..knowledge.models import Knowledge


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class Question(Base):
    category = models.ForeignKey(
        Category, related_name='category_awareness', on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(
        SubCategory, related_name='subcategory_awareness', on_delete=models.CASCADE, null=True
    )
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '1. 3 As of Life: Question'
        verbose_name_plural = '1. 3 As of Life: Questions'


class Answer(Base):
    # affirmations = models.ForeignKey(Affirmation, related_name='awareness_answers', on_delete=models.DO_NOTHING, null=True)
    question = models.ForeignKey(
        Question, related_name='question_answers', on_delete=models.DO_NOTHING)
    text = models.TextField()
    videoLink = models.CharField(
        max_length=500, default="", verbose_name="Video Link")
    OTCText = models.TextField(default="", verbose_name="Text")
    OTCThinkPerDay = models.IntegerField(
        default=0, verbose_name="How often think it/day")
    OTCThinkEachTime = models.IntegerField(
        default=0, verbose_name="How long think it each time")
    OTCIntensity = models.CharField(
        max_length=25, default="", verbose_name="Intensity")
    ITCText = models.TextField(default="", verbose_name="Text")
    ITCThinkPerDay = models.IntegerField(
        default=0, verbose_name="How often think it/day")
    ITCThinkEachTime = models.IntegerField(
        default=0, verbose_name="How long think it each time")
    ITCIntensity = models.CharField(
        max_length=25, default="", verbose_name="Intensity")
    NTCText = models.TextField(default="", verbose_name="Text")
    NTCThinkPerDay = models.IntegerField(
        default=0, verbose_name="How often think it/day")
    NTCThinkEachTime = models.IntegerField(
        default=0, verbose_name="How long think it each time")
    NTCIntensity = models.CharField(
        max_length=25, default="", verbose_name="Intensity")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '2. 3 As of Life: Answer'
        verbose_name_plural = '2. 3 As of Life: Answers'


class RecommendedPS(Base):
    answer = models.ForeignKey(
        Answer, related_name='answer_contents', on_delete=models.CASCADE,  null=True)
    practicesessions = models.ManyToManyField(
        PracticeSession, related_name='awareness_ps_recommended')

    class Meta:
        verbose_name = 'Recommended Practice Session'
        verbose_name_plural = 'Recommended Practice Sessions'

    def __str__(self):
        return '%s' % self.id


# class Text(Base):
#     text = models.TextField()
#
#     class Meta:
#         verbose_name_plural = 'Awareness Cover Text'
#
#     def __str__(self):
#         return self.text
#
#
# class Image(Base):
#     image = models.ImageField(upload_to='images/%Y/%m/%d')
#
#     class Meta:
#         verbose_name_plural = 'Awareness Cover Image'
#
#     def __str__(self):
#         return 'cover_image'

class AwarenessTextBoxes(Base):
    text = models.CharField(max_length=100)
    order = models.IntegerField(default=1)

    def __str__(self):
        return '%s ' % self.text

    class Meta:
        verbose_name_plural = '3. Awareness Text Boxes'
        verbose_name = '3. Awareness Text Box'


class QuestionAnswers(Base):
    user = models.ForeignKey(
        User, related_name='user_id', on_delete=models.CASCADE)
    # userAnswers = models.TextField(default='', verbose_name="User Answers")
    question = models.ForeignKey(
        Question, related_name='question_id', on_delete=models.CASCADE, null=True)
    answer = models.ManyToManyField(Answer, related_name='user_answers')

    class Meta:
        verbose_name_plural = 'User Answers'
        verbose_name = 'User Answer'

    def __str__(self):
        return '%s' % self.id


class Space(Base):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=1)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        verbose_name_plural = '3. Spaces'
        verbose_name = '3. Space'


class SpaceTextBoxes(Base):
    space = models.ForeignKey(
        Space, related_name='space_text_boxes', on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=100)
    order = models.IntegerField(default=1)

    def __str__(self):
        return '%s ' % self.text

    class Meta:
        verbose_name_plural = 'Text Boxes'
        verbose_name = 'Text Box'


class SpaceQuestions(Base):
    space = models.ForeignKey(
        Space, related_name='space_questions', on_delete=models.CASCADE)
    question = models.CharField(
        max_length=500, default="", verbose_name="Question")

    class Meta:
        verbose_name_plural = '4. Space: Questions'
        verbose_name = '4. Space: Question'

    def __str__(self):
        return self.question


class SpaceAnswers(Base):
    question = models.ForeignKey(
        SpaceQuestions, related_name='space_question_answers', on_delete=models.CASCADE)
    answer = models.CharField(
        max_length=500, default="", verbose_name="Answer")
    videoLink = models.CharField(
        max_length=500, default="", verbose_name="Video Link")
    OTCText = models.TextField(default="", verbose_name="Text")
    OTCThinkPerDay = models.IntegerField(
        default=0, verbose_name="How often think it/day")
    OTCThinkEachTime = models.IntegerField(
        default=0, verbose_name="How long think it each time")
    OTCIntensity = models.CharField(
        max_length=25, default="", verbose_name="Intensity")
    ITCText = models.TextField(default="", verbose_name="Text")
    ITCThinkPerDay = models.IntegerField(
        default=0, verbose_name="How often think it/day")
    ITCThinkEachTime = models.IntegerField(
        default=0, verbose_name="How long think it each time")
    ITCIntensity = models.CharField(
        max_length=25, default="", verbose_name="Intensity")
    NTCText = models.TextField(default="", verbose_name="Text")
    NTCThinkPerDay = models.IntegerField(
        default=0, verbose_name="How often think it/day")
    NTCThinkEachTime = models.IntegerField(
        default=0, verbose_name="How long think it each time")
    NTCIntensity = models.CharField(
        max_length=25, default="", verbose_name="Intensity")

    class Meta:
        verbose_name_plural = '5. Space: Answers'
        verbose_name = '5. Space: Answer'

    def __str__(self):
        return self.answer


class SpaceRecommendedPS(Base):
    answer = models.ForeignKey(
        SpaceAnswers, related_name='space_answer_contents', on_delete=models.CASCADE,  null=True)
    practicesessions = models.ManyToManyField(
        PracticeSession, related_name='space_awareness_ps_recommended')

    class Meta:
        verbose_name = 'Recommended Practice Session'
        verbose_name_plural = 'Recommended Practice Sessions'

    def __str__(self):
        return '%s' % self.id


class SpaceQuestionAnswers(Base):
    user = models.ForeignKey(
        User, related_name='space_user_id', on_delete=models.DO_NOTHING)
    question = models.ForeignKey(
        SpaceQuestions, related_name='space_question_id', on_delete=models.DO_NOTHING, null=True)
    answer = models.ManyToManyField(
        SpaceAnswers, related_name='space_user_answers')

    class Meta:
        verbose_name_plural = 'Space: User Answers'
        verbose_name = 'Space: User Answer'

    def __str__(self):
        return '%s' % self.id


class Timeline(Base):
    name = models.CharField(max_length=100, verbose_name="Name")
    fundamentalKnowledge = models.TextField(
        verbose_name="Fundamental Knowledge", default="")
    fundamentalKnowledgePage = models.ForeignKey(
        Knowledge, verbose_name="Fundamental Knowledge Page", related_name='fundamental_knowledge', on_delete=models.DO_NOTHING, null=True)
    detailedKnowledge = models.TextField(
        verbose_name="Detailed Knowledge", default="")
    detailedKnowledgePage = models.ForeignKey(
        Knowledge, verbose_name="Detailed Knowledge Page", related_name='detailed_knowledge', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        verbose_name_plural = '6. Timelines'
        verbose_name = '6. Timeline'

    def __str__(self):
        return '%s' % self.name


class UserTimeline(Base):
    user = models.ForeignKey(User, related_name='timeline_user_id',
                             on_delete=models.DO_NOTHING, verbose_name="User")
    starttime = models.TimeField(
        auto_now=False, auto_now_add=False, verbose_name="Start Time")
    endtime = models.TimeField(
        auto_now=False, auto_now_add=False, verbose_name="End Time")
    timeline = models.ForeignKey(Timeline, verbose_name="Timeline Name",
                                 related_name="user_timeline_fk", on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, verbose_name="Category Name",
                                 related_name="user_timeline_category_fk", on_delete=models.DO_NOTHING, null=True)

    class Meta:
        verbose_name_plural = 'User Timelines'
        verbose_name = 'User Timeline'

    def __str__(self):
        return '%s' % self.user.username
