from django.template.defaulttags import register
from django.template import Library


register = Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def replace(value, arg):
    arg_list = arg.split(':')
    if len(arg_list) != 2:
        return value
    return value.replace(arg_list[0], arg_list[1])