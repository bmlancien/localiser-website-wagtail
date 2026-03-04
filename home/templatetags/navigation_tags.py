from django import template
from wagtail.models import Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_nav_pages(context):
    request = context.get("request")
    site = Site.find_for_request(request) if request else Site.objects.first()
    if not site:
        return []
    root = site.root_page
    return root.get_children().live().in_menu().specific()
