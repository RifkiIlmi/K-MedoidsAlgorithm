from django import template
import re
# from django.utils.html import conditional_escape
# from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def truncate(str):
    res = re.sub("[{}']", '', str)
    resu = re.sub("[:]",' =>', res)
    result = re.sub("[,]",'\n',resu)
    return result