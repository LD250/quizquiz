from django.conf import settings


def site_settings(request):
    """
    Returns a lazy 'messages' context variable.
    """
    return {
        'site_url': settings.SITE_URL
    }