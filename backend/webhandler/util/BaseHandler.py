import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, context):
        self.context = context
