import models
from django import forms


class PageForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300, required=False)
    body = forms.CharField(widget=forms.Textarea)
    template = forms.CharField(max_length=30)
    navbar = forms.BooleanField(required=False)
    publish = forms.BooleanField(required=False)

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