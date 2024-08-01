# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def format_number(value):
    try:
        return '{:,}'.format(value).replace(',', ' ')
    except (ValueError, TypeError):
        return value


@register.filter
def pluralize(value):
    if value % 10 == 1 and value % 100 != 11:
        return f"{value} товар"
    elif value % 10 in [2, 3, 4] and (value % 100 < 10 or value % 100 >= 20):
        return f"{value} товара"
    else:
        return f"{value} товаров"
