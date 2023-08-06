import tornado.web

def create_route(path:str, callback, method='get'):
    name = method.title() + 'Handler' + path.title().replace('/', '')
    print(name)
    return type(
        name, 
        (tornado.web.RequestHandler,), 
        {method: callback})
