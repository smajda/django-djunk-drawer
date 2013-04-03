import hashlib

from django.core.cache import cache
from django.utils.http import urlquote

def invalidate_template_cache(fragment_name, *args):
    """
    Invalidate template cache for fragment_name with args

    i.e you have this:

        {% cache 600 user_links user.pk %}

    In a view or a save method or a receiver, say, do this:

        invalidate_template_cache('user_links', user.pk)

    The method for generating the cache key is taken directly from
    django.templatetags.cache.CacheNode's render method. If this
    ever breaks, look there for changes.
    """
    hash = hashlib.md5(u':'.join([urlquote(x) for x in args]))
    cache_key = 'template.cache.{0}.{1}'.format(fragment_name, hash.hexdigest())
    cache.delete(cache_key)
    return cache_key
