import json
import simplejson
import yaml as YAML

from mjooln.core.name import Name
from mjooln.core.dic import Dic, DicError


class DocError(DicError):
    pass


class JSON:
    """Dict to/from JSON string, with optional human readable"""

    @classmethod
    def dumps(cls, dic, human=True, sort_keys=False, indent=4 * ' '):
        """Convert from dict to JSON string

        :param dic: Input dictionary
        :type dic: dict
        :param human: Human readable flag
        :param sort_keys: Sort key flag (human readable only)
        :param indent: Indent to use (human readable only)
        """
        if human:
            return simplejson.dumps(dic, sort_keys=sort_keys, indent=indent)
        else:
            return json.dumps(dic)

    @classmethod
    def loads(cls, json_string):
        """ Parse JSON string to dictionary

        :param json_string: JSON string
        :return: dict
        """
        return simplejson.loads(json_string)


class Dic:
    """Enables child classes to mirror attributes and dictionaries

    Private variables start with underscore, and are ignored by default.

    .. note:: Meant for inheritance and not direct use
    """

    # TODO: Consider moving ignore_private to a private class attribute
    # TODO: Consider deprecation. Or removing force equal/addonlyexisting.
    # TODO: Replace add and dic/doc with to_dict, from_dict, to_yaml etc
    # TODO: Require equal keys, except private.
    # Maybe even require equal keys if adding. I.e. only to be used for
    # configuration, or serialization
    _PRIVATE_STARTSWITH = '_'

    @classmethod
    def from_dict(cls,
                  data: dict):
        doc = cls()
        doc.add(data)
        return doc

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

    # @classmethod
    # def _from_strings(cls, dic):
    #     for key, item in dic.items():
    #         if isinstance(item, str):
    #             dic[key] = cls._parse_if_iso(item)
    #         elif isinstance(item, dict):
    #             dic[key] = cls._from_strings(item)
    #             if Atom.check(dic[key]):
    #                 dic[key] = Atom(**dic[key])
    #         elif isinstance(item, Dic):
    #             dic[key] = cls._from_strings(item.to_dict())
    #     return dic
    #
    # @classmethod
    # def _to_strings(cls, dic):
    #     for key, item in dic.items():
    #         if isinstance(item, Zulu):
    #             dic[key] = item.iso()
    #         elif isinstance(item, Identity):
    #             dic[key] = str(item)
    #         elif isinstance(item, Key):
    #             dic[key] = str(item)
    #         elif isinstance(item, Atom):
    #             dic[key] = cls._to_strings(vars(item))
    #         elif isinstance(item, dict):
    #             dic[key] = cls._to_strings(item)
    #         elif isinstance(item, Dic):
    #             dic[key] = cls._to_strings(item.to_dict())
    #     return dic

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


# TODO: Rewrite as serializer/deserializer
# TODO: In other words, doc will be dic with dates as strings.
# TODO: Atom can be builtin, otherwise it will be a bit tricky.
# TODO: SHould zulu/key/identity also be builtin?
class Doc(Dic):
    """ Enables child classes to mirror attributes, dictionaries and JSON
    strings

    Special cases:

    - Zulu objects will be converted to an ISO 8601 string before a dictionary
      is converted to JSON
    - ISO 8601 strings that are time zone aware with UTC, will be converted to
      Zulu objects after JSON document has been converted to a dictionary
    - Elements that are dictionaries with key names corresponding to Atom
      (key, zulu, identity), will be recognized and converted back to an Atom
      object after JSON document has been converted to a dictionary
    """

    @classmethod
    def from_doc(cls, doc: dict):
        """
        Override in child class to handle non serializable items

        :param doc: Dictionary with serializable items only
        :return: New Doc object instantiated with input dictionary
        :rtype: Doc
        """
        return cls.from_dict(doc)

    @classmethod
    def from_json(cls,
                  json_string: str):
        doc = JSON.loads(json_string=json_string)
        return cls.from_doc(doc)

    @classmethod
    def from_yaml(cls,
                  yaml_string: str):
        doc = YAML.safe_load(yaml_string)
        return cls.from_doc(doc)

    def to_dict(self,
                ignore_private: bool = True):
        """ Return dictionary with a copy of attributes

        :param ignore_private: Ignore private attributes flag
        :return: dict
        """
        doc = vars(self).copy()
        if ignore_private:
            pop_keys = [x for x in doc
                        if x.startswith(self._PRIVATE_STARTSWITH)]
            for key in pop_keys:
                doc.pop(key)
        return doc

    def to_doc(self,
               ignore_private: bool = True):
        doc = vars(self).copy()
        if ignore_private:
            pop_keys = [x for x in doc
                        if x.startswith(self._PRIVATE_STARTSWITH)]
            for key in pop_keys:
                doc.pop(key)
        for key, item in doc.items():
            if isinstance(item, Doc):
                doc[key] = item.to_doc(ignore_private=ignore_private)
        return doc

    def to_json(self,
                human_readable: bool = False,
                ignore_private: bool = True):
        doc = self.to_doc(ignore_private=ignore_private)
        return JSON.dumps(doc, human=human_readable)

    def to_yaml(self,
                ignore_private: bool = True):
        doc = self.to_doc(ignore_private=ignore_private)
        return YAML.safe_dump(doc)

