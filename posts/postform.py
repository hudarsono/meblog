import models
from google.appengine.ext.db import djangoforms

class NewPostForm(djangoforms.ModelForm):
    class Meta:
        model = models.Post
        exclude = ['author', 'pub_date']