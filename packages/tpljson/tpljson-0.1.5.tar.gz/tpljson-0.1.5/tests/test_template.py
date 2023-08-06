"""
Tests for `template` module in tpljson
"""
import unittest
from collections import OrderedDict

import pytest

from tpljson.exceptions import TplUnmatched, TplException
from tpljson.template import TplDict, TplList


class TestTemplateList(unittest.TestCase):
    def test_single_variable_list(self):
        l = TplList(['one', '{$.*[0]}', 'three'])
        self.assertListEqual(l, ['one', 'one', 'three'])

    def test_repr(self):
        l = TplList(['one', '{$.*[0]}', 'three'])
        self.assertEqual(repr(l), "TplList(['one', 'one', 'three'])")


class TestTemplateDict(unittest.TestCase):

    def test_single_variable_dict(self):
        d = TplDict({'one': 1, 'two': '{$.one}', 'three': 3})
        self.assertDictEqual(d, {'one': 1, 'two': 1, 'three': 3})

    def test_repr(self):
        d = TplDict({'one': 1, 'two': '{$.one}', 'three': 3})
        self.assertEqual(repr(d), "TplDict({'one': 1, 'two': 1, 'three': 3})")

    def test_update(self):
        d = TplDict({'one': 1, 'two': '{$.one}', 'three': 3})
        d.update({'two': 2, 'four': 4})
        self.assertDictEqual(d, {'one': 1, 'two': 2, 'three': 3, 'four': 4})

    def test_multi_variable(self):
        d = TplDict({'one': 1, 'two': '{$.one}', 'three': 3, 'four': '{$.three}'})
        self.assertDictEqual(d, {'one': 1, 'two': 1, 'three': 3, 'four': 3})

    def test_nested(self):
        d = TplDict({
            'one': {
                'first': 'a',
                'second': 'b',
                'third': 'c'
            },
            'two': {
                'top': '{$.one.first}',
                'last': '{$.one.third}'
            }
        })
        self.assertDictEqual(d, {
            'one': {
                'first': 'a',
                'second': 'b',
                'third': 'c'
            },
            'two': {
                'top': 'a',
                'last': 'c'
            }
        })

    def test_multi_variable_dependency(self):
        d = TplDict(OrderedDict([('one', 1), ('two', '{$.one}'), ('three', 3), ('four', '{$.two}')]))
        self.assertDictEqual(d, {'one': 1, 'two': 1, 'three': 3, 'four': 1})

    def test_multi_string_var(self):
        d = TplDict(OrderedDict([
            ('first_name', 'Peter'),
            ('last_name', 'Henderson'),
            ('phone', '3338675309'),
            ('email', '{$.first_name}.{$.last_name}@example.org'),
            ('contact', '{$.first_name} {$.last_name}\nCell: {$.phone}\nEmail: {$.email}')
        ]))
        self.assertDictEqual(d, {
            'first_name': 'Peter',
            'last_name': 'Henderson',
            'phone': '3338675309',
            'email': 'Peter.Henderson@example.org',
            'contact': 'Peter Henderson\nCell: 3338675309\nEmail: Peter.Henderson@example.org'
        })

    def test_variable_order(self):
        # TODO test exception for when the ordered of the data structure is not defined correctly.
        pass

    def test_template_vars_order(self):
        template = OrderedDict([
            ('first_name', 'Peter'),
            ('last_name', 'Henderson'),
            ('phone', '3338675309'),
        ])
        d = TplDict(OrderedDict([
            ('contact', '{$.first_name} {$.last_name}\nCell: {$.phone}'),
        ]), template=template)

        self.assertDictEqual(d, {
            'contact': 'Peter Henderson\nCell: 3338675309'
        })


class TestTemplateEdgeCases(unittest.TestCase):

    def test_unmatched(self):
        with pytest.raises(TplUnmatched) as excinfo:
            d = TplDict({'two': '{$.one}', 'three': 3})

        self.assertIn('Template value not matched: $.one', str(excinfo.value))

    def test_unmatched_template_string(self):
        with pytest.raises(TplUnmatched) as excinfo:
            d = TplDict({'two': 'xyz {$.one}', 'three': 3})

        self.assertIn('Failed formatting string "xyz {$.one}": Template value not matched: $.one', str(excinfo.value))

    def test_invalid_template_string(self):
        with pytest.raises(TplException) as excinfo:
            d = TplDict({'two': 'xyz {$.one!%5}}', 'three': 3})

        self.assertIn('Failed formatting string', str(excinfo.value))

    def test_whitespace(self):
        d = TplDict({'one': 1, 'two': '{   $.one }', 'three': 3})
        self.assertDictEqual(d, {'one': 1, 'two': 1, 'three': 3})

    def test_format_template(self):
        # jsontpl should ignore normal format strings {myvar}
        d = TplDict({'one': 1, 'two': '{   $.one}', 'three': 3, 'ignore': '{asdf} by {xyz}'})
        self.assertDictEqual(d, {'one': 1, 'two': 1, 'three': 3, 'ignore': '{asdf} by {xyz}'})

    def test_resolve_generator(self):
        def gen():
            yield 1
            yield 2
            yield 3

        d = TplDict({'one': gen(), 'two': '{$.one}'})
        self.assertListEqual(d['two'], [1, 2, 3])

    def test_generator_in_string(self):
        # if for some reason you choose to embed a generator in a string it will
        # embed the string representation of a list.
        def gen():
            yield 'a'
            yield 'b'

        d = TplDict({'one': gen(), 'two': 'asdf {$.one}'})
        self.assertEqual(d['two'], "asdf ['a', 'b']")