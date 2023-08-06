import apicli.fields

class Model:
    """Base object that can be serialized/deserialized
    """

    def load(self):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    @classmethod
    def openapi_definition(cls):
        # list model fields
        properties = [prop for prop in dir(cls) if isinstance(getattr(cls, prop), apicli.fields.Field)]

        return {
            'type': 'object',
            'properties': {
                prop: getattr(cls, prop).specs() for prop in properties
            }
        }
