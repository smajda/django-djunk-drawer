"""
Dealing with timezone-aware datetimes sucks.

Django's docs on its timezone code is here:

https://docs.djangoproject.com/en/dev/topics/i18n/timezones/

Here are some convenience functions to do common date-related things.

Standard disclaimer: work in progress. I'm not sure these are all
that great as-is so far.

Something like Arrow may be a better foundation:

https://github.com/crsmithdev/arrow

"""
import time

from django.utils import timezone
from datetime import time, timedelta
from dateutil.relativedelta import relativedelta


DATE_FORMAT = '%m/%d/%Y'
DATETIME_FORMAT = "{0} %H:%M".format(DATE_FORMAT)
DATETIME_FILE_FORMAT = '%Y%m%d_%H%M'


def local_now():
    return timezone.now().astimezone(timezone.get_current_timezone())


def get_midnight_for_date(dt):
    """
    Timezone and DST-safe way to get midnight from a current date

    i.e. "Nov 4 00:00:00 CDT" will become "Nov 4 23:59:59 CST"
    """
    tz = dt.tzinfo
    naive_date = timezone.datetime.combine(dt.date(), time.max)
    return timezone.make_aware(naive_date, tz)


def get_yesterday_midnight():
    now = local_now()
    naive_now_date = timezone.make_naive(now, now.tzinfo).date()
    return timezone.make_aware(
        timezone.datetime.combine(naive_now_date, time.max) - timedelta(days=1),
        now.tzinfo)


def get_tonight_midnight():
    now = local_now()
    naive_midnight = timezone.datetime.combine(timezone.make_naive(now, now.tzinfo).date(), time.max)
    return timezone.make_aware(naive_midnight, now.tzinfo)


def get_year_start():
    now = local_now()
    return timezone.make_aware(
               timezone.datetime(year=now.year, month=1, day=1),
               timezone.get_current_timezone())


def get_month_start():
    now = local_now()
    return timezone.make_aware(
               timezone.datetime(year=now.year, month=now.month, day=1),
               timezone.get_current_timezone())


def format_local_datetime(dt, df=DATETIME_FORMAT):
    "Helper function to simplify converting a datetime to local tz and formatting"
    return dt.astimezone(timezone.get_current_timezone()).strftime(df)


def format_local_date(dt, df=DATE_FORMAT):
    if hasattr(dt, 'astimezone'):
        dt = dt.astimezone(timezone.get_current_timezone())
    return dt.strftime(df)

def datetime_to_timestamp(dt):
    "Convert tz-aware datetime to utc timestamp"
    return int(time.mktime(dt.astimezone(timezone.utc).timetuple()))


def timestamp_to_datetime(timestamp, tz=timezone.get_current_timezone()):
    "Convert utc timestamp to datetime in tz (default django current tz)"
    return timezone.make_aware(
               timezone.datetime.utcfromtimestamp(tz),
               timezone.get_default_timezone())
