# this is a context processor for template
from pages.models import Page

def pages(request):
    pages = Page.all().filter('publish =', True)

    # get all page titles and url
    context_pages = []

    if pages :
        for page in pages:
            context_pages.append({'name':page.name,
                                  'url':page.get_absolute_url()})

    return {'context_pages':context_pages}