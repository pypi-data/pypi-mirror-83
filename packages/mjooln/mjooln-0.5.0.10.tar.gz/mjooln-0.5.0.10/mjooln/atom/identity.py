import uuid
import re


class IdentityError(Exception):
    pass


class Identity(str):
    """ UUID string generator with convenience functions

    Inherits str, and is therefore an immutable string, with a fixed format
    as illustrated below.

    Examples::

        Identity()
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

        Identity.is_in('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            True

        Identity.find_one('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

    """

    _REGEX_STRING = r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}' \
                   r'\_[0-9A-F]{12}'
    _REGEX_STRING_EXACT = r'^' + _REGEX_STRING + r'$'
    _REGEX = re.compile(_REGEX_STRING)
    _REGEX_EXCACT = re.compile(_REGEX_STRING_EXACT)

    @classmethod
    def is_stub(cls,
                stub: str):
        """ Check if input text is an identity

        :type stub: str
        :return: bool
        """
        if cls._REGEX_EXCACT.match(stub):
            return True
        else:
            return False

    @classmethod
    def is_in(cls,
              text: str):
        """ Check if input text contains an identity

        :type text: str
        :return: bool
        """
        if cls._REGEX.search(text):
            return True
        else:
            return False

    @classmethod
    def find_one(cls,
                 text: str):
        """ Looks for and returns exactly one Identity from text

        Will fail if there are none or multiple identities.
        Use find_all() to return a list of identities in text, including
        an empty list if there are none.

        :type text: str
        :return: Identity
        """
        res = cls._REGEX.search(text)
        if res:
            return cls(res.group())
        else:
            raise IdentityError(f'No identity found in this text: {text}. '
                                f'Consider using find_all, which will return '
                                f'empty list if no identities are found.')

    @classmethod
    def find_all(cls,
                 text: str):
        """ Finds and returns all identities in text

        :type text: str
        :return: [Identity]
        """
        ids = re.findall(cls._REGEX_STRING, text)
        return [cls(x) for x in ids]

    @classmethod
    def _verify_string(cls, identity_string):
        if cls._REGEX.match(identity_string) is None:
            raise IdentityError(f'String is not a valid identity: '
                                f'{identity_string}')

    @classmethod
    def from_stub(cls,
                  stub: str):
        return cls(stub)

    def __new__(cls,
                identity: str = None):
        if not identity:
            identity = str(uuid.uuid4()).replace('-', '_').upper()
        else:
            cls._verify_string(identity)
        instance = super(Identity, cls).__new__(cls, identity)
        return instance

    def __repr__(self):
        return f'Identity(\'{self}\')'

    def stub(self):
        return self.__str__()

    @classmethod
    def elf(cls, identity):
        """ Returns new or existing identity

        None will create a new Identity, a string will be parsed as Identity,
        and an existing Identity will be returned as itself.

        :type identity: None, str or Identity
        :return: Identity
        """
        if isinstance(identity, Identity):
            return identity
        else:
            return cls(identity)

