#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import logging

import tornado.web
import tornado.ioloop

from database import Database
from util import PyStacheRenderer
from config import Config
from config import WebhandlerContext

from webhandler import ApiHandler

webhandlers = [
	(r"/api", ApiHandler.ApiHandler, {"context": None})
	#(r"/", MainHandler.MainHandler, {"context": ctx}),
	#(r"/logout", LogoutHandler.LogoutHandler, {"context": ctx}),
	#(r"/confirm", ConfirmHandler.ConfirmHandler, {"context": ctx}),
	#(r"/css/(.*\.css)", tornado.web.StaticFileHandler, {"path": "style"}),
	#(r"/js/(.*\.js)", tornado.web.StaticFileHandler, {"path": "javascript"}),
	#(r"/images/(.*)", tornado.web.StaticFileHandler, {'path': "./img"}),
	#(r"/(favicon.ico)", tornado.web.StaticFileHandler, {"path": "img/favicon"})
]

def start_webserver(config_path, database_path):

	# TODO: add logging destination path
	# TODO: check wether config_path is given
	cfg = Config.Config(config_path)
	dbs = Database.Database(database_path)
	rnd = PyStacheRenderer.PyStacheRenderer()
	log = logging.getLogger("internHHC")
	ctx = WebhandlerContext.WebhandlerContext(cfg, dbs, rnd, log)
	start_tornado(ctx)


def start_tornado(ctx):
	app = tornado.web.Application(webhandlers)
	app.listen(
		ctx.config.tornado["port"],
		address=ctx.config.tornado["host"]
	)

	print "Listening on localhost:%d..." % ctx.config.tornado["port"]
	try:
		tornado.ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
		pass
	print "Done."