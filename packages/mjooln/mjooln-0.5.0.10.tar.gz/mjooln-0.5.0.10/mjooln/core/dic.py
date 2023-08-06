from mjooln.core.name import Name


class DicError(Exception):
    pass


class Dic:
    """
    Enables child classes to mirror attributes and dictionaries

    Private variables start with underscore, and are ignored by default.

    .. note:: Meant for inheritance and not direct use
    """

    # TODO: Consider moving ignore_private to a private class attribute
    # TODO: Consider deprecation. Or removing force equal/addonlyexisting.
    # TODO: Require equal keys, except private.
    # Maybe even require equal keys if adding. I.e. only to be used for
    # configuration, or serialization
    _PRIVATE_STARTSWITH = '_'

    @classmethod
    def from_dict(cls,
                  data: dict):
        return cls(**data)

    @classmethod
    def default(cls):
        return cls()

    @classmethod
    def default_dict(cls):
        dic = cls.default()
        return dic.to_dict()

    def to_vars(self):
        return vars(self).copy()

    def __repr__(self):
        dic = self.to_vars()
        dicstr = []
        for key, item in dic.items():
            dicstr.append(f'{key}={item.__repr__()}')
        dicstr = ', '.join(dicstr)
        return f'{type(self).__name__}({dicstr})'

    def to_dict(self,
                ignore_private: bool = True):
        """ Return dictionary with a copy of attributes

        :param ignore_private: Ignore private attributes flag
        :return: dict
        """
        dic = self.to_vars()
        if ignore_private:
            pop_keys = [x for x in dic
                        if x.startswith(self._PRIVATE_STARTSWITH)]
            for key in pop_keys:
                dic.pop(key)
        for key, item in dic.items():
            if isinstance(item, Dic):
                dic[key] = item.to_dict(ignore_private=ignore_private)
        return dic

    def _add_item(self, key, item, ignore_private=True):
        # Add item and ignore private items if ignore_private is set to True
        if not ignore_private or not key.startswith(self._PRIVATE_STARTSWITH):
            self.__setattr__(key, item)

    def _add_dic(self,
                 dic: dict,
                 ignore_private: bool = True):
        for key, item in dic.items():
            self._add_item(key, item, ignore_private=ignore_private)

    def add(self,
            dic: dict,
            ignore_private: bool = True):
        """ Add dictionary to class as attributes

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        self._add_dic(dic, ignore_private=ignore_private)

    def add_only_existing(self, dic, ignore_private=True):
        """ Add dictionary keys and items as attributes if they already exist
        as attributes

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        dic_to_add = {}
        for key in dic:
            if hasattr(self, key):
                dic_to_add[key] = dic[key]
        self._add_dic(dic_to_add, ignore_private=ignore_private)

    def force_equal(self, dic, ignore_private=True):
        """ Add all dictionary keys and items as attributes in object, and
        delete existing attributes that are not keys in the input dictionary

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        self._add_dic(dic, ignore_private=ignore_private)
        for key in self.to_dict(ignore_private=ignore_private):
            if key not in dic:
                self.__delattr__(key)

    def print(self,
              ignore_private=True,
              indent=4*' ',
              width=80,
              flatten=False,
              separator=Name.ELEMENT_SEPARATOR):
        # TODO: Rename dev_print to print (print goes to terminal inherently)
        """ Pretty print of attributes in terminal meant for development
        purposes
        """
        text = f'--{indent}[[ {type(self).__name__} ]]{indent}'
        text += (width-len(text)) * '-'
        print(text)
        if not flatten:
            dic = self.to_dict(ignore_private=ignore_private)
        else:
            dic = self.flatten(sep=separator)
        self._print(dic, level=0)
        print(width*'-')

    def _print(self, dic, level=0, indent=4 * ' '):
        for key, item in dic.items():
            if isinstance(item, dict):
                self._print(item, level=level + 1)
            else:
                print(level*indent + f'{key}: [{type(item).__name__}] {item} ')

    def print_flat(self,
                   ignore_private=True,
                   separator=Name.ELEMENT_SEPARATOR):
        self.print(ignore_private=ignore_private,
                   separator=separator, flatten=True)

    # TODO: Move to flag in to_dict etc., and unflatten in from_dict etc
    # TODO: Replace sep with Key sep.
    # TODO: Require var names not to have double underscores
    # TODO: Figure out how to handle __vars__, what is the difference with _vars
    def flatten(self, sep=Name.ELEMENT_SEPARATOR, ignore_private=True):
        """
        Flatten dictionary to top level only by combining keys with the
        given separator

        :param sep: Separator to use, default is double underscore (__)
        :type sep: str
        :param ignore_private: Flags whether to ignore private attributes,
            identified by starting with underscore
        :return: Flattened dictionary
        :rtype: dict
        """
        dic = self.to_dict(ignore_private=ignore_private)
        flat_dic = dict()
        flat_dic = self._flatten(flat_dic=flat_dic, parent_key='',
                                 dic=dic, sep=sep)
        return flat_dic

    def _flatten(self,
                 flat_dic, parent_key, dic, sep=Name.ELEMENT_SEPARATOR):
        for key, item in dic.items():
            if isinstance(item, dict):
                flat_dic = self._flatten(flat_dic=flat_dic, parent_key=key,
                                         dic=item, sep=sep)
            else:
                if sep in key:
                    raise DicError(f'Separator \'{sep}\' found in '
                                   f'key: {key}')
                if parent_key:
                    flat_dic[parent_key + sep + key] = item
                else:
                    flat_dic[key] = item
        return flat_dic
