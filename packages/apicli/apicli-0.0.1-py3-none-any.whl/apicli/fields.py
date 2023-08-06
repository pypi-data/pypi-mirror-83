
class Field:
    def __init__(self, *, type, format=None, example=None, required=False):
        self.required = required
        self.type = type
        self.format = format
        self.example = example

    def specs(self):
        _specs = {'type': self.type}
        if self.format:
            _specs['format'] = self.format
        if self.example:
            _specs['example'] = self.example
        return _specs


class String(Field):
    def __init__(self, required=False, format=None, example=None):
        super().__init__(required=required, type='string', format=format, example=example)


class Email(String):
    def __init__(self, required=False, format='email', example='toto@example.com'):
        super().__init__(required=required, format=format, example=example)


class Password(Field):
    def __init__(self, required=False, default=None, format=None, example=None):
        super().__init__(required=required, type='string', format='string', example=example)
