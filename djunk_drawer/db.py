


def get_first_or_none(model, **kwargs):
    "Try to get an object by **kwargs. return the first object or None"
    try:
        return model._default_manager.filter(**kwargs)[0]
    except IndexError:
        return None
