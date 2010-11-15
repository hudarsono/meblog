#    Copyright 2010 Hudarsono <http://blog.hudarsono.me>
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
import urllib
from pages.models import Page
from google.appengine.api import memcache
from django.conf import settings

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
            
    if settings.BLOG_TITLE != '':
        blog_title = settings.BLOG_TITLE
            
    return {'context_pages':context_pages, 'blog_title':blog_title}
    
    
def addon(request):
    # dont turn on all of this when on development
    if settings.DEBUG == False:
        if settings.DISQUS == True:
            disqus=True
        else:
            disqus=False

        if settings.ANALYTICS == True:
            ga=True
        else:
            ga=False
    
        if settings.FBLIKE == True:
            fblike=True
        else:
            fblike=False
    else:
        disqus = ga = fblike = False
        
    return {'disqus':disqus, 'ga':ga, 'fblike':fblike}
    
    
    return {'context_pages':context_pages, 'blog_title':blog_title, 'disqus':disqus, 'ga':ga, 'fblike':fblike}

def daily_quote(request):
    if memcache.get('today_quote'):
        todayquote = memcache.get('today_quote')
    else:
        f = urllib.urlopen('http://www.iheartquotes.com/api/v1/random?max_lines=1')
        quotelines = f.readlines()
        #remove last line
        trimmedlines = quotelines[:-1]
        todayquote = ''.join(trimmedlines)
        memcache.set('today_quote', todayquote, 86400)
        
    return {'todayquote':todayquote}