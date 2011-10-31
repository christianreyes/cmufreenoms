#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#

import os
import cgi
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class Report(db.Model):
    type = db.StringProperty()
    location = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)
	
class MainHandler(webapp.RequestHandler):
    def get(self):
		reports = Report.all().fetch(100)
	
		path = templatePath('views/index.html')
		template_values = {"reports": reports}
		self.response.out.write(template.render(path,template_values))

class ReportHandler(webapp.RequestHandler):
	def get(self):
		rtype = cgi.escape(self.request.get("type"))
		rlocation = cgi.escape(self.request.get("location"))
		
		report = Report(type = rtype, location = rlocation)
		report.put()

def main():
	routes = [
	          ('/', MainHandler), 
	          ('/report', ReportHandler)
	         ]
	application = webapp.WSGIApplication(routes, debug=True)
	util.run_wsgi_app(application)

def templatePath(path):
    return os.path.join(os.path.dirname(__file__), path)

if __name__ == '__main__':
    main()
