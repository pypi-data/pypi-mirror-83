import re


class Name:

    MINIMUM_ELEMENT_LENGTH = 2
    ELEMENT_SEPARATOR = '__'
    CLASS_SEPARATOR = '___'

    CAMEL_TO_SNAKE = r'(?<!^)(?=[A-Z])'
    SNAKE_TO_CAMEL = r'(.+?)_([a-z])'
    RE_CAMEL_TO_SNAKE = re.compile(CAMEL_TO_SNAKE)
    RE_SNAKE_TO_CAMEL = re.compile(SNAKE_TO_CAMEL)

    @classmethod
    def camel_to_snake(cls, camel):
        return cls.RE_CAMEL_TO_SNAKE.sub('_', camel).lower()

    @classmethod
    def snake_to_camel(cls, snake):
        # TODO: Implement regex instead
        return ''.join(x[0].upper() + x[1:] for x in
                       snake.split('_'))


class StubError(Exception):
    pass


class Stub:

    @classmethod
    def from_stub(cls, stub: str):
        raise StubError(f'Method from_stub() must be overridden in child '
                        f'class \'{cls.__name__}\'')

    def stub(self):
        raise StubError(f'Method stub() must be overridden in child '
                        f'class \'{type(self).__name__}')

