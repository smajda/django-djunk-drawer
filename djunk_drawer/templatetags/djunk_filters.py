from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter('message_alert_class')
def message_alert_class(value):
    """
    Maps Django messages tags to Bootstrap alert classes

    Bootstrap alerts:
    '' = yellow
    'alert-error' = red
    'alert-success' = green
    'alert-info' = blue

    Django messages tags: debug, info, success, warning, error

    """
    bootstrap_alerts = {
        'info': 'alert-info',
        'success': 'alert-success',
        'error': 'alert-error'
    }
    return bootstrap_alerts.get(value, '')


@register.filter('linked_list')
def linked_list(objects, url_name):
    """
    Take a list of objects and return link to
    DetailView's based on pk and url_name passed
    in to filter. i.e.:

        {{ my_objects|linked_list:"my_objects_detail" }}
    """
    links = []
    for obj in objects:
        url = reverse(url_name, args=[obj.pk])
        links.append("<a href='{0}'>{1}</a>".format(
                        url, unicode(obj)))
    return mark_safe(", ".join(links))


@register.filter('default_base')
def default_base(url, url_base):
    """
    Sometimes urls are absolute paths (to s3), but sometimes
    they're relative paths ("/img/foo.png").

    But sometimes we *always* need absolute paths (i.e. emails)
    so this will add the url_base passed in if the url
    looks like a relative path.
    """
    if url.startswith('http'):
        return url
    return "{0}{1}".format(url_base, url)


@register.filter(name="startswith")
def startswith(path, initial):
    return path.startswith(initial)


@register.filter(name="active_url_class")
def active_url_class(request, url_name):
    """
    Adds .active to class if current url starts with the same base
    as reversed url_name.

    Useful for cases where you have a nav element ("Tasks") and you
    want .active on it for /tasks/ as well as /tasks/<id>,
    /tasks/create/', and so on. i.e.:

        <div class="{{ request|active_url_class:"tasks_index">Tasks</div>
    """
    try:
        url = reverse(url_name)
    except NoReverseMatch:
        return ""
    return " active" if request.path.startswith(url) else ""
