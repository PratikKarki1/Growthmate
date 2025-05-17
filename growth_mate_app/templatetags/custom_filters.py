from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Split a string by the given delimiter and return the list
    """
    return value.split(delimiter)

@register.filter
def first(value):
    """
    Return the first element of a list
    """
    if value and len(value) > 0:
        return value[0]
    return ''

@register.filter
def last(value):
    """
    Return the last element of a list
    """
    if value and len(value) > 0:
        return value[-1]
    return '' 