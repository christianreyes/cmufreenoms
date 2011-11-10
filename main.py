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


import cgi			# module for escaping out text
import datetime		# module for working with datetimes
import os			# module for working with the OS
import re			# module for regular expressions
import logging		# module for debugging and logging
import time			# module for working with time
from pytz import timezone	# module for working with timezones
import pytz					# module for working with timezones
from pytz import gae		# module for working with timezones in Google App Engine
from google.appengine.ext import db		# Google App Engine Datastore
from google.appengine.api import users	# Google App Engine User (Google Account)
from google.appengine.ext import webapp	# Google App Engine App
from google.appengine.ext.webapp import util		# Google App Engine App
from google.appengine.ext.webapp import template	# Django templates

###########################################################
# 						Models
###########################################################

# Model for Report
class Report(db.Model):
	description = db.StringProperty()
	location = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add = True) # automatically set date to now when created
	user = db.UserProperty() # Google Account User
				
###########################################################
# 						Helpers
###########################################################
			
# given a request for a page, check if the user is logged in.
# if yes, populate user_nickname and logout_url in template_values
# it not, populate login_url in template values
def basePrepPage(request):
	template_values = {}

	user = users.get_current_user()
	
	if user:
		template_values["user_nickname"] = user.nickname()
		template_values["logout_url"] = users.create_logout_url(request.uri)
	else: 
		template_values["login_url"] = users.create_login_url(request.uri)
		
	return template_values
	
# returns the absolute path from the relative path. needed for templates
def templatePath(path):
    return os.path.join(os.path.dirname(__file__), path)

# if no user is present, redirect to /login/destination .
def redirectToLoginIfNoUser(handler, destination):
	user = users.get_current_user()
	if not user:
		handler.redirect("/login/" + destination) # if no user, redirect to login
		
# Google App Engine does not store the timezone of datetimes. ALl are stored as "UTC".
# Datetimes must be converted back from "UTC" to "US/Eastern"
def fromUTC(date,tz):
    utc = pytz.timezone('UTC')
    d_tz = utc.normalize(date)
    localetime = d_tz.astimezone(tz)
    return localetime

###########################################################
# 						Handlers
###########################################################

# Handles requests to "/" 
class MainHandler(webapp.RequestHandler):
    def get(self):
		# determines if user is logged in. (user does not have to be to view page)
		template_values = basePrepPage(self.request)
		
		# use the home template (which extends base)
		path = templatePath('views/home.html')
		self.response.out.write(template.render(path,template_values))

# Handles requests to "/" 		
class LoginHandler(webapp.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			# /login/report -> /report is the destination
			destination = re.search("/login(/.*)", self.request.uri)
			if destination:
				self.redirect(destination.group(1)) #redirect to destination if there is one
			else:
				self.redirect("/") #if no destination and already logged in, redirect to home
		
		# prep page based on login
		template_values = basePrepPage(self.request)

		# use the login template (which extends base)
		path = templatePath('views/login.html')
		self.response.out.write(template.render(path,template_values))

# Handles requests to "/report" 		
class ReportHandler(webapp.RequestHandler):
	def get(self):
		redirectToLoginIfNoUser(self, "report") # if no user, redirect to "/login/report"
				
		# prep page based on login
		template_values = basePrepPage(self.request)

		# use the report template (which extends base)
		path = templatePath('views/report.html')
		self.response.out.write(template.render(path,template_values))
		
	# form sends a post request to "/report"
	def post(self):
		# escape the text in the fields
		description = cgi.escape(self.request.get("description"))	# description field from form
		location = cgi.escape(self.request.get("location"))			# location field from form
		user = users.get_current_user()								# logged in user
		
		# make a new report from the form data
		report = Report(description = description, 
		                location = location, 
		                user = user)
		report.put()
		
		# redirect user to the "/find" page after the report is saved
		self.redirect("/find")
		
# Handles requests to '/find/?.*'	e.g. '/find/pizza'
class FindHandler(webapp.RequestHandler):
	# user has the page bookmarked or is directly performing search by modifying url
    def get(self):
		destination = re.search("(find/?.*)", self.request.uri) # search for (find/.*) in the url
		redirectToLoginIfNoUser(self, destination.group(1))	   	# redirect to login if not logged in
	
		# prep page based on login
		template_values = basePrepPage(self.request)

		# only show reports from <= 24 hours ago
		twenty_four_hours =  datetime.datetime.now() - datetime.timedelta(days=1)
		reports = Report.all().filter('date >=', twenty_four_hours).order("-date").fetch(1000)
		
		# if there are reports <= 24 hours ago
		if reports:
			EST = timezone('US/Eastern')
			for report in reports:
				report.date = fromUTC(report.date.replace(tzinfo=EST), EST ) # transform date
	
		template_values["reports"] = reports

		# use the find template (which extends base)
		path = templatePath('views/find.html')
		self.response.out.write(template.render(path,template_values))

# Route for adding a "default" set of reports.
class AddDataHandler(webapp.RequestHandler):
	def get(self):
		descriptions = ["#brownies and #cookies for freshman",
		                "#pizza and #soda . All majors welcome",
		                "#candy and #ice_cream while watching movies",
		                "#hot_pockets and #smores"];
		locations = ["HCII Lounge",
		             "GHC 6615",
		             "PH 226B",
		             "UC Black Chairs"];
		times = [ datetime.datetime.now(),
		          datetime.datetime.now() - datetime.timedelta(hours=1),
		          datetime.datetime.now() - datetime.timedelta(hours=2),
				  datetime.datetime.now() - datetime.timedelta(hours=3)]
		
		for i in range(len(descriptions)):
			r = Report(description = descriptions[i],
                       location = locations[i],
                       date = times[i])
			r.put()
			self.response.out.write("<h3>Added report</h3>")
			self.response.out.write("<ul>") 
			self.response.out.write("	<li>Description: " + r.description + "</li>")
			self.response.out.write("	<li>Location: " + r.location + "</li>")
			self.response.out.write("	<li>Date: " + r.date.strftime("%b %d - %I:%M %p") + " UTC</li>")
			self.response.out.write("</ul>")
			self.response.out.write("<br>")

###########################################################
# 				  Google App Engine Main
###########################################################

def main():
	# routes that the application will handle
	routes = [
	          ('/', MainHandler), 			# "/"
	          ('/login/?.*', LoginHandler), # "/login", "/login/report", "/login/find/pizza"
	          ('/report/?', ReportHandler), # "/report"
              ('/find/?.*', FindHandler),	# "/find", "/find/pizza"
              ('/add_data', AddDataHandler)		 # "/add_food"
	         ]
	application = webapp.WSGIApplication(routes, debug=True)
	util.run_wsgi_app(application)
	
###########################################################
# 				    Python Engine Main
###########################################################
    
if __name__ == '__main__':
    main()
