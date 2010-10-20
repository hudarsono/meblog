# Create your views here.
from pages import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext

from pageform import PageForm
from contactform import ContactForm

from google.appengine.api import memcache
from google.appengine.api import mail

def render(request, name):
    page = models.Page.get_by_key_name(name)
    if page:
        return render_to_response('pages/'+page.template, {'page':page},
                                                context_instance=RequestContext(request))
    else:
        raise Http404


def listPages(request):
    pages = models.Page.all()
    return render_to_response('admin_pagelist.html', {
                                                     'pages':pages})

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

    return render_to_response('admin_newpage.html', {
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
    return render_to_response('admin_newpage.html', {'pageForm':pageForm,
                                                     'action':page.get_edit_url()})

def delPage(request, key_name):
    page = models.Page.get_by_key_name(key_name.replace('-',' '))
    if page:
        page.delete()
    return HttpResponseRedirect('/pages/')


def contact(request):
    form = None
    if request.method == 'POST':
        newMessage = ContactForm(request.POST)
        if newMessage.is_valid():
            #send message
            mail.send_mail(sender="hudarsono.appspot.com <contact@hudarsono.appspot.com>",
                              to="Hudarsono <hudarsono@gmail.com>",
                              subject="New Message from "+newMessage.name,
                              body="Sender Email : "+newMessage.email+"\n Message : "+newMessage.message)
        else:
            form = ContactForm(request.POST)

    if form is None: form = ContactForm()

    return render_to_response('pages/contact.html', {'form':form},
                                                   context_instance=RequestContext(request))