from django.contrib import admin
from .models import SelfTalk


@admin.register(SelfTalk)
class SelfTalkAdmin(admin.ModelAdmin):
    list_filter = ('category', 'subcategory')
    list_display = (
        'name', 'category', 'subcategory'
    )
    ordering = ('order',)

    fieldsets = [
        (None, {'fields': ['name', 'category', 'subcategory', 'order']}),
        ('Fundamentals', {
            'fields': ['polarity_self_talk', 'function_self_talk', 'emotion_self_talk']}),
        ('Low Level', {
            'fields': ['low_low', 'low_high', 'low_medium']}),
        ('High Level', {
            'fields': ['high_low', 'high_high', 'high_medium']}),
        ('Medium Level', {
            'fields': ['medium_low', 'medium_high', 'medium_medium']}),
    ]
