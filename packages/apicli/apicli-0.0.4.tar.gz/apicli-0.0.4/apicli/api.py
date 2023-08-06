import logging
import tornado.web

from apicli.defaults import SERVER_HOST, SERVER_PORT, DEBUG_MODE


logger = logging.getLogger(__name__)


class ApiSpecs(tornado.web.RequestHandler):
    title = None
    description = None
    version = None
    address = None
    definitions = []

    @classmethod
    def set_address(cls, host, port):
        cls.address = 'http://{}{}/'.format(host, ':' + str(port) if port!=80 else '')

    @classmethod
    def set_models(cls, models):
        cls.definitions = {model.__name__: model.openapi_definition() for model in models}

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(self.json())

    def json(self):
        import json
        return json.dumps({
            "swagger": "2.0",
            "host": self.address,
            "schemes": ["https", "http"],
            "info": {
                "description": self.description,
                "version": self.version,
                "title": self.title
            },
            "definitions": self.definitions
        }, indent=4)


class API:
    def __init__(self, *, title, description, version='0.0.1'):
        self.specs = ApiSpecs

        self.specs.title = title
        self.specs.description = description
        self.specs.version = version
        self.specs.address = None

    def add_namespace(self, namespace):
        self.namespace = namespace

    def run(self, host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE):
        # configure api specs with bind address
        self.specs.set_address(host, port)
        self.specs.set_models(self.namespace.models)

        server = tornado.web.Application([
            (r'/swagger.json', ApiSpecs)
        ])
        server.listen(port=port, address=host)

        if DEBUG_MODE:
            logger.warning('Debug mode enabled')

        # log server address and start
        logger.info(
            'Tornado server listening on {} {}'.format(self.specs.address, 'in debug mode'*DEBUG_MODE))
        tornado.ioloop.IOLoop.current().start()
        