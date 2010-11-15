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

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from posts.models import Post
from django.conf import settings

from google.appengine.api import memcache

class LatestRSSFeed(Feed):
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
		
class LatestAtomFeed(LatestRSSFeed):
    feed_type = Atom1Feed
    subtitle = LatestRSSFeed.description