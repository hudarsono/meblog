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

# this utils used to construct keyname from post or page title by removing unallowed char
from utilities.utils import construct_keyname



class PostForm(forms.Form):
    key = forms.CharField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'textInput'}))
    body = forms.CharField(widget=forms.Textarea())
    category = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'textInput'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'textInput'}))

    def save(self, post=None, commit=True):
        data = self.cleaned_data
        if not post: post = models.Post(key_name=construct_keyname(data['title']))
        post.title = data['title']
        post.body = self.data['body']
        post.category = data['category']
        post.tags = data['tags'].split()
        if commit: post.put()
        return post
        
    
    def clean_title(self):
        title = self.cleaned_data['title']
        query = models.Post.all(keys_only=True)
        query.filter('title = ', title)

        post = query.get()

        if post and not self.cleaned_data['key']:
            raise forms.ValidationError('Title "%s" already used before.' % title)

        return title