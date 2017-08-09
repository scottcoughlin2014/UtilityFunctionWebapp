from django.template import Library

register = Library()

@register.tag
def tag(a, b):
    return a + b