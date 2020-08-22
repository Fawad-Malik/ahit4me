def page_detector(request):

    landing_pages = [
        'landing_index', 'landing_login', 'landing_discover', 'landing_help', 'landing_about', 'landing_contact'
    ]

    request_view_name = request.resolver_match.view_name

    if request_view_name in landing_pages:
        return {
            'landing': True
        }

    return {
        'landing': False
    }


def user_extra(request):
    extra_variables = {
        'last_subscription': None,
        'profile': None
    }

    if not request.user.is_authenticated:
        return extra_variables

    extra_variables['last_subscription'] = request.user.user_subscriptions.last()
    extra_variables['profile'] = request.user.profile

    return extra_variables

