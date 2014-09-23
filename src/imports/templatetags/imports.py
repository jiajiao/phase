import json

from django import template


register = template.Library()


@register.simple_tag
def errors_to_list(json_data):
    """Takes a json encoded dict and returns html"""
    data = json.loads(json_data)
    data = [(k, v[0]) for k, v in data.items()]
    data_list = ''.join(['<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in data])
    return '<dl>%s</dl>' % data_list