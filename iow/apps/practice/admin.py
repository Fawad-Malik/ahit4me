from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from .models import (
    Affirmation, AffirmationText,  Image, PracticeSession, Pack
)

# class SubCategoryInline(admin.TabularInline):
#     model = SubCategory
#     extra = 0


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     inlines = [SubCategoryInline]
#     list_display = (
#         '__str__', 'number_of_subcats'
#     )
#     ordering = ('order',)

#     def number_of_subcats(self, obj):
#         return obj.category_subcats.count()


# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = (
#         'category', '__str__', 'number_of_affirmation_bundles'
#     )
#     list_filter = ('category',)

#     def number_of_affirmation_bundles(self, obj):
#         return obj.subcategory_affirmations.count()


class AffirmationTextInline(admin.TabularInline):
    model = AffirmationText

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 4


@admin.register(Affirmation)
class AffirmationAdmin(admin.ModelAdmin):
    inlines = [AffirmationTextInline]
    fieldsets = [
        (None, {'fields': (
            'order',
            'category',
            'subcategory',
            'title'
        )})
    ]
    change_form_template = 'admin/practice/affirmations/change_form.html'
    list_filter = ('category', 'subcategory')
    list_display = (
        'title', 'number_of_affirmations', 'category', 'subcategory', 'order'
    )
    ordering = ('order',)

    def number_of_affirmations(self, obj):
        return obj.affirmation_texts.count()

    def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
        return super(AffirmationAdmin, self).get_inline_formsets(request, formsets, inline_instances, obj)


@admin.register(PracticeSession)
class PracticeSessionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        '__str__', 'affirmation_category', 'affirmation_subcategory', 'affirmation_texts',
    )
    list_filter = ('affirmation__category', 'affirmation__subcategory')
    fieldsets = [
        (None, {'fields': (
            'name', 'purpose', 'affirmation', 'music_file'
        )})
    ]

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        return super(PracticeSessionAdmin, self).save_model(request, obj, form, change)

    def affirmation_category(self, obj):
        return obj.affirmation.category.name
    affirmation_category.short_description = 'Category'

    def affirmation_subcategory(self, obj):
        return obj.affirmation.subcategory.name
    affirmation_subcategory.short_description = 'Subcategory'

    def affirmation_texts(self, obj):
        if obj.affirmation.affirmation_texts.count():
            return '%s ...' % obj.affirmation.affirmation_texts.first().text[:30]
    affirmation_texts.short_description = 'Affirmation Texts'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    exclude = ('practice_session',)


# @admin.register(Pack)
# class PackAdmin(admin.ModelAdmin):
#     pass

