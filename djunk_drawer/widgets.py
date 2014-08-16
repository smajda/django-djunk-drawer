import floppyforms as forms

from dateutil.parser import parse

from django.template import Context, loader
from django.utils import timezone


class USPhoneNumberMultiWidget(forms.MultiWidget):
    """
    A Widget that splits US Phone number input into three <input type='text'> boxes.

    Source: http://stackoverflow.com/a/1912686
    """
    def __init__(self, attrs=None, *args, **kwargs):
        widgets = (
            forms.widgets.TextInput(attrs={'pattern': '[0-9]*', 'size': '3', 'maxlength': '3', 'class': 'phone', 'placeholder': 'xxx'}),
            forms.widgets.TextInput(attrs={'pattern': '[0-9]*', 'size': '3', 'maxlength': '3', 'class': 'phone', 'placeholder': 'xxx'}),
            forms.widgets.TextInput(attrs={'pattern': '[0-9]*', 'size': '4', 'maxlength': '4', 'class': 'phone', 'placeholder': 'xxxx'}),
        )
        super(USPhoneNumberMultiWidget, self).__init__(widgets, attrs)

    def render(self, *args, **kwargs):
        required = self.is_required
        for widget in self.widgets:
            widget.is_required = required
        return super(USPhoneNumberMultiWidget, self).render(*args, **kwargs)

    def decompress(self, value):
        if value:
            return value.split('-')
        return (None, None, None)

    def value_from_datadict(self, data, name, files=None):
        value = [u'', u'', u'']
        # look for keys like name_1, get the index from the end
        # and make a new list for the string replacement values
        for d in filter(lambda x: x.startswith(name), data):
            index = int(d[len(name) + 1:])
            value[index] = data[d]
        if value[0] == value[1] == value[2] == u'':
            return None
        return u'%s-%s-%s' % tuple(value)


class DateRangeWidget(forms.MultiWidget):
    """
    A widget that gives two date fields and returns a tuple of two datetime fields.

    Use with ListFormField (below):

        my_date_range = ListFormField(widget=DateRangeWidget(), required=False)

    Useful for forms that need date range searches.
    """
    def __init__(self, attrs={}, *args, **kwargs):
        # Note that forms.DateInput from floppyforms works, but Chrome
        # started adding it's own datepicker widget, which conflicts
        # with ours. Yay.
        widgets = (
            forms.TextInput(attrs=attrs.update({'class': 'datepicker date_range date_range_start'})),
            forms.TextInput(attrs=attrs.update({'class': 'datepicker date_range date_range_end'})),
        )
        super(DateRangeWidget, self).__init__(widgets, attrs)

    def render(self, *args, **kwargs):
        return super(DateRangeWidget, self).render(*args, **kwargs)

    def decompress(self, value):
        if value is None:
            return (None, None)
        values = []
        values.append(value[0].strftime('%m/%d/%Y')
                      if isinstance(value[0], timezone.datetime) else None)
        values.append(value[1].strftime('%m/%d/%Y')
                      if isinstance(value[1], timezone.datetime) else None)
        return tuple(values)

    def value_from_datadict(self, data={}, files=None, name=None):
        from_date = None
        to_date = None

        def make_datetime(date_text, time=timezone.datetime.min.time()):
            try:
                return timezone.make_aware(
                           timezone.datetime.combine(
                               parse(date_text), time),
                           timezone.get_current_timezone()
                       )
            except Exception:
                return None  # Just do nothing if invalid data?

        from_text = data.get('{0}_0'.format(name))
        if from_text:
            from_date = make_datetime(from_text, timezone.datetime.min.time())

        to_text = data.get('{0}_1'.format(name))
        if to_text:
            to_date = make_datetime(to_text, timezone.datetime.max.time())

        return (from_date, to_date)

    @staticmethod
    def date_range_filter(dates, field_name):
        """
        Pass in a tuple of dates (from_date, to_date)

        Returns a dictionary of queryset filters for filtering `field_name`
        by dates. i.e.

            dates = (from_date, to_date)
            date_filters = DateRangeWidget.date_range_filter(dates, 'my_date_field')
            queryset.filter(**date_filters)

        Will return dates in between gte from_date and/or lte to_date

        Why @staticmethod? Because this is designed for this MultiWidget
        and our TableFilterForm and there's no good place to access
        both the widget instance and the queryset at the same time.
        """
        filters = {}
        expire_from, expire_to = dates
        if expire_from:
            filters['{0}__gte'.format(field_name)] = expire_from
        if expire_to:
            filters['{0}__lte'.format(field_name)] = expire_to
        return filters


class ListFormField(forms.CharField):
    """
    A stupid hack to let DateRangeWidget return a list of dates instead of a string.

    Actually not even a "list" field but a "raw python field".

    May be a better way to do this.
    """
    def to_python(self, value):
        return value


class BetterFileInput(forms.ClearableFileInput):
    """ Replacement ClearableFileInput whose output is easier to control via CSS. """
    template_name = 'widgets/better_file_input.html'

    def __init__(self, attrs={}, *args, **kwargs):
        super(BetterFileInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        t = loader.get_template(self.template_name)
        return t.render(Context({'value': value, 'name': name, 'attrs': attrs}))
