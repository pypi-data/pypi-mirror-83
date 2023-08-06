"""
Templated JSON and Dictionary library

See https://github.com/vaidik/commentjson/blob/master/commentjson/commentjson.py as reference
"""
# TODO support enabling/disabling comment_json

__all__ = ['load', 'loads', 'dump', 'dumps']

import collections
import io
import json

from tpljson.template import TplDict, TplList
from tpljson.text import preview_text, highlight_text

from commentjson.commentjson import serializer, detect_encoding, parser
import lark
from lark.lexer import Token
from lark.tree import Tree

from colorama import init
from colorama import Fore, Back

init()

_ALLOW_COMMENTS = True
_PREVIEW_CHARS = 1000
_DEFAULT_COLORED = True
_DEFAULT_COMMENTS = True


def _read_template(template, **kwargs):
    """
    When reading a JSON object an optional "template" argument may be specified.
    This "template" argument must be a valid JSON object, JSON string, dictionary or list.

    The template is then passed into the TplDict or TplList object to be used as the source of template
    lookup values instead of referencing itself.

    :param template: A json string, or dict or list, or file-object (of a json string)
    :type template: None, str, dict, list, io.IOBase
    :param kwargs: all the arguments that `json.loads <http://docs.python.org/
                   2/library/json.html#json.loads>`_ accepts.
    :return:
    """
    if template is None:
        return

    if isinstance(template, (bytes, bytearray)):
        template = template.decode(detect_encoding(template), 'surrogatepass')

    if isinstance(template, str):
        template = loads(template, **kwargs)
    elif isinstance(template, (dict, list)):
        pass
    elif isinstance(template, io.IOBase):
        template = loads(template.read(), **kwargs)
    else:
        raise TypeError('"template" argument unsupported type: {}, '
                        'must be one of [None, bytes, str, dict, list, io.IOBase]'.format(type(template)))
    return template


def _loads(text=None, fp=None, template=None, colored=None, comments=None, **kwargs):
    """
    Deserialize `text` (a `str` or `unicode` instance containing a JSON
    document supporting template references `{$.key}`) to a Python object.

    :param text: serialized JSON string
    :param template: (optional) None, str, dict, list, io.IOBase - Causes template values to be sourced form this object
    :param kwargs: all the arguments that `json.loads <http://docs.python.org/
                   2/library/json.html#json.loads>`_ accepts.
    :returns: dict or list.
    """
    kwargs['object_pairs_hook'] = collections.OrderedDict
    template = _read_template(template, **kwargs)

    if colored is None:
        colored = _DEFAULT_COLORED
    if comments is None:
        comments = _DEFAULT_COMMENTS

    if isinstance(text, (bytes, bytearray)):
        text = text.decode(detect_encoding(text), 'surrogatepass')

    if fp is not None:
        fp.seek(0)
        text = fp.read()

        fp_desc = getattr(fp, 'name', type(fp).__name__)
        if colored:
            fp_desc = highlight_text(fp_desc, fg=Fore.LIGHTBLUE_EX, bg=Back.RESET)
        obj_desc = 'JSON File/Stream ({})'.format(fp_desc)
    else:
        obj_desc = 'JSON String'
        # test for empty string to preserve similarity to built-in `json` module
        if not text.strip():
             raise json.JSONDecodeError('Expecting value - cannot parse empty {}'.format(obj_desc), text, 0)

    try:
        if comments:
            datum = _commentjson_loads(text, **kwargs)
        else:
            datum = json.loads(text, **kwargs)

    except lark.exceptions.UnexpectedEOF as e:
        last_line_pos = len(text) + 1
        for i in range(100):
            last_line_pos = text.rfind('\n', 0, last_line_pos)

            if text[last_line_pos:].strip() or last_line_pos < 1:
                break

        lineno = text.count('\n', 0, last_line_pos) + 1

        sample = preview_text(text,
                              max_chars=_PREVIEW_CHARS,
                              center_line=lineno,
                              highlight=lineno,
                              prefix='NEAR:\n',
                              suffix='\n...\n\nTOTAL LENGTH: {} chars'.format(len(text)),
                              colored=colored)
        error_desc = 'Error Decoding {} - Incomplete Document'.format(obj_desc)
        msg = '{}\n{}\n\nError at'.format(error_desc, sample)
        raise json.JSONDecodeError(msg, doc=text, pos=last_line_pos)

    except (lark.UnexpectedCharacters, lark.UnexpectedToken) as e:
        # handle exception from Lark parser (used for commentjson)
        sample = preview_text(text,
                              max_chars=_PREVIEW_CHARS,
                              center_line=e.line,
                              highlight=e.line,
                              prefix='NEAR:\n',
                              suffix='\n...\n\nTOTAL LENGTH: {} chars'.format(len(text)),
                              colored=colored)
        error_desc = 'Error Decoding {} - Unexpected Character\n{}'.format(obj_desc, e.get_context(text))
        msg = '{}\n{}\n\nError at'.format(error_desc, sample)
        raise json.JSONDecodeError(msg, doc=text, pos=e.pos_in_stream)

    except json.JSONDecodeError as e:
        sample = preview_text(text,
                              max_chars=_PREVIEW_CHARS,
                              center_line=e.lineno,
                              highlight=e.lineno,
                              prefix='NEAR:\n',
                              suffix='\n...\n\nTOTAL LENGTH: {} chars'.format(len(text)),
                              colored=colored)
        msg = '{} in {}\n{}\n\nError at'.format(e.msg, obj_desc, sample)

        # raise an exception similar to the built-in
        raise json.JSONDecodeError(msg, doc=e.doc, pos=e.pos) from None
    if isinstance(datum, dict):
        return TplDict(datum, template=template)
    elif isinstance(datum, list):
        return TplList(datum, template=template)
    else:
        return datum


def loads(text, template=None, colored=None, comments=None, **kwargs):
    """
    Deserialize `text` (a `str` or `unicode` instance containing a JSON
    document supporting template references `{$.key}`) to a Python object.

    :param text: serialized JSON string
    :type text: str
    :param template: (optional) None, str, dict, list, io.IOBase - Causes template values to be sourced form this object
    :type template: dict
    :type template: list
    :param kwargs: all the arguments that `json.loads <http://docs.python.org/
                   2/library/json.html#json.loads>`_ accepts.
    :returns: dict or list.
    # TODO update docstring
    """
    if not isinstance(text, (str, bytes, bytearray)):
        # just use the default json library to raise the normal error (TypeError)
        json.loads(text)

    return _loads(text=text, template=template, colored=colored, comments=comments, **kwargs)


def load(fp, template=None, colored=None, comments=None, **kwargs):
    """
    Deserialize `fp` (a `.read()`-supporting file-like object containing a
    JSON document supporting template references `{$.key}`) to a Python object.

    Note that when passing `template`

    :param fp: a `.read()`-supporting file-like object
    :param template: (optional) None, str, dict, list, io.IOBase - Causes template values to be sourced form this object
    :param kwargs: all the arguments that `json.load <http://docs.python.org/
                   3/library/json.html#json.load>`_ accepts.
    :raises: tpljson.JSONLibraryException
    :returns: dict or list.
    # TODO update docstring
    """
    if not isinstance(fp, io.IOBase):
        raise TypeError('first argument must be file-type (IOBase) got: {}'.format(type(fp)))

    return _loads(fp=fp, template=template, colored=colored, comments=comments, **kwargs)


def dumps(obj, **kwargs):
    """
    Serialize `obj` to a JSON formatted `str`. Accepts the same arguments
    as `json` module in stdlib.
    :param obj: a JSON serializable Python object.
    :param kwargs: all the arguments that `json.dumps <http://docs.python.org/
                   3/library/json.html#json.dumps>`_ accepts.
    :raises: tpljson.JSONLibraryException
    :returns str: serialized string.

    :param obj:
    :param kwargs:
    :return:
    """
    return json.dumps(obj, **kwargs)


def dump(obj, fp, **kwargs):
    """
    Serialize `obj` as a JSON formatted stream to `fp` (a
    `.write()`-supporting file-like object). Accepts the same arguments as
    `json` module in stdlib.

    :param obj: a JSON serializable Python object.
    :param fp: a `.read()`-supporting file-like object containing a JSON
               document with or without comments.
    :param kwargs: all the arguments that `json.dump <http://docs.python.org/
                   2/library/json.html#json.dump>`_ accepts.
    """
    if not isinstance(fp, io.IOBase):
        raise TypeError('second argument must be file-type (IOBase) got: {}'.format(type(fp)))

    return json.dump(obj, fp, **kwargs)


def _remove_trailing_commas(tree):
    """
    borrowed from commentjson project
    """
    if isinstance(tree, Tree):
        tree.children = [
            _remove_trailing_commas(ch) for ch in tree.children
                if not (isinstance(ch, Token) and ch.type == 'TRAILING_COMMA')
        ]
    return tree


def _commentjson_loads(text, *args, **kwargs):
    """
    Load json string using comment json.

    We re-implement the internal calls that compose commentjson `loads` method to issue better exceptions
    and avoid redundant checks and decoding.

    :param text: json string to decode into Python object.
    :type text: str
    :param args: `json.loads` arguments
    :param kwargs: `json.loads` keyword arguments
    :return:
    """
    parsed = _remove_trailing_commas(parser.parse(text))
    final_text = serializer.reconstruct(parsed)

    return json.loads(final_text, *args, **kwargs)