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


from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
import datetime
import markdown

class Page(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    body = db.TextProperty()
    body_html = db.TextProperty()
    template = db.StringProperty()
    navbar = db.BooleanProperty()
    publish = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty(auto_current_user_add=True)

    def get_absolute_url(self):
        return "/%s" % self.name

    def get_delete_url(self):
        return "/page/delete/%s" % (self.name)

    def get_edit_url(self):
        return "/page/edit/%s" % (self.name)

    def put(self):
        self.check_double_name()
        self.populate_html()
        key = super(Page, self).put()
        return key

    def check_double_name(self):
        query = Page.all(keys_only=True)
        query.filter('name = ', self.name)

        page = query.get()

        if page and (not self.is_saved() or self.key() != page):
            raise PageConstraintViolation(self.name)

    def populate_html(self):
        md = markdown.Markdown(extensions=['codehilite'])

        if self.body:
            self.body_html = md.convert(self.body)

class PageConstraintViolation(Exception):
    def __init__(self, name):
        super(PageConstraintViolation, self).__init__("Page with name '%s' was already used before" % name )