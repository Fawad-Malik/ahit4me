from django.contrib import admin

from .models import (
    Question, Answer, RecommendedPS, Space, SpaceQuestions, SpaceAnswers, QuestionAnswers, SpaceQuestionAnswers, SpaceRecommendedPS, SpaceTextBoxes, AwarenessTextBoxes, Timeline, UserTimeline
)


class RecommendedPSInline(admin.TabularInline):
    model = RecommendedPS
    filter_horizontal = ('practicesessions',)
    extra = 1
    max_num = 1


class SpaceRecommendedPSInline(admin.TabularInline):
    model = SpaceRecommendedPS
    filter_horizontal = ('practicesessions',)
    extra = 1
    max_num = 1


class SpaceTextBoxesTextInline(admin.TabularInline):
    model = SpaceTextBoxes

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 4


@admin.register(AwarenessTextBoxes)
class AwarenessTextBoxesAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_filter = ('category', 'subcategory')
    list_display = (
        'question_text', 'category', 'subcategory'
    )

    def question_text(self, obj):
        return obj.text
    question_text.short_description = 'Question'
    question_text.admin_order_field = 'text'


# @admin.register(QuestionAnswers)
# class UserQuestionAdmin(admin.ModelAdmin):
#     filter_horizontal = ('answer',)
#
#
# @admin.register(SpaceQuestionAnswers)
# class UserQuestionAdmin(admin.ModelAdmin):
#     filter_horizontal = ('answer',)


# @admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question', 'text']}),
        ('Video information', {'fields': ['videoLink']}),
        ('Optimal Thought Conversation', {'fields': ['OTCText', 'OTCThinkPerDay', 'OTCThinkEachTime', 'OTCIntensity']}),
        ('Improved Thought Conversation', {'fields': ['ITCText', 'ITCThinkPerDay', 'ITCThinkEachTime', 'ITCIntensity']}),
        ('Negative Thought Conversation', {'fields': ['NTCText', 'NTCThinkPerDay', 'NTCThinkEachTime', 'NTCIntensity']})
    ]

    inlines = [RecommendedPSInline]


admin.site.register(Answer, AnswerAdmin)

    
# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         num_objects = self.model.objects.count()
#         if num_objects >= 1:
#             return False
#         else:
#             return True
#     pass
#
#
# @admin.register(Text)
# class TextAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         num_objects = self.model.objects.count()
#         if num_objects >= 1:
#             return False
#         else:
#             return True
#     pass


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    inlines = [SpaceTextBoxesTextInline]


@admin.register(SpaceQuestions)
class SpaceQuestionsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_filter = ('space', )
    list_display = (
        'question_text', 'space'
    )

    def question_text(self, obj):
        return obj.question

    question_text.short_description = 'Question'
    question_text.admin_order_field = 'question'


@admin.register(SpaceAnswers)
class SpaceAnswersAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question', 'answer']}),
        ('Video information', {'fields': ['videoLink']}),
        ('Optimal Thought Conversation', {'fields': ['OTCText', 'OTCThinkPerDay', 'OTCThinkEachTime', 'OTCIntensity']}),
        ('Improved Thought Conversation', {'fields': ['ITCText', 'ITCThinkPerDay', 'ITCThinkEachTime', 'ITCIntensity']}),
        ('Negative Thought Conversation', {'fields': ['NTCText', 'NTCThinkPerDay', 'NTCThinkEachTime', 'NTCIntensity']})
    ]

    inlines = [SpaceRecommendedPSInline]


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'detailedKnowledgePage', 'fundamentalKnowledgePage'
    )
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Fundamental Knowledge', {'fields': ['fundamentalKnowledge', 'fundamentalKnowledgePage']}),
        ('Detailed Knowledge', {'fields': ['detailedKnowledge', 'detailedKnowledgePage']}),
    ]


# @admin.register(UserTimeline)
# class TimelineAdmin(admin.ModelAdmin):
#     list_display = (
#         'user', 'timeline', 'starttime', 'endtime'
#     )
