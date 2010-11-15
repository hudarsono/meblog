from django.http import HttpResponseRedirect
from google.appengine.api import users

def login_required(func):
    def _wrapper(request, *args, **kw):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                return func(request, *args, **kw)
            else:
                return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
        else:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))

    return _wrapper

