from django.shortcuts import HttpResponse, render, redirect, reverse
from django.views.generic import FormView

from iow.apps.practice.models import Category
from iow.apps.knowledge.models import Help
from .forms import ContactForm
from .utils import send_html_mail
from iow.apps.text.models import LandingPage, DiscoverPage


def letsencrypt1(request):
    return HttpResponse(
        'jFQjgHBNunoNCnn4953rtTi8fD08qsuqd_aWwOJ_lzY.Rcz4GO0RowCnc8vJIFndcvLvBAeyxtvb4YW18BFeaPY',
        content_type='text/plain'
    )


def letsencrypt2(request):
    return HttpResponse(
        'KN5bCYaSt3Dqq_TypDjGNgWiVkk4A4l-Ssf9Q-TUOdI.N0h6QnEjZ5muHZZz2tbxin6FZD4mX6_vIquD2ExMg6g',
        content_type='text/plain'
    )


def index(request):
    page_text = LandingPage.objects.last()
    return render(request, 'index.html', {
        'page_text': page_text
    })


def landing_discover(request):

    all_categories = Category.objects.order_by('order')

    for cat in all_categories:
        cat.dreams = DiscoverPage.objects.filter(category_id=cat.id).order_by('order')

    return render(request, 'explore.html', {
        'all_categories': all_categories,
        # 'page_text': page_text
    })


def help_(request):
    return render(request, 'help.html', {
        'helps': Help.objects.all()
    })


class ContactView(FormView):

    def get(self, request, *args, **kwargs):
        form = ContactForm()

        # put user's email if user is logged in
        if request.user.is_authenticated:
            form.initial.update({
                'email': request.user.email
            })

        return render(request, 'contact.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')

            text = "<p>Someone contacted us. The message:</p><p>Name: %s</p><p>Email: %s</p><p>Message: %s</p>" % (
                name, email, message
            )

            send_html_mail(
                'Someone contacted us',
                ['doniyor.v.j@gmail.com', 'mark@millerteamre.com', ],
                **{
                    'text': text
                }
            )

            return redirect('%s?sent=1' % reverse('landing_contact'))

        return render(request, 'contact.html', {
            'form': form,
            'error': 'Something went wrong. Please try again.'
        })

























