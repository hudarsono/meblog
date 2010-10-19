# Create your views here.
from posts import models
import postform
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from google.appengine.api import memcache

# class for new form
def index(request):
	return render_to_response('stream.html')


def listPost(request):
	posts = models.Post.all()
	return render_to_response('admin_postlist.html', {
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
							    'url': '/posts/category/%s' % cat,
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
	# get post list
	posts = models.Post.all()

	# get tag and categories
	cat_tag = get_tag_cat_list()

	return render_to_response('stream.html', {'posts': posts,
											  'categories': cat_tag['cat_list'],
											  'tags': cat_tag['tag_list']})


def listPostByCategory(request, cat):
	posts = models.Post.all().filter('category =', cat)

	# get tag and categories
	cat_tag = get_tag_cat_list()

	return render_to_response('stream.html', {'posts': posts,
											  'categories': cat_tag['cat_list'],
											  'tags': cat_tag['tag_list']})


def showPost(request, year, month, day, key):
	post = models.Post.get(key)

	# get tag and categories
	cat_tag = get_tag_cat_list()

	return render_to_response('post.html', {'post': post,
											  'categories': cat_tag['cat_list'],
											  'tags': cat_tag['tag_list']})

def newPost(request):
	postForm = None
	if request.method == 'POST':
		newPost = postform.NewPostForm(request.POST)
		if newPost.is_valid():
			newPost.save()
			return HttpResponseRedirect('/posts/')
		else:
			postForm = postform.NewPostForm(request.POST)


	if postForm is None:
		postForm = postform.NewPostForm()
	return render_to_response('admin_newpost.html', {
													'postForm':postForm})

def editPost(request, year, month, day, key):
	if request.method == 'POST':
		post = models.Post.get(key)
		if post:
			post.title = request.POST.get('title')
			post.body = request.POST.get('body')
			post.save()
		return HttpResponseRedirect('/posts/')

	if request.method == 'GET':
		post = models.Post.get(key)
		editPostForm = postform.NewPostForm(instance=post)
		return render_to_response('admin_newpost.html', {
														 'postForm':editPostForm,
														 'action':post.get_edit_url(),})

def delPost(request, year, month, day, key):
	post = models.Post.get(key)
	if post:
		post.delete()
	return HttpResponseRedirect('/posts/')
