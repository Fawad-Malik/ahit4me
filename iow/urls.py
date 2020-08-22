from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from iow.apps.core.views import (
    index, letsencrypt1, letsencrypt2, landing_discover, help_, ContactView
)


urlpatterns = [

    path('', index, name='landing_index'),
    path('landing/explore/', landing_discover, name='landing_discover'),
    path('landing/about/', TemplateView.as_view(template_name='about.html'), name='landing_about'),
    path('landing/contact/', ContactView.as_view(), name='landing_contact'),
    path('landing/help/', help_, name='landing_help'),
    path('pricing/', TemplateView.as_view(template_name='plans.html'), name='pricing'),

    path('under_construction/', TemplateView.as_view(template_name='under_construction.html'), name='under_construction'),

    path('.well-known/acme-challenge/jFQjgHBNunoNCnn4953rtTi8fD08qsuqd_aWwOJ_lzY', letsencrypt1),
    path('.well-known/acme-challenge/KN5bCYaSt3Dqq_TypDjGNgWiVkk4A4l-Ssf9Q-TUOdI', letsencrypt2),

    path('user/', include('iow.apps.user.urls')),
    path('practice/', include('iow.apps.practice.urls')),
    path('knowledge/', include('iow.apps.knowledge.urls')),
    path('awareness/', include('iow.apps.awareness.urls')),
    # path('categories/', include('iow.apps.categories.urls')),
    path('causeandeffects/', include('iow.apps.causeandeffects.urls')),
    path('causalforces/', include('iow.apps.causalforces.urls')),
    path('selftalk/', include('iow.apps.selftalk.urls')),
    path('admin/', admin.site.urls),

    # info pages
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms_and_conditions/', TemplateView.as_view(template_name='terms_and_conditions.html'), name='terms'),
    path('cookie_policy/', TemplateView.as_view(template_name='cookie_policy.html'), name='cookie_policy'),

    path('accounts/', include('allauth.urls')),

    path("stripe/", include("djstripe.urls", namespace="djstripe")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
