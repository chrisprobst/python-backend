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
from webhandler import GenerateApiTokenHandler
from webhandler import DeleteApiTokenHandler
from webhandler import DeleteAllApiTokensHandler
from webhandler import CreateContactHandler

def start_webserver(config_path, database_path):

	# TODO: add logging destination path
	# TODO: check wether config_path is given
	log = logging.getLogger("internHHC")
	cfg = Config.Config(config_path)
	dbs = Database.Database(
		database_path,
		debug=cfg.database_debug,
		logger=log
	)
	rnd = PyStacheRenderer.PyStacheRenderer()
	ctx = WebhandlerContext.WebhandlerContext(cfg, dbs, rnd, log)
	start_tornado(ctx)


def start_tornado(ctx):
	webhandlers = [
		(r"/api", ApiHandler.ApiHandler, {"context": ctx}),
		(r"/api/generateApiToken", GenerateApiTokenHandler.GenerateApiTokenHandler, {"context": ctx}),
		(r"/api/deleteApiToken", DeleteApiTokenHandler.DeleteApiTokenHandler, {"context": ctx}),
		(r"/api/deleteAllApiTokens", DeleteAllApiTokensHandler.DeleteAllApiTokensHandler, {"context": ctx}),
		(r"/api/createContact", CreateContactHandler.CreateContactHandler, {"context": ctx}),
		#(r"/logout", LogoutHandler.LogoutHandler, {"context": ctx}),
		#(r"/confirm", ConfirmHandler.ConfirmHandler, {"context": ctx}),
		#(r"/(favicon.ico)", tornado.web.StaticFileHandler, {"path": "img/favicon"})
	]
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