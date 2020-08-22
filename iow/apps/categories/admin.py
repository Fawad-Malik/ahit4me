from django.contrib import admin

from .models import (
   Category, SubCategory, SubCatTextBoxes
)


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0


class SubCatTextBoxesTextInline(admin.TabularInline):
    model = SubCatTextBoxes

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = (
        '__str__', 'number_of_subcats'
    )
    ordering = ('order',)

    def number_of_subcats(self, obj):
        return obj.category_subcats.count()
    


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'category'
    )
    list_filter = ('category',)
    inlines = [SubCatTextBoxesTextInline]

