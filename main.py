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
import re
import logging
import time
from pytz import timezone
import pytz
from pytz import gae
from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class Food(db.Model):
    name = db.StringProperty()

class Report(db.Model):
	description = db.StringProperty()
	location = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add = True)
	user = db.UserProperty()

class Spotted(db.Model):
	food = db.ReferenceProperty(Food,
	                            required=False,
	                            collection_name="reports")
	report = db.ReferenceProperty(Report,
	                              required=False,
	                              collection_name="foods")

class AddFoodHandler(webapp.RequestHandler):
	def get(self):
		foods = ['Pizza', 'Cake', 'Cupcakes', 'Soda', 'Pancake']
		
		for food in foods:
			exists = Food.all().filter('name =', food).fetch(1)
			if len(exists) < 1:
				f = Food(name = food)
				f.put()
				self.response.out.write(f.name + " added <br>") 
			else:
				self.response.out.write(food + " already exists <br>") 
			

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
		
class LoginHandler(webapp.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			destination = re.search("/login(/.*)", self.request.uri)
			if destination:
				self.redirect(destination.group(1))
				
		template_values = basePrepPage(self.request)
		template_values["login_url"] = users.create_login_url(self.request.uri)

		path = templatePath('views/login.html')
		self.response.out.write(template.render(path,template_values))

def redirectToLoginIfNoUser(handler, destination):
	user = users.get_current_user()
	if not user:
		handler.redirect("/login/" + destination)

class ReportHandler(webapp.RequestHandler):
	def get(self):
		redirectToLoginIfNoUser(self, "report")
		
		template_values = basePrepPage(self.request)

		path = templatePath('views/report.html')
		self.response.out.write(template.render(path,template_values))
		
	def post(self):
		description = cgi.escape(self.request.get("description"))
		location = cgi.escape(self.request.get("location"))
		user = users.get_current_user()
		
		report = Report(description = description, 
		                location = location, 
		                user = user)
		report.put()
		
		selected_foods = cgi.escape(self.request.get("selected_foods"))

		ids = selected_foods.split(",")
		
		for i in ids:
			f = Food.get_by_id(int(i))
			s = Spotted(report = report, food = f)
			s.put()
		
		self.redirect("/find")
		
class FindHandler(webapp.RequestHandler):
    def get(self):
		destination = re.search("(find.*)", self.request.uri)
		redirectToLoginIfNoUser(self, destination.group(1))
	
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
		
class FoodsJSONHandler(webapp.RequestHandler):
    def get(self):
		query = self.request.query_string[2:].lower()
		
		foods = Food.all().order("name").fetch(1000)
		
		to_json = []
		
		for food in foods:
			if(query == "" or re.match(query, food.name.lower())):
				to_json.append({ "id" : food.key().id() , "name" : food.name})
		
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(simplejson.dumps(to_json))


def main():
	routes = [
	          ('/', MainHandler), 
	          ('/login/?.*', LoginHandler),
	          ('/report/?', ReportHandler),
              ('/find/?.*', FindHandler),
              ('/foods.json', FoodsJSONHandler),
              ('/add_food', AddFoodHandler)
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
