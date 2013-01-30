from django.contrib import messages
from django.views.generic import TemplateView


class TextPlainView(TemplateView):
    "A base view for serving plain text files via templates"
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(
            context, content_type='text/plain', **kwargs)


class RobotsTxtView(TextPlainView):
    template_name = 'robots.txt'


class FormMessagesMixin(object):
    """
    Use to add a success_message and fail_message to any view
    that calls form_valid and form_invalid.

    Default success and error message uses either class name of
    view's object or 'Form' if self.model is not set.

    To override, set `success_message` or `error_message` or
    override `get_success_message` or `get_error_message`
    """
    success_message = None
    error_message = None

    def message_obj_name(self):
        return self.model.__name__ if hasattr(self, 'model') else 'Form'

    def get_success_message(self):
        if self.success_message:
            return self.success_message
        return "{0} saved.".format(self.message_obj_name())

    def get_error_message(self):
        if self.error_message:
            return self.error_message
        return "Error saving {0}.".format(self.message_obj_name())

    def form_valid(self, form):
        messages.success(self.request, self.get_success_message())
        return super(FormMessagesMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.get_error_message())
        return super(FormMessagesMixin, self).form_invalid(form)
