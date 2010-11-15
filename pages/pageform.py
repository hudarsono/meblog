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

import os

from django.conf import settings
from django import forms

import models
from widgets.models import Widget

from google.appengine.api import memcache

# this utils used to construct keyname from post or page title by removing unallowed char
from utilities.utils import construct_keyname


class PageForm(forms.Form):
    key = forms.CharField(required=False,widget=forms.HiddenInput())
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'textInput'}))
    description = forms.CharField(max_length=300, required=False,widget=forms.TextInput(attrs={'class':'textInput'}))
    body = forms.CharField(widget=forms.Textarea)
    template = forms.ChoiceField()
    widget = forms.ChoiceField(required=False, widget=forms.SelectMultiple())
    navbar = forms.BooleanField(required=False, widget=forms.Select(choices=(('True','True'),
                                                                             ('False', 'False'))))
    publish = forms.BooleanField(widget=forms.Select(choices=(('Published','Publish Now'),
                                                              ('Private','Private'),
                                                              ('Draft','Draft'))))

    
    def __init__(self, *args, **kwrds):
        super(PageForm,self).__init__(*args, **kwrds)
        
        # read available templates
        path = os.path.join(settings.ROOT_PATH,'templates','pages')
        templates = os.listdir(path)
        self.fields['template'].choices=[[x,x] for x in templates]
        
        # read available widget
        if memcache.get('widgets_enabled'):
            widgets = memcache.get('widgets_enabled')
        else:
            widgets = Widget.all().filter('enabled =',True)
            memcache.set('widgets_enabled', widgets)
        self.fields['widget'].choices = ()
        for w in widgets:
            self.fields['widget'].choices.append([str(w.key()), w.title])
        
    
    def save(self, page=None, commit=True):
        data = self.cleaned_data
        if not page: page = models.Page(key_name=construct_keyname(data['name']))
        page.name = data['name']
        page.description = data['description']
        page.body = data['body']
        page.template = data['template']
        page.publish = data['publish']
        if commit: page.put()
        return page
        
     
    
    # prevent the same page 's name
    def clean_name(self):
        name = self.cleaned_data['name']
        query = models.Page.all(keys_only=True)
        query.filter('name = ', name)
        
        page = query.get()
        
        if page and (not self.cleaned_data['key']):
            raise forms.ValidationError('Page name "%s" was already used before' % name)
           
        return name

