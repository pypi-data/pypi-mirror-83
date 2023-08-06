import logging
from .route import create_route

logger = logging.getLogger(__name__)

class Namespace:
    def __init__(self, name):
        self.name = name
        self.models = []
        self.routes = []
    
    
    def model(self, cli=None, http=None):
        def declare_model(Model):
            logger.debug('Add model {} to namespace {}'.format(Model.__name__, self.name))
            self.models.append(Model)
        return declare_model
    

    def method(self, cli=None, http=None, method='get'):
        def declare_method(func):
            """
            Declare method func from the model defined by its class
            """
            logger.debug('declaring method %s'%func)

            if http is not None:
                # declare a new route in api
                print('/'+http)
                self.routes.append(
                    create_route(path='/'+http, callback=func, method=method))
        return declare_method

    def cli(self):
        pass
