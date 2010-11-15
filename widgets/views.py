from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext


from google.appengine.api import memcache
from utilities.auth_helper import login_required


from widgets import models
import widgetform

def listWidget(request):
    widgets = models.Widget.all()
    return render_to_response('admin/widgetlist.html', {'widgets':widgets})
    

def newWidget(request):
    c = {}
    c.update(csrf(request))
    widgetForm = None
    if request.method == 'POST':
        newWidget = widgetform.WidgetForm(request.POST)
        if newWidget.is_valid():
            newWidget.save()
            memcache.flush_all()
            return HttpResponseRedirect('/widgets/')
        else:
            widgetForm = widgetform.WidgetForm(request.POST)
    
    if widgetForm is None:
        widgetForm = widgetform.WidgetForm()
        
    return render_to_response('admin/widgetform.html', {'widgetForm':widgetForm},
                                                    context_instance=RequestContext(request))
                                                    

def editWidget(request, key):
    c = {}
    c.update(csrf(request))
    widgetForm = None
    if request.method == 'POST':
        form = widgetform.WidgetForm(request.POST)
        widget = models.Widget.get(key)
        if form.is_valid():
            form.save(widget)
            memcache.flush_all()
            return HttpResponseRedirect('/widgets/')
        else:
            widgetForm = widgetform.WidgetForm(request.POST)
    
    if widgetForm is None:
        widget = models.Widget.get(key)
        if widget:
            widgetForm = widgetform.WidgetForm(initial={'key':widget.key(),
                                                        'title':widget.title,
                                                        'body':widget.body,
                                                        'enabled':widget.enabled})
    return render_to_response('admin/widgetform.html', {'widgetForm':widgetForm,
                                                        'action':widget.get_edit_url()},
                                                        context_instance=RequestContext(request))
                                                        
def delWidget(request, key):
    widget = models.Widget.get(key)
    if widget:
        widget.delete()
        memcache.flush_all()
    return HttpResponseRedirect('/widgets/')