from wagtail.models import Page, Site

# Defines which pages appear as dropdown children of which parent nav item.
# Key: parent page slug, Value: list of child page slugs.
# Page tree position does not matter — URLs remain independent.
NAV_GROUPS = {
    "hydrogen": ["hydrogen-registration"],
}


def nav_pages(request):
    site = Site.find_for_request(request)
    if not site:
        return {"nav_pages": []}
    root = site.root_page

    all_pages = {
        p.slug: p
        for p in site.root_page.get_descendants().live().in_menu().specific()
    }

    nav = []
    grouped_slugs = {slug for children in NAV_GROUPS.values() for slug in children}

    for page in all_pages.values():
        if page.slug in grouped_slugs:
            continue  # rendered as a dropdown child, not a top-level item
        children = [
            all_pages[slug]
            for slug in NAV_GROUPS.get(page.slug, [])
            if slug in all_pages
        ]
        nav.append({"page": page, "children": children})

    return {"nav_pages": nav}
