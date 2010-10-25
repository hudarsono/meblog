# Create your views here.
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from google.appengine.ext import blobstore
from media import models
from fileform import FileForm
from utilities import blob_helper

def upload(request):
    form = None
    if request.method =='POST':
        blob_info = blob_helper.get_uploads(request, field_name='media', populate_post=True)
        form = FileForm(request.POST)
        if form.is_valid() and len(blob_info) == 1:
            media_item = models.Media(title=form.cleaned_data['title'],
                                   media=blob_info[0])
            media_item.put()
            return HttpResponseRedirect('/posts/')

        if len(media_blobs) == 0:
            request.session['upload_error'] = "Media file is required"

        form = FileForm(request.POST)

    if form is None: form = FileForm()
    upload_url = blobstore.create_upload_url('/media/upload/')
    return render_to_response('admin/upload.html', {'upload_url':upload_url,
													'upload_error': request.session.pop('upload_error', None),
													'form': form})
