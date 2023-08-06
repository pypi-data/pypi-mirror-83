import logging
import string

from mjooln.core.name import Name
from mjooln.core.seed import Seed

logger = logging.getLogger(__name__)


class InvalidElement(Exception):
    pass


class Element(str, Seed):
    """
    Defines element string with limitations

    - Minimum length is 3
    - Allowed characters are
        - Lower case ascii (a-z)
        - Digits (0-9)
        - Underscore (_)
    - Underscore and digits can not be the first character
    - Underscore can not be the last character
    - Can not contain double underscore since it acts as separator for elements
      in Key

    Sample elements::

        'simple'
        'with_longer_name'
        'digit1'
        'longer_digit2'

    """
    REGEX = r'(?!.*__.*)[a-z0-9][a-z_0-9]*[a-z0-9]'

    ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + '_'
    ALLOWED_STARTSWITH = string.ascii_lowercase + string.digits
    ALLOWED_ENDSWITH = string.ascii_lowercase + string.digits

    def __new__(cls,
                element: str):
        # TODO: Add list as input, creating key with separator
        cls.verify_element(element)
        self = super(Element, cls).__new__(cls, element)
        return self

    def __repr__(self):
        return f'Element(\'{self}\')'

    def stub(self):
        return self.__str__()

    @classmethod
    def from_stub(cls, stub: str):
        return cls(stub)

    @classmethod
    def verify_element(cls, element: str):
        if not len(element) >= Name.MINIMUM_ELEMENT_LENGTH:
            raise InvalidElement(
                f'Element too short. Element \'{element}\' has '
                f'length {len(element)}, while minimum length '
                f'is {Name.MINIMUM_ELEMENT_LENGTH}')
        if not element[0] in cls.ALLOWED_STARTSWITH:
            raise InvalidElement(f'Invalid startswith. Element \'{element}\' '
                                 f'cannot start with \'{element[0]}\'. '
                                 f'Allowed startswith characters are: '
                                 f'{cls.ALLOWED_STARTSWITH}')
        if not element[-1] in cls.ALLOWED_ENDSWITH:
            raise InvalidElement(f'Invalid endswith. Element \'{element}\' '
                                 f'cannot end with \'{element[-1]}\'. '
                                 f'Allowed endswith characters are: '
                                 f'{cls.ALLOWED_ENDSWITH}')
        invalid_characters = [x for x in element if x not in
                              cls.ALLOWED_CHARACTERS]
        if len(invalid_characters) > 0:
            raise InvalidElement(
                f'Invalid character(s). Element \'{element}\' cannot '
                f'contain any of {invalid_characters}. '
                f'Allowed characters are: '
                f'{cls.ALLOWED_CHARACTERS}')
        if Name.ELEMENT_SEPARATOR in element:
            raise InvalidElement(
                f'Element contains element separator, which is '
                f'reserved for separating Elements in a Key.'
                f'Element \'{element}\' cannot contain '
                f'\'{Name.CLASS_SEPARATOR}\'')

    @classmethod
    def elf(cls, element):
        """ Allows key class to pass through instead of throwing exception

        :param element: Input element string or element class
        :type element: str or Element
        :return: Element
        """
        # TODO: Handle input and guess a conversion that would match criteria
        if isinstance(element, Element):
            return element
        else:
            return cls(element)
