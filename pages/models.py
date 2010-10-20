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