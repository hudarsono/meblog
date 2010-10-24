# Create your views here.
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from google.appengine.ext import blobstore
import cgi
from models import Media
from fileform import FileForm


def get_uploads(request, field_name=None, populate_post=False):
    """Get uploads sent to this handler.
    Args:
      field_name: Only select uploads that were sent as a specific field.
      populate_post: Add the non blob fields to request.POST
    Returns:
      A list of BlobInfo records corresponding to each upload.
      Empty list if there are no blob-info records for field_name.
    """
    
    if hasattr(request,'__uploads') == False:
        request.META['wsgi.input'].seek(0)
        fields = cgi.FieldStorage(request.META['wsgi.input'], environ=request.META)
        
        request.__uploads = {}
        if populate_post:
            request.POST = {}
        
        for key in fields.keys():
            field = fields[key]
            if isinstance(field, cgi.FieldStorage) and 'blob-key' in field.type_options:
                request.__uploads.setdefault(key, []).append(blobstore.parse_blob_info(field))
            elif populate_post:
                request.POST[key] = field.value
    if field_name:
        try:
            return list(request.__uploads[field_name])
        except KeyError:
            return []
    else:
        results = []
        for uploads in request.__uploads.itervalues():
            results += uploads
        return results


def upload(request):
	form = None
	if request.method =='POST':
		media_blobs = get_uploads(request, field_name='media', populate_post=True)
		form = FileForm(request.POST)
		if form.is_valid() and len(media_blobs) == 1:
			media_item = Media(name=form.cleaned_data['name'],
								media=media_blobs[0])
			media_item.put()
			return HttpResponse('success')
		
		if len(media_blobs) == 0:
			request.session['upload_error'] = "Media file is required"
		
		form = FileForm(request.POST)
            
	if form is None: form = FileForm()
	upload_url = blobstore.create_upload_url('/media/upload')
	return render_to_response('admin/upload.html', {'upload_url':upload_url,
													'upload_error': request.session.pop('upload_error', None),
													'form': form})
