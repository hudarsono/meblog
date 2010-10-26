# Django module
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.conf import settings

# App module
from pages import models
from pageform import PageForm
from contactform import ContactForm

# Appengine module
from google.appengine.api import memcache
from google.appengine.api import mail

PAGESIZE = settings.PAGESIZE

def render(request, name):
    page = models.Page.get_by_key_name(name)
    if page:
        return render_to_response('pages/'+page.template, {'page':page},
                                                context_instance=RequestContext(request))
    else:
        raise Http404


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


def newPage(request):
    pageForm = None
    if request.method == 'POST':
        newPage = PageForm(request.POST)
        if newPage.is_valid():
            newPage.save()
            return HttpResponseRedirect('/pages/')
        else:
            pageForm = PageForm(request.POST)

    if pageForm is None:
        pageForm = PageForm()

    return render_to_response('admin/newpage.html', {
                                                     'pageForm':pageForm})


def editPage(request, key_name):
    pageForm = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        page = page = models.Page.get_by_key_name(key_name.replace('-',' '))
        if form.is_valid():
            form.save(page)
            return HttpResponseRedirect('/pages/')
        else:
            pageForm = PageForm(request.POST)

    if pageForm is None:
        page = models.Page.get_by_key_name(key_name.replace('-',' '))
        if page:
            pageForm = PageForm(initial={'name':page.name,
                                         'description':page.description,
                                         'body':page.body,
                                         'template':page.template,
                                         'publish':page.publish})
    return render_to_response('admin/newpage.html', {'pageForm':pageForm,
                                                     'action':page.get_edit_url()})

def delPage(request, key_name):
    page = models.Page.get_by_key_name(key_name.replace('-',' '))
    if page:
        page.delete()
    return HttpResponseRedirect('/pages/')


def contact(request):
    form = None
    msg = None
    if request.method == 'POST':
        newMessage = ContactForm(request.POST)
        if newMessage.is_valid():
            data = newMessage.cleaned_data
            #send message
            mail.send_mail(sender="hudarsono.appspot.com <contact@hudarsono.appspot.com>",
                              to="Hudarsono <hudarsono@gmail.com>",
                              subject="New Message from "+data['name'],
                              body="Sender Email : "+data['email']+"\n Message : "+data['message'])

            msg = 'Thanks for your message, will get back to you soon.'
        else:
            form = ContactForm(request.POST)

    if form is None: form = ContactForm()

    return render_to_response('pages/contact.html', {'form':form, 'msg':msg},
                                                   context_instance=RequestContext(request))