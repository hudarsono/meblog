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

# Python module
import os

# Django module
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.conf import settings
from django.core.context_processors import csrf


# App module
from pages import models
from pageform import PageForm
from contactform import ContactForm
from utilities.auth_helper import login_required

# Appengine module
from google.appengine.api import memcache
from google.appengine.api import mail

from django.template.loader import render_to_string
import django_mobile 
from gaesessions import get_current_session

PAGESIZE = settings.PAGESIZE

def render(request, name):
    page = models.Page.get_by_key_name(name)
    if page:
        if page.template:
            template = page.template
        else:
            template = 'default.html'
            
        session = get_current_session()
        if session.is_active():
            if request.GET.get('mobile'):
                session['mobile'] = request.GET.get('mobile');

            if session.has_key('mobile'):
                if session['mobile'] == 'off':
                    django_mobile.set_flavour('full');
        else:
            session.start()
        rendered = render_to_string('pages/'+template, {'page':page},
                                                context_instance=RequestContext(request))
                                                
        return HttpResponse(rendered);
    else:
        raise Http404


@login_required
def listPages(request):
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1

    offset = PAGESIZE *(page - 1)

    if memcache.get('pagespage-'+str(page)):
        pages = memcache.get('pagespage-'+str(page))
    else:
        pages = models.Page.all().fetch(PAGESIZE, offset)
        memcache.set('pagespage-'+str(page), pages)

    # check if there is next page
    offset = PAGESIZE *(page)
    next_page = models.Page.all().fetch(PAGESIZE, offset)
    if next_page:
        p_next = page + 1
    else:
        p_next = None

    paging = {'prev': page - 1, 'next':p_next}

    return render_to_response('admin/pagelist.html', {'pages':pages,
                                                      'paging':paging})


@login_required
def newPage(request):
    c = {}
    c.update(csrf(request))
    pageForm = None
    if request.method == 'POST':
        newPage = PageForm(request.POST)
        if newPage.is_valid():
            newPage.save()
            memcache.flush_all()
            return HttpResponseRedirect('/pages/')
        else:
            pageForm = PageForm(request.POST)

    if pageForm is None:
        pageForm = PageForm()
        

    return render_to_response('admin/newpage.html', {'pageForm':pageForm},
                                                    context_instance=RequestContext(request))


@login_required
def editPage(request, key):
    c = {}
    c.update(csrf(request))
    pageForm = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        page = models.Page.get(key)
        if form.is_valid():
            form.save(page)
            memcache.flush_all()
            return HttpResponseRedirect('/pages/')
        else:
            pageForm = PageForm(request.POST)

    if pageForm is None:
        page = models.Page.get(key)
        if page:
            pageForm = PageForm(initial={'key':page.key(),
                                         'name':page.name,
                                         'description':page.description,
                                         'body':page.body,
                                         'template':page.template,
                                         'publish':page.publish})
    return render_to_response('admin/newpage.html', {'pageForm':pageForm,
                                                     'action':page.get_edit_url()},
                                                     context_instance=RequestContext(request))

@login_required
def delPage(request, key):
    page = models.Page.get(key)
    if page:
        page.delete()
        memcache.flush_all()
    return HttpResponseRedirect('/pages/')


def contact(request):
    c = {}
    c.update(csrf(request))
    form = None
    msg = None
    if request.method == 'POST':
        newMessage = ContactForm(request.POST)
        if newMessage.is_valid():
            data = newMessage.cleaned_data
            #send message
            mail.send_mail(sender='AppSpot <'+settings.AUTHOR_EMAIL+'>',
                              to=settings.AUTHOR+' <'+settings.AUTHOR_EMAIL+'>',
                              subject="New Message from "+data['name'],
                              body="Sender Email : "+data['email']+"\n\nMessage :\n"+data['message'])

            msg = 'Thanks for your message, will get back to you soon.'

        else:
            form = ContactForm(request.POST)

    if form is None: form = ContactForm()
    
    session = get_current_session()
    if session.is_active():
        if request.GET.get('mobile'):
            session['mobile'] = request.GET.get('mobile');

        if session.has_key('mobile'):
            if session['mobile'] == 'off':
                django_mobile.set_flavour('full');
    else:
        session.start()

    rendered =  render_to_string('pages/contact.html', {'form':form, 'msg':msg},
                                                   context_instance=RequestContext(request))
    return HttpResponse(rendered)