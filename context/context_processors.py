#    Copyright 2010 Hudarsono <http://hudarsono.me>
#
#    This file is part of MeBlog.
#
#    MeBlog is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MeBlog is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MeBlog.  If not, see <http://www.gnu.org/licenses/>.



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