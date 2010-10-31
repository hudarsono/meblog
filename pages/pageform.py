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

import models
from django import forms


class PageForm(forms.Form):
    key = forms.CharField(required=False,widget=forms.HiddenInput())
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'textInput'}))
    description = forms.CharField(max_length=300, required=False,widget=forms.TextInput(attrs={'class':'textInput'}))
    body = forms.CharField(widget=forms.Textarea)
    template = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'textInput'}))
    navbar = forms.BooleanField(required=False, widget=forms.Select(choices=(('True','True'),
                                                                             ('False', 'False'))))
    publish = forms.BooleanField(widget=forms.Select(choices=(('Published','Publish Now'),
                                                              ('Private','Private'),
                                                              ('Draft','Draft'))))

    def save(self, page=None, commit=True):
        data = self.cleaned_data
        if not page: page = models.Page(key_name=data['name'].replace(' ','-'))
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

