from django import template

register = template.Library()

@register.filter
def get_value_from_dict(d, key):
    return d.get(key)
