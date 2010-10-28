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


class PostForm(forms.Form):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'textInput'}))
    body = forms.CharField(widget=forms.Textarea())
    category = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'textInput'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'textInput'}))

    def save(self, post=None, commit=True):
        data = self.cleaned_data
        if not post: post = models.Post(key_name=data['title'].replace(' ','-'))
        post.title = data['title']
        post.body = data['body']
        post.category = data['category']
        post.tags = data['tags'].split()
        if commit: post.put()
        return post
