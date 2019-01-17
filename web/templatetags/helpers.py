from django import template

register = template.Library()


@register.filter
def get_class(instance):
    return instance.__class__.__name__


@register.filter
def name(user):
    if user.first_name and user.last_name:
        return user.first_name + ' ' + user.last_name
    elif user.first_name:
        return user.first_name
    return user.username
