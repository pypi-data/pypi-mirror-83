import logging
import string
import re

from mjooln.core.name import Name
from mjooln.core.seed import Seed
from mjooln.atom.element import Element, InvalidElement

logger = logging.getLogger(__name__)


class Key(str, Seed):
    f"""
    Defines key string with limitations

    - Minimum length is {Name.MINIMUM_ELEMENT_LENGTH}
    - Allowed characters are
        - Lower case ascii (a-z)
        - Digits (0-9)
        - Underscore (_)
        - Double underscore (__)
    - Underscore and digits can not be the first character
    - Underscore can not be the last character
    - The double underscore act as separator for groups in the key
    - Triple underscore is reserved for separating keys from other keys or
      strings, such as in class :class:`.Atom`

    Sample keys::

        'simple'
        'with_longer_name'
        'element_one__element_two__element_three'
        'digit1'
        'longer_digit2'
        'element1__element2__element3'
        'element_1__element_2__element_3'

    """

    ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + '_'
    ALLOWED_STARTSWITH = string.ascii_lowercase
    ALLOWED_ENDSWITH = string.ascii_lowercase + string.digits

    REGEX = rf'(?!.*{Name.CLASS_SEPARATOR}.*)[a-z][a-z_0-9]*[a-z0-9]'

    # #: Separates key from other keys or elements, such as identity and zulu
    # #: in Atom
    # OUTER_SEPARATOR = '___'
    #
    # #: Separates groups in key
    # SEPARATOR = '__'

    def __new__(cls,
                key: str):
        # TODO: Add list as input, creating key with separator
        cls.verify_key(key)
        instance = super(Key, cls).__new__(cls, key)
        return instance

    def __repr__(self):
        return f'Key(\'{self}\')'

    @classmethod
    def verify_key(cls, key: str):
        if not len(key) >= Name.MINIMUM_ELEMENT_LENGTH:
            raise InvalidKey(f'Key too short. Key \'{key}\' has length '
                             f'{len(key)}, while minimum length is '
                             f'{Name.MINIMUM_ELEMENT_LENGTH}')
        if Name.CLASS_SEPARATOR in key:
            raise InvalidKey(f'Key contains element reserved as class '
                             f'separator. '
                             f'Key \'{key}\' cannot contain '
                             f'\'{Name.CLASS_SEPARATOR}\'')
        if not key[0] in cls.ALLOWED_STARTSWITH:
            raise InvalidKey(f'Invalid startswith. Key \'{key}\' '
                             f'cannot start with \'{key[0]}\'. '
                             f'Allowed startswith characters are: '
                             f'{cls.ALLOWED_STARTSWITH}')

        elements = key.split(Name.ELEMENT_SEPARATOR)
        for element in elements:
            try:
                Element.verify_element(element)
            except InvalidElement as ee:
                raise InvalidKey(f'Error with element \'{element}\': {ee}') \
                    from ee

    def elements(self):
        """ Returns key parts as defined by separator (double underscore)

        Example::

            key = Key('some_key__with_two__no_three_elements')
            key.elements()
                ['some_key', 'with_two', 'three_elements']

        :returns: [str]
        """
        return [Element(x) for x in self.split(Name.ELEMENT_SEPARATOR)]

    def with_separator(self,
                       separator: str):
        """ Replace separator

        Example::

            key = Key('some__key_that_could_be__path')
            key.with_separator('/')
                'some/key_that_could_be/path'

        :param separator: Separator of choice
        :type separator: str
        :return: str
        """
        return separator.join(self.elements())

    @classmethod
    def elf(cls, key):
        """ Allows key class to pass through instead of throwing exception

        :param key: Input key string or key class
        :type key: str or Key
        :return: Key
        """
        if isinstance(key, Key):
            return key
        else:
            return cls(key)


class InvalidKey(Exception):
    pass
