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

import models
from django import forms


class PageForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300, required=False)
    body = forms.CharField(widget=forms.Textarea)
    template = forms.CharField(max_length=30)
    navbar = forms.BooleanField(required=False)
    publish = forms.BooleanField()

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