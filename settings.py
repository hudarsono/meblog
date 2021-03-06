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

# Django settings for google-app-engine-django project.

import os

if os.environ['SERVER_NAME'] == 'localhost':
    DEBUG = True
else:
    DEBUG = False
    
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'appengine'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'resources')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hvhxfm5u=^*v&doo#oq8x*eg8+1&9sxbye@=umutgn^t_sg_nx'

# Ensure that email is not sent via SMTP by default to match the standard App
# Engine SDK behaviour. If you want to sent email via SMTP then add the name of
# your mailserver here.
EMAIL_HOST = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'gaesessions.DjangoSessionMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.doc.XViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',

    # context processor to get all pages
    'context.context_processors.pages',
    
    # get addon settings
    'context.context_processors.addon',
    
    # get daily quote 
    'context.context_processors.daily_quote',
    
    # get mobile context
    'django_mobile.context_processors.flavour',

)

ROOT_URLCONF = 'urls'


TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
     # External Packages
     'appengine_django',
     'django_mobile',
     'markdown',
     'pygments',
     'gaesessions',
     
     # Meblog Packages
	 'posts',
     'pages',
     'context',
     'utilities',
)

# APP SETTINGS
APPNAME = 'your-appname'                               
BLOG_TITLE = 'your-blog-name'                      # This will show on header of the blog
SITE_URL = 'http://appname.appspot.com'       # Put AppEngine URL here
AUTHOR = 'your-name'                                # Put Your Name
AUTHOR_EMAIL = 'your-email'                         # Put Your Email, will be used to let user contact you from your blog
PAGESIZE = 10                                       # This is how many posts will show on home page

# Extension
DISQUS = 'False'      #Disquss is a comment system for blog.  http://disqus.com
ANALYTICS = 'False'    #Google analytics integration
FBLIKE = 'True'       #Facebook Like Button. Set this to True will enable fblike automatically on every post. No additional action required.

