# Create your views here.
from posts import models
import postform
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

from django.conf import settings

from google.appengine.api import memcache

from gaesessions import get_current_session


def listPost(request):
	posts = models.Post.all().order('-pub_date')
	return render_to_response('admin/postlist.html', {
													  'posts':posts})


def get_tag_cat_list():

	cat_tag = memcache.get('cat_tag')
	if cat_tag is not None:
		return cat_tag

	posts = models.Post.all()

	# get all category
	cat_list = {}
	for p in posts:
		if p.category in cat_list:
			cat_list[p.category] += 1
		else:
			cat_list[p.category] = 1

	sorted_cat_list = []
	for cat in sorted(cat_list):
		sorted_cat_list.append({'category': cat,
							    'count':cat_list[cat],
							    'url': '/posts/category/%s' % cat.replace(' ','-'),
							    })

	# get all tags
	tag_list = {}
	for p in posts:
		for tag in p.tags:
			if tag in tag_list:
				tag_list[tag] +=1
			else:
				tag_list[tag] = 1

	sorted_tag_list = []
	for tag in sorted(tag_list.iterkeys()):
		sorted_tag_list.append({'tag': tag,
                                'count': tag_list[tag],
                                'url': '/posts/tag/%s' % (tag),
                               })

	cat_tag  = {'tag_list': sorted_tag_list,
		    	'cat_list': sorted_cat_list}

	memcache.set('cat_tag', cat_tag)
	return cat_tag




def stream(request):
	PAGESIZE = int(settings.PAGESIZE)
	offset = 0

	# get post list
	if request.GET.get('page'):
		#get the corrent page
		page = int(request.GET.get('page'))
	else:
		page = 1


	offset = settings.PAGESIZE *(page - 1)

	if memcache.get('blogpage-'+str(page)):
		posts = memcache.get('blogpage-'+str(page))
	else:
		posts = models.Post.all().order('-pub_date').fetch(settings.PAGESIZE, offset)
		memcache.set('blogpage-'+str(page), posts)

	# check if there is next page
	offset = settings.PAGESIZE *(page)
	next_page = models.Post.all().order('-pub_date').fetch(settings.PAGESIZE, offset)
	if next_page:
		p_next = page + 1
	else:
		p_next = None

	paging = {'prev': page - 1, 'next':p_next}
	# get tag and categories
	cat_tag = get_tag_cat_list()

	return render_to_response('front/stream.html', {'posts': posts,
												    'paging':paging,
													  'categories': cat_tag['cat_list'],
													  'tags': cat_tag['tag_list']},
		                           						context_instance=RequestContext(request))




def listPostByCategory(request, cat):
	posts = models.Post.all().filter('category =', cat.replace('-',' '))

	# get tag and categories
	cat_tag = get_tag_cat_list()

	return render_to_response('front/stream.html', {'posts': posts,
													  'categories': cat_tag['cat_list'],
													  'tags': cat_tag['tag_list']},
		                           						context_instance=RequestContext(request))



def listPostByTag(request, tag):
	posts = models.Post.all().filter('tags =', tag)

	# get tag and categories
	cat_tag = get_tag_cat_list()
	return render_to_response('front/stream.html', {'posts': posts,
											  'categories': cat_tag['cat_list'],
											  'tags': cat_tag['tag_list']},
                           						context_instance=RequestContext(request))



def showPost(request, year, month, day, key_name):
	post = models.Post.get_by_key_name(key_name)
	if post:
		# get tag and categories
		cat_tag = get_tag_cat_list()

		return render_to_response('front/post.html', {'post': post,
													  'categories': cat_tag['cat_list'],
													  'tags': cat_tag['tag_list']},
		                           						context_instance=RequestContext(request))
	else:
		raise Http404


def newPost(request):
	postForm = None
	if request.method == 'POST':
		newPost = postform.PostForm(request.POST)
		if newPost.is_valid():
			newPost.save()
			return HttpResponseRedirect('/posts/')
		else:
			postForm = postform.PostForm(request.POST)


	if postForm is None:
		postForm = postform.PostForm()
	return render_to_response('admin/newpost.html', {
													'postForm':postForm})


def editPost(request, year, month, day, key_name):
	if request.method == 'POST':
		post = models.Post.get_by_key_name(key_name)
		if post:
			form = postform.PostForm(request.POST)
			if form.is_valid():
				form.save(post)
		return HttpResponseRedirect('/posts/')

	if request.method == 'GET':
		post = models.Post.get_by_key_name(key_name)
		editPostForm = postform.PostForm(initial={
												  'title': post.title,
												  'body': post.body,
												  'category': post.category,
												  'tags': ' '.join(post.tags)})
		return render_to_response('admin/newpost.html', {
														 'postForm':editPostForm,
														 'action':post.get_edit_url(),})


def delPost(request, year, month, day, key_name):
	post = models.Post.get_by_key_name(key_name)
	if post:
		post.delete()
	return HttpResponseRedirect('/posts/')
