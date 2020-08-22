# -*- coding: utf-8 -*-
import random
import re

from django import template
from django.template.defaultfilters import stringfilter

from iow.apps.core.utils import convert_seconds_to_hours

register = template.Library()


@register.filter
@stringfilter
def append_pagination(path, page):
    if '?' in path:
        if 'page' in path:
            return re.sub(r'page=(\d+)', 'page=%s' % page, path)
        else:
            return '%s&page=%s' % (path, page)
    else:
        return '%s?page=%s' % (path, page)


@register.simple_tag
def define(value=None):
    return value


@register.filter
@stringfilter
def count_list(words):
    words_list = words.split(',')
    return len(words_list)


@register.simple_tag
def randomized_object(objects_list):
    if len(objects_list):
        return random.choice(objects_list)
    return None


@register.filter
def is_already_added(session, user):
    if not user.is_authenticated:
        return False

    user_pack = user.user_packs.last()
    if not user_pack:
        return False

    user_practice_session_ids = list(user_pack.practice_sessions.values_list('id', flat=True))

    if session.id in user_practice_session_ids:
        return True

    return False


@register.filter
def negative(number):
    return number < 0


@register.filter
def convert_seconds(secs):
    return convert_seconds_to_hours(secs=secs)


@register.filter
def subtract(value, arg):
    return value - arg