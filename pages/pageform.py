import models
from django import forms


class PageForm(forms.Form):
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