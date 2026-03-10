from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_page_translations(context):
    """Returns all live translations of the current page, including itself."""
    page = context.get("page")
    if page:
        return page.get_translations(inclusive=True).filter(live=True).select_related("locale")
    return []
