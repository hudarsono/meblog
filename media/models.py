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


import urllib

from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.ext import blobstore

from django.conf import settings

# Create your models here.
class Media(db.Model):
    title = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    media = blobstore.BlobReferenceProperty()
    filename = db.StringProperty()
    filesize = db.IntegerProperty()
    type = db.StringProperty()


    def get_absolute_url(self):
        return settings.SITE_URL+'/media/serve/%s' % self.key()

    def get_download_url(self):
        return '/media/download/%s' % self.key()
        
    def get_delete_url(self):
        return '/media/delete/%s' % self.key()
