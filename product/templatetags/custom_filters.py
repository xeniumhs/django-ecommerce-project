from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies value by arg"""
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0
