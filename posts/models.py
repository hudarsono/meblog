from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
import datetime
import markdown

class Post(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    body_html = db.TextProperty()
    category = db.CategoryProperty()
    tags = db.StringListProperty()
    pub_date = db.DateTimeProperty(auto_now_add=True)
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
                                                   self.title.replace(' ','-'))

    def get_delete_url(self):
        return "/post/delete/%04d/%02d/%02d/%s" % (self.pub_date.year,
                                                   self.pub_date.month,
                                                   self.pub_date.day,
                                                   self.title.replace(' ','-'))

    def trunc_body(self):
        if len(self.body) > 500:
            return self.body[:500].rsplit(' ', 1)[0]+'...'+'<a href="'+self.get_absolute_url()+'">Read More</a>'
        else:
            return self.body


    def put(self):
        self.check_double_title()
        self.populate_html()
        key = super(Post, self).put()
        return key

    def check_double_title(self):
        query = Post.all(keys_only=True)
        query.filter('title = ', self.title)

        post = query.get()

        if post and (not self.is_saved() or self.key() != post):
            raise TitleConstraintViolation(self.title)

    def populate_html(self):
        md = markdown.Markdown(extensions=['codehilite'])

        if self.body:
            self.body_html = md.convert(self.body)


class TitleConstraintViolation(Exception):
    def __init__(self, title):
        super(TitleConstraintViolation, self).__init__("Title '%s' was already used before" % title )