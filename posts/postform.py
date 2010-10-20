import models
from django import forms


class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    category = forms.CharField(max_length=30)
    tags = forms.CharField()

    def save(self, post=None, commit=True):
        data = self.cleaned_data
        if not post: post = models.Post(key_name=data['title'].replace(' ','-'))
        post.title = data['title']
        post.body = data['body']
        post.category = data['category']
        post.tags = data['tags'].split()
        if commit: post.put()
        return post
