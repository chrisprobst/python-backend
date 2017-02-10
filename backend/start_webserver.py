#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import datetime
import logging
import os

import tornado.web
import tornado.ioloop

from database import Database
from config import Config
from config import WebhandlerContext

from webhandler.auth import GenerateApiTokenHandler
from webhandler.auth import DeleteApiTokenHandler
from webhandler.auth import DeleteAllApiTokensHandler
from webhandler.contact import CreateContactHandler
from webhandler.contact import SelectContactForIdHandler
from webhandler.contact import SelectAllContactsHandler
from webhandler.contact import UpdateContactHandler
from webhandler.contact import DeleteContactHandler


def setup_logger(log_path):
    logger = logging.getLogger("internHHC")
    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-8.8s]  %(message)s")
    log_streamhandler = logging.StreamHandler()
    log_streamhandler.setFormatter(log_formatter)
    logger.addHandler(log_streamhandler)
    logging.getLogger("tornado.access").addHandler(log_streamhandler)
    logging.getLogger("tornado.application").addHandler(log_streamhandler)
    logging.getLogger("tornado.general").addHandler(log_streamhandler)
    if log_path:
        log_filename = "{name}.log".format(name=datetime.datetime.now().isoformat())
        log_filepath = os.path.join(log_path, log_filename)
        log_filehandler = logging.FileHandler(log_filepath)
        log_filehandler.setFormatter(log_formatter)
        logger.addHandler(log_filehandler)
        logging.getLogger("tornado.access").addHandler(log_filehandler)
        logging.getLogger("tornado.application").addHandler(log_filehandler)
        logging.getLogger("tornado.general").addHandler(log_filehandler)
    return logger


def start_webserver(config_path, database_path, log_path):
    # TODO: check wether config_path is given
    logger = setup_logger(log_path)
    logger.info("Starting server...")
    cfg = Config.Config(config_path, logger)
    dbs = Database.Database(database_path, logger)
    ctx = WebhandlerContext.WebhandlerContext(cfg, dbs, logger)
    start_tornado(ctx)


# TODO: Based on the webhandler file structure the routes and respective classes could be loaded dynamically
def start_tornado(ctx):
    webhandlers = [
        (r"/api/auth/generateApiToken", GenerateApiTokenHandler.GenerateApiTokenHandler, {"context": ctx}),
        (r"/api/auth/deleteApiToken", DeleteApiTokenHandler.DeleteApiTokenHandler, {"context": ctx}),
        (r"/api/auth/deleteAllApiTokens", DeleteAllApiTokensHandler.DeleteAllApiTokensHandler, {"context": ctx}),
        (r"/api/contact/createContact", CreateContactHandler.CreateContactHandler, {"context": ctx}),
        (r"/api/contact/selectContactForId", SelectContactForIdHandler.SelectContactForIdHandler, {"context": ctx}),
        (r"/api/contact/selectAllContacts", SelectAllContactsHandler.SelectAllContactsHandler, {"context": ctx}),
        (r"/api/contact/updateContact", UpdateContactHandler.UpdateContactHandler, {"context": ctx}),
        (r"/api/contact/deleteContact", DeleteContactHandler.DeleteContactHandler, {"context": ctx}),
        # (r"/logout", LogoutHandler.LogoutHandler, {"context": ctx}),
        # (r"/confirm", ConfirmHandler.ConfirmHandler, {"context": ctx}),
        # (r"/(.*.png)", tornado.web.StaticFileHandler, {"path": "img/"})
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
