from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Knowledge, KnowledgeContent, Help


class KnowledgeContentInline(admin.TabularInline):
    model = KnowledgeContent
    extra = 0


@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    inlines = [KnowledgeContentInline]
    fieldsets = [
        (None, {'fields': (
            'category',
            'subcategory',
            'title'
        )})
    ]
    list_display = ('title', 'number_of_content', 'user')

    def number_of_content(self, obj):
        return mark_safe('<a href="/admin/knowledge/knowledgecontent/?knowledge=%s">%s Contents</a>' % (
            obj.id, obj.knowledge_contents.count()
        ))

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        return super(KnowledgeAdmin, self).save_model(request, obj, form, change)


@admin.register(KnowledgeContent)
class KnowledgeContentAdmin(admin.ModelAdmin):
    list_filter = ('knowledge',)
    list_display = ('id', 'knowledge')


@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    pass

