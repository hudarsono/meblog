from django.contrib.syndication.views import Feed
from posts.models import Post
from django.conf import settings

from google.appengine.api import memcache


class LatestFeed(Feed):
	title = settings.BLOG_TITLE
	link = settings.SITE_URL
	description = 'Latest Update'
	
	item_author_name = settings.AUTHOR
	item_author_email = settings.AUTHOR_EMAIL
	item_author_link = settings.SITE_URL
	
	def items(self):
		if memcache.get('feed_latest'):
			posts = memcache.get('feed_latest')
		else:
			posts = Post.all().order('-pub_date').fetch(10)
			memcache.set('feed_latest', posts)
		return posts
			
	def item_title(self, item):
		return item.title
		
	def item_description(self, item):
		return item.trunc_body()