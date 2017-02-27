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
from webhandler.contact import SelectContactsBySearchHandler
from webhandler.contact import SelectFilterValuesHandler

stdout_log_format = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-8.8s]  %(message)s"
tornado_log_format = "%(asctime)s [Tornado     ] [%(levelname)-8.8s]  %(message)s"


def setup_logger(log_path):
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)
    stdout_formatter = logging.Formatter(stdout_log_format)
    tornado_formatter = logging.Formatter(tornado_log_format)
    log_streamhandler = logging.StreamHandler()
    log_streamhandler.setFormatter(stdout_formatter)
    log_tornado_streamhandler = logging.StreamHandler()
    log_tornado_streamhandler.setFormatter(tornado_formatter)
    logger.addHandler(log_streamhandler)
    logging.getLogger("tornado.access").addHandler(log_tornado_streamhandler)
    logging.getLogger("tornado.application").addHandler(log_tornado_streamhandler)
    logging.getLogger("tornado.general").addHandler(log_tornado_streamhandler)
    if log_path:
        log_filename = "{name}.log".format(name=datetime.datetime.now().isoformat())
        log_filepath = os.path.join(log_path, log_filename)
        log_filehandler = logging.FileHandler(log_filepath)
        log_filehandler.setFormatter(stdout_formatter)
        log_tornado_filehandler = logging.FileHandler(log_filepath)
        log_tornado_filehandler.setFormatter(tornado_formatter)
        logger.addHandler(log_filehandler)
        logging.getLogger("tornado.access").addHandler(log_tornado_filehandler)
        logging.getLogger("tornado.application").addHandler(log_tornado_filehandler)
        logging.getLogger("tornado.general").addHandler(log_tornado_filehandler)
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
        (r"/api/contact/selectContactsBySearch", SelectContactsBySearchHandler.SelectContactsBySearchHandler, {"context": ctx}),
        (r"/api/contact/selectFilterValues", SelectFilterValuesHandler.SelectFilterValuesHandler, {"context": ctx}),
        # (r"/logout", LogoutHandler.LogoutHandler, {"context": ctx}),
        # (r"/confirm", ConfirmHandler.ConfirmHandler, {"context": ctx}),
        # (r"/(.*.png)", tornado.web.StaticFileHandler, {"path": "img/"})
    ]
    for handler in webhandlers:
        ctx.logger.info("Setup route '{r}' for handler {h}".format(r=handler[0], h=handler[1].__name__))
    app = tornado.web.Application(webhandlers)
    host = ctx.config.tornado["host"]
    port = ctx.config.tornado["port"]
    app.listen(
        port,
        address=host
    )
    ctx.logger.info("Listen on {host}:{port}".format(host=host, port=port))
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass
    ctx.logger.info("Shut down webserver")
