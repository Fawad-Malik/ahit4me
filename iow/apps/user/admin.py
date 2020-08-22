from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Subscription, Profile, UserSettings


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'mode', 'cancelled')
    list_display_links = None


# unregister user for now
admin.site.unregister(Group)
# admin.site.register(Profile)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    pass
