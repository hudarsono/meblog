from django import forms


class FileForm(forms.Form):
	title = forms.CharField(required=True)
	