from django.shortcuts import render

from iow.apps.knowledge.models import Knowledge
from iow.apps.text.models import KnowledgePage


def index(request):
    knowledges = Knowledge.objects.all()
    return render(request, 'knowledge/index.html', {
        'knowledges': knowledges,
        'page_text': KnowledgePage.objects.last()
    })


def detail(request, slug, pk):
    knowledge = Knowledge.objects.get(id=pk)
    return render(request, 'knowledge/detail.html', {
        'knowledge': knowledge
    })
