from django.contrib import admin

from .models import LandingPage, DiscoverPage, DashboardPage, KnowledgePage

admin.site.register(LandingPage)
admin.site.register(DashboardPage)
admin.site.register(KnowledgePage)


@admin.register(DiscoverPage)
class DiscoverPageAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('dream', 'category')
