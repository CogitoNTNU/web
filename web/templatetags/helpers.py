from django import template

register = template.Library()

@register.filter
def get_class(instance):
    return instance.__class__.__name__
