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

from google.appengine.ext import db

class Widget(db.Model):
    title = db.StringProperty()
    body = db.StringProperty()
    enabled = db.BooleanProperty()
    
    def get_edit_url(self):
        return '/widget/edit/%s' % str(self.key())
    
    def get_delete_url(self):
        return '/widget/delete/%s' % str(self.key())