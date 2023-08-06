import sys
import string
import objectpath
import collections
import re
from types import GeneratorType
from tpljson.exceptions import TplException, TplUnmatched

OBJECT_TREE_PREDICATE = '$.'
REGEX_TYPE = type(re.compile(''))


class TplAbstract:

    _tree = None

    def _expire_tree(self):
        self._tree = None

    def _get_tree(self, template):
        if self._tree is None:
            if isinstance(template, dict):
                self._tree = objectpath.Tree(dict(template))
            else:
                self._tree = objectpath.Tree(list(template))
        return self._tree

    def _fmt_value(self, value, dict_state):
        # if the string has no other contents than the object-search path itself
        # simply assign the value of the search
        # otherwise, use the string formatting logic to resolve multiple template strings
        if '$.' not in value:
            return value
        if value.startswith('{') and value.lstrip('{').lstrip().startswith(OBJECT_TREE_PREDICATE) \
                and value.endswith('}') and value.count('$.') == 1:
            return self._fmt_assign(value, dict_state)
        else:
            return self._fmt_string(value, dict_state)

    def _fmt_assign(self, value: string, dict_state):
        """
        Reads a templated value (`{$.key}`) and returns the value pointed to by the template.

        :param value: A string template to read from
        :param dict_state: The current state of the dictionary/list as template values are applied.
        :return:
        """
        tree = self._get_tree(dict_state)
        search = value.lstrip('{').rstrip('}').strip()
        matched = tree.execute(search)
        if matched is None or isinstance(matched, REGEX_TYPE):
            excvalue = value.lstrip('{').rstrip('}').strip()
            raise TplUnmatched('Template value not matched: {}'.format(excvalue))
        if isinstance(matched, GeneratorType):
            matched = list(matched)
        self._expire_tree()
        return matched

    def _fmt_string(self, value, dict_state):
        """
        Format a string with values from the dictionary `dict_state`
        :param value:
        :param dict_state:
        :return:
        """
        fmt = TplStringFormatter(tree=self._get_tree(dict_state))
        try:
            result = fmt.vformat(value, args=[], kwargs=dict_state)
        except TplUnmatched as e:
            # add additional context to the traceback to help the user debug.
            msg = 'Failed formatting string "{}": {}'.format(value, e)
            raise type(e)(msg).with_traceback(sys.exc_info()[2])
        except Exception as e:
            raise TplException('Failed formatting string "{}": {}'.format(value, e)) from e
        self._expire_tree()
        return result

    def _format_dict(self, dictionary, template):
        # its required that the dictionary be modified in place.
        # this is only acceptable when you are not adding or removing keys
        for key in list(dictionary.keys()):
            value = dictionary[key]
            if isinstance(value, str):
                dictionary[key] = self._fmt_value(value, template)
            elif isinstance(value, (type(None), int, float, bool)):
                # value is scalar, just assign
                dictionary[key] = value
            else:
                dictionary[key] = self._render(value, template)

        return dictionary

    def _format_sequence(self, seq, template):
        # modify the list elements in-place
        for idx in range(len(seq)):
            value = seq[idx]
            if isinstance(value, str):
                seq[idx] = self._fmt_value(value, template)
            elif isinstance(value, (type(None), int, float, bool)):
                # value is scalar, just assign and return
                continue
            else:
                seq[idx] = self._render(value, template)

        return seq

    def _render(self, datum, template):
        if isinstance(datum, (dict, collections.OrderedDict)):
            return self._format_dict(datum, template or self)
        if isinstance(datum, (list, tuple, set)):
            return self._format_sequence(datum, template or self)
        else:
            return datum


class TplList(list, TplAbstract):
    """
    A python list that supports templating
    """
    def __init__(self, *args, template=None, **kwargs):
        super(TplList, self).__init__(*args, **kwargs)
        self._template = template
        self._render(self, self._template)

    def __repr__(self):
        listrepr = list.__repr__(self)
        return '%s(%s)' % (type(self).__name__, listrepr)


class TplDict(dict, TplAbstract):
    """
    A python dictionary that supports templating
    """
    def __init__(self, *args, template=None, **kwargs):
        super(TplDict, self).__init__(*args, **kwargs)
        self._template = template
        self._render(self, self._template)

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


class TplStringFormatter(string.Formatter):
    """
    Formatter designed to work with TplList and TplDict string template format
    """

    def __init__(self, tree):
        self._tree = tree

    def get_field(self, field_name, args, kwargs):
        if field_name.startswith(OBJECT_TREE_PREDICATE):
            return self._search_value(field_name, kwargs), field_name
        else:
            return super().get_field(field_name, args, kwargs)

    def _search_value(self, key, _):
        # parse the value from the dictionary
        matched = self._tree.execute(key)
        if matched is None or isinstance(matched, REGEX_TYPE):
            raise TplUnmatched('Template value not matched: {}'.format(key))
        if isinstance(matched, GeneratorType):
            matched = list(matched)
        return matched
