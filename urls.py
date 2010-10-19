# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^foo/', include('foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),

	# serve static resources
	(r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),

	(r'^$', 'posts.views.stream'),
	(r'^posts/$', 'posts.views.listPost'),
    (r'^posts/category/([-\w]+)$', 'posts.views.listPostByCategory'),
    (r'^post/new/', 'posts.views.newPost'),
    (r'^post/(\d{4})/(\d{2})/(\d{2})/([-\w]+)', 'posts.views.showPost'),
    (r'^post/edit/(\d{4})/(\d{2})/(\d{2})/([-\w]+)', 'posts.views.editPost'),
    (r'^post/delete/(\d{4})/(\d{2})/(\d{2})/([-\w]+)', 'posts.views.delPost'),
)
