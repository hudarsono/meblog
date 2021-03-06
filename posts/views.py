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

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.conf import settings
from django.core.context_processors import csrf

from google.appengine.api import memcache

from posts import models
from posts import postform
from utilities.auth_helper import login_required

from django.template.loader import render_to_string
import django_mobile 
from gaesessions import get_current_session

PAGESIZE = settings.PAGESIZE

@login_required
def listPost(request):
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1

    offset = PAGESIZE *(page - 1)

    if memcache.get('postpage-'+str(page)):
        posts = memcache.get('postpage-'+str(page))
    else:
        posts = models.Post.all().order('-pub_date').fetch(PAGESIZE, offset)
        memcache.set('postpage-'+str(page), posts)

    # check if there is next page
    offset = PAGESIZE *(page)
    next_page = models.Post.all().order('-pub_date').fetch(PAGESIZE, offset)
    if next_page:
        p_next = page + 1
    else:
        p_next = None

    paging = {'prev': page - 1, 'next':p_next}
    return render_to_response('admin/postlist.html', {'posts':posts,
                            						'paging':paging})


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
  if cat_list:
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

  if tag_list:
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
  
  if request.GET.get('mobile'):
    if request.GET.get('mobile') == 'full':
        django_mobile.set_flavour('full');
  

  session = get_current_session()
  if session.is_active():
    if request.GET.get('mobile'):
        session['mobile'] = request.GET.get('mobile');
  
    if session.has_key('mobile'):
        if session['mobile'] == 'off':
            django_mobile.set_flavour('full');
  else:
    session.start()

  rendered  = render_to_string('front/stream.html', {'posts': posts,
                                'paging':paging,
                                'categories': cat_tag['cat_list'],
                                'tags': cat_tag['tag_list']},
                                context_instance=RequestContext(request))
                                
  return HttpResponse(rendered)




def listPostByCategory(request, cat):
  PAGESIZE = int(settings.PAGESIZE)
  offset = 0

  # get post list
  if request.GET.get('page'):
    page = int(request.GET.get('page'))
  else:
    page = 1

  offset = settings.PAGESIZE *(page - 1)

  if memcache.get('catpage-'+str(page)):
    posts = memcache.get('catpage-'+str(page))
  else:
    posts = models.Post.all().order('-pub_date').filter('category =', cat.replace('-',' ')).fetch(settings.PAGESIZE, offset)
    memcache.set('catpage-'+str(page), posts)

  # check if there is next page
  offset = settings.PAGESIZE *(page)
  next_page = models.Post.all().order('-pub_date').filter('category =', cat.replace('-',' ')).fetch(settings.PAGESIZE, offset)
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



def listPostByTag(request, tag):
  PAGESIZE = int(settings.PAGESIZE)
  offset = 0

  # get post list
  if request.GET.get('page'):
    page = int(request.GET.get('page'))
  else:
    page = 1

  offset = settings.PAGESIZE *(page - 1)

  if memcache.get('catpage-'+str(page)):
    posts = memcache.get('catpage-'+str(page))
  else:
    posts = models.Post.all().order('-pub_date').filter('tags =', tag).fetch(settings.PAGESIZE, offset)
    memcache.set('catpage-'+str(page), posts)

  # check if there is next page
  offset = settings.PAGESIZE *(page)
  next_page = models.Post.all().order('-pub_date').filter('tags =', tag).fetch(settings.PAGESIZE, offset)
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



def showPost(request, year, month, day, key_name):
  if memcache.get('page-'+key_name):
    post = memcache.get('page-'+key_name)
  else:
    post = models.Post.get_by_key_name(key_name)
    memcache.set('page-'+key_name, post)

  if post:
    # get tag and categories
    cat_tag = get_tag_cat_list()
    
    session = get_current_session()
    if session.is_active():
      if request.GET.get('mobile'):
          session['mobile'] = request.GET.get('mobile');
  
      if session.has_key('mobile'):
          if session['mobile'] == 'off':
              django_mobile.set_flavour('full');
    else:
      session.start()

    return render_to_response('front/post.html', {'post': post,
                            'categories': cat_tag['cat_list'],
                            'tags': cat_tag['tag_list']},
                             context_instance=RequestContext(request))
  else:
    raise Http404


@login_required
def newPost(request):
  c = {}
  c.update(csrf(request))
  postForm = None
  if request.method == 'POST':
    newPost = postform.PostForm(request.POST)
    if newPost.is_valid():
      newPost.save()

      #flush memcache
      memcache.flush_all()
      return HttpResponseRedirect('/posts/')
    else:
      postForm = postform.PostForm(request.POST)


  if postForm is None:
    postForm = postform.PostForm()

  return render_to_response('admin/newpost.html', {
                          'postForm':postForm},context_instance=RequestContext(request))



@login_required
def editPost(request, year, month, day, key):
  c = {}
  c.update(csrf(request))
  if request.method == 'POST':
    post = models.Post.get(key)
    if post:
      form = postform.PostForm(request.POST)
      if form.is_valid():
        form.save(post)
        memcache.flush_all()
    return HttpResponseRedirect('/posts/')

  if request.method == 'GET':
    post = models.Post.get(key)
    editPostForm = postform.PostForm(initial={'key':post.key(),
                          'title': post.title,
                          'body': post.body,
                          'category': post.category,
                          'tags': ' '.join(post.tags)})

    return render_to_response('admin/newpost.html', {
                             'postForm':editPostForm,
                             'action':post.get_edit_url()},context_instance=RequestContext(request))



@login_required
def delPost(request, year, month, day, key):
  post = models.Post.get(key)
  if post:
    post.delete()

    # refresh memcache
    memcache.flush_all()
  return HttpResponseRedirect('/posts/')
