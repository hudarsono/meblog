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

class WidgetForm(forms.Form):
    key = forms.CharField(required=False, max_length=30,widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'TextInput'}))
    body = forms.CharField(widget=forms.Textarea())
    enabled = forms.BooleanField(required=False, widget=forms.Select(choices=(('True','True'),('False','False'))))

    def save(self, widget=None, commit=True):
        data = self.cleaned_data
        if not widget: widget = models.Widget()
        widget.title = data['title']
        widget.body = data['body']
        widget.enabled = data['enabled']
        if commit: widget.put()
        return widget