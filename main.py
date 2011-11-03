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

import cgi
import datetime
import os
import time
from pytz import timezone
import pytz
from pytz import gae
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class Report(db.Model):
    type = db.StringProperty()
    location = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)

def basePrepPage(request):
	template_values = {}

	user = users.get_current_user()
	
	if user:
		template_values["user_nickname"] = user.nickname()
		template_values["logout_url"] = users.create_logout_url(request.uri)
	else: 
		template_values["login_url"] = users.create_login_url(request.uri)
		
	return template_values

class MainHandler(webapp.RequestHandler):
    def get(self):
		template_values = basePrepPage(self.request)
	
		path = templatePath('views/home.html')
		self.response.out.write(template.render(path,template_values))

class ReportHandler(webapp.RequestHandler):
	def get(self):
		template_values = basePrepPage(self.request)

		path = templatePath('views/report.html')
		self.response.out.write(template.render(path,template_values))
		
	def post(self):
		rtype = cgi.escape(self.request.get("type"))
		rlocation = cgi.escape(self.request.get("location"))
		
		report = Report(type = rtype, location = rlocation)
		report.put()
		self.redirect("/find")
		
class FindHandler(webapp.RequestHandler):
    def get(self):
		template_values = basePrepPage(self.request)

		twenty_four_hours =  datetime.datetime.now() - datetime.timedelta(days=1)
		reports = Report.all().filter('date >=', twenty_four_hours).order("-date").fetch(1000)

		if reports:
			for report in reports:
				EST = timezone('US/Eastern')
				report.date = fromUTC(report.date.replace(tzinfo=EST), 'US/Eastern' )
	
		template_values["reports"] = reports

		path = templatePath('views/find.html')
		self.response.out.write(template.render(path,template_values))

def main():
	routes = [
	          ('/', MainHandler), 
	          ('/report', ReportHandler),
              ('/find', FindHandler)
	         ]
	application = webapp.WSGIApplication(routes, debug=True)
	util.run_wsgi_app(application)

def templatePath(path):
    return os.path.join(os.path.dirname(__file__), path)
    
# "US/Eastern"
def toUTC(date,tz):
    tz = timezone(tz)
    utc = pytz.timezone('UTC')
    d_tz = tz.normalize(tz.localize(date))
    d_utc = d_tz.astimezone(utc)
    return d_utc

def fromUTC(date,tz):
    tz = timezone(tz)
    utc = pytz.timezone('UTC')
    d_tz = utc.normalize(date)
    localetime = d_tz.astimezone(tz)
    return localetime

def convert2EST(date, time, tzone):
    dt = datetime.datetime.strptime(date+time, '%Y%m%d%H:%M:%S')
    tz = pytz.timezone(tzone)
    dt = tz.localize(dt)
    return dt.astimezone(EST)
    
if __name__ == '__main__':
    main()
