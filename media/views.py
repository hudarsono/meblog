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

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from google.appengine.ext import blobstore
from google.appengine.api import memcache


from media import models
from fileform import FileForm
from utilities import blob_helper
from utilities.auth_helper import login_required


ADMIN_PAGESIZE = settings.PAGESIZE

@login_required
def listMedia(request):
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1

    offset = ADMIN_PAGESIZE *(page - 1)

    if memcache.get('mediapage-'+str(page)):
        list = memcache.get('mediapage-'+str(page))
    else:
        list = models.Media.all().order('-created').fetch(ADMIN_PAGESIZE, offset)
        memcache.set('mediapage-'+str(page), list)

    # check if there is next page
    offset = ADMIN_PAGESIZE *(page)
    next_page = models.Media.all().order('-created').fetch(ADMIN_PAGESIZE, offset)
    if next_page:
        p_next = page + 1
    else:
        p_next = None

    paging = {'prev': page - 1, 'next':p_next}

    return render_to_response('admin/medialist.html', {'list':list,
                                                 'paging':paging})


@login_required
def delMedia(request, key):
    blob_key = str(urllib.unquote(key))
    blobstore.delete(blob_key)
    memcache.delete('mediapage-1')
    return HttpResponseRedirect('/media/')


@csrf_exempt
@login_required
def upload(request):
    form = None
    if request.method =='POST':
        blob_info = blob_helper.get_uploads(request, field_name='media', populate_post=True)
        form = FileForm(request.POST)
        if form.is_valid() and len(blob_info) == 1:
            media_item = models.Media(title=form.cleaned_data['title'],
                                   media=blob_info[0],
                                   filename = blob_info[0].filename,
                                   filesize = blob_info[0].size,
                                   type = blob_info[0].content_type)
            media_item.put()
            memcache.flush_all()
            return HttpResponseRedirect('/media/')

        if len(media_blobs) == 0:
            request.session['upload_error'] = "Media file is required"

        form = FileForm(request.POST)

    if form is None: form = FileForm()
    upload_url = blobstore.create_upload_url('/media/upload/')
    return render_to_response('admin/upload.html', {'upload_url':upload_url,
													'upload_error': request.session.pop('upload_error', None),
													'form': form})

def serve(request, key):
    media = models.Media.get(key)
    return blob_helper.send_blob(request, media.media, save_as=False) 
                                                    
def download(request, key):
    media = models.Media.get(key)
    return blob_helper.send_blob(request, media.media, save_as=True)