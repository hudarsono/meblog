from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.ext import blobstore

# Create your models here.
class Media(db.Model):
	title = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	media = blobstore.BlobReferenceProperty()
