from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def settings_value(name):
"""
This Tag allows to access values from the configuration file in the templates.
"""
    try:
        return settings.__getattr__(name)
    except AttributeError:
        return ""
