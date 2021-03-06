#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- This is the main web.py module.
- Everything starts here!
"""

import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)

import web
import urllib2
from lib.network.twitter import oauth as twitter_oauth
from lib.network.facebook import oauth as facebook_oauth
from lib.controller.network import oauth as oauth_controller

""" Setup urls. """
web.config.debug = False
urls = (
	"/rest/service.py/picproxy/(.+)", "pic_proxy",
	"/rest/service.py/oauthtwitter/(.+)", "oauth_twitter",
	"/rest/service.py/oauthfacebook/(.+)", "oauth_facebook",
)

""" Setup app and session. """
app = web.application(urls, globals(), autoreload=False)
session = web.session.Session(app, web.session.DiskStore('/tmp/3dfoo-sessions'), 
	initializer={
		# OAuth related params
		'oauth_network': '', 'oauth_token': '', 'oauth_token_secret': '',
		'network_user_id': '', 'network_user_name': ''
	}
)

class pic_proxy:
	""" Proxies images to avoid cross origin requests. """

	def GET(self, url):
		web.header('Content-Type','image', unique=True)

		url = url.replace('/', '//', 1)
		req = urllib2.Request(url)
		f = urllib2.urlopen(req)

		return f.read()

class oauth_twitter:
	""" Handles Twitter oauth requests. """

	def GET(self, step):
		web.header('Content-Type','text/html; charset=utf-8', unique=True)

		oauth_obj = twitter_oauth(session)
		oauth_ctr = oauth_controller(oauth_obj, step)
		return oauth_ctr.process()
			
class oauth_facebook:
	""" Handles Facebook oauth requests. """

	def GET(self, step):
		web.header('Content-Type','text/html; charset=utf-8', unique=True)
		
		oauth_obj = facebook_oauth(session)
		oauth_ctr = oauth_controller(oauth_obj, step)
		return oauth_ctr.process()

if __name__ == "__main__":
	web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
	app.run()
