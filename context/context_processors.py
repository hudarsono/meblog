# this is a context processor for template
from pages.models import Page
from google.appengine.api import memcache

def pages(request):
    if memcache.get('context_pages'):
        context_pages = memcache.get('context_pages')
    else:
        pages = Page.all().filter('publish =', True)

        # get all page titles and url
        context_pages = []

        if pages :
            for page in pages:
                context_pages.append({'name':page.name,
                                      'url':page.get_absolute_url()})
            memcache.set('context_pages', context_pages)

    return {'context_pages':context_pages}