from django import template

register = template.Library()

@register.filter(name='cache_key')
def get_cache_key(model, suffix=None):
    if not model:
        return None

    if suffix is not None:
        suffix = ':%s' % suffix
    else:
        suffix = ''

    return '%s:%s%s' % (model._meta.model_name, model.pk, suffix)

def _get_cache_tag(model):
    return '%s:%s' % (model._meta.model_name, model.pk)

def get_cache_tags(*args):
    tags = []

    for arg in args:
        if hasattr(arg, '__iter__'):
            for model in arg:
                tags.append(_get_cache_tag(model))
        else:
            tags.append(_get_cache_tag(arg))

    return tags
