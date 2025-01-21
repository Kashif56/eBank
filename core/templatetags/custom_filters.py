from django import template

register = template.Library()

@register.filter
def format_account_number(value):
    """Format account number with spaces every 4 digits"""
    if not value:
        return value
    value = str(value)
    return ' '.join(value[i:i+4] for i in range(0, len(value), 4))
