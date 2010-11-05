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

from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.api import users

# Create your models here.
import datetime
import markdown
import re

class Post(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    body_html = db.TextProperty()
    category = db.CategoryProperty()
    tags = db.StringListProperty()
    pub_date = db.DateTimeProperty(auto_now_add=True)
    last_update = db.DateTimeProperty(auto_now=True)
    author = db.UserProperty(auto_current_user_add=True)

    def get_absolute_url(self):
        return "/post/%04d/%02d/%02d/%s" % (self.pub_date.year,
                                            self.pub_date.month,
                                            self.pub_date.day,
                                            self.title.replace(' ','-'))

    def get_edit_url(self):
        return "/post/edit/%04d/%02d/%02d/%s" % (self.pub_date.year,
                                                   self.pub_date.month,
                                                   self.pub_date.day,
                                                   self.key())

    def get_delete_url(self):
        return "/post/delete/%04d/%02d/%02d/%s" % (self.pub_date.year,
                                                   self.pub_date.month,
                                                   self.pub_date.day,
                                                   self.key())

    def trunc_body(self):
        # remove image
        p = re.compile(r'<img.*?>')
        body = p.sub('', self.body_html)
        if len(body) > 500:
            return body[:500].rsplit(' ', 1)[0]+'...'+'<a href="'+self.get_absolute_url()+'">Read More</a>'
        else:
            return body


    def put(self):
        self.populate_html()
        
        # get author
        self.author = users.get_current_user()
        key = super(Post, self).put()
        return key


    def populate_html(self):
        md = markdown.Markdown(extensions=['codehilite'])

        if self.body:
            self.body_html = md.convert(self.body)

