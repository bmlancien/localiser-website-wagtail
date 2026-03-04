from wagtail.models import Site


def nav_pages(request):
    site = Site.find_for_request(request)
    if not site:
        return {"nav_pages": []}
    root = site.root_page
    return {"nav_pages": root.get_children().live().in_menu().specific()}
