from wagtail.models import Site

def navigation(request):
    site = Site.find_for_request(request)
    return {'navigation': site.root_page.get_children().live().in_menu() if site else []}
