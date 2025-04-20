from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        if value is None:
            if key in query:
                del query[key]
        else:
            query[key] = value
    return query.urlencode()


@register.simple_tag(takes_context=True)
def preserve_query_params(context, **kwargs):
    request = context['request']
    params = request.GET.copy()
    
    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
            
    return params.urlencode()
