"""
Test main functionality `tpljson`
"""

import pytest
import unittest
from io import StringIO
from tpljson import loads, load, dumps, dump
import json


class TestJsonFunctionality(unittest.TestCase):
    """Test basic json functionality"""

    input1, result1 = ('{"one": 1, "two": "two", "l": [1,2,3]}', {'one': 1, 'two': 'two', 'l': [1, 2, 3]})
    input2, result2 = ('[{"one": 1, "two": "two", "l": [1,2,3]}, 2]', [{'one': 1, 'two': 'two', 'l': [1, 2, 3]}, 2])
    input3 = '''
    // comment1
    # comment2
    {
        "one": 1, # comment 2
        "two": "two" # comment 3
    }
    '''
    result3 = {'one': 1, 'two': 'two'}

    dump1, string1 = ({'one': 1}, '{"one": 1}')

    def test_dict_loads(self):
        for enabled in (True, False):
            j = loads(self.input1, comments=enabled)
            self.assertDictEqual(j, self.result1)

    def test_list_loads(self):
        for enabled in (True, False):
            j = loads(self.input2, comments=enabled)
            self.assertListEqual(j, self.result2)

    def test_dict_load(self):
        for enabled in (True, False):
            j = load(StringIO(self.input1), comments=enabled)
            self.assertDictEqual(j, self.result1)

    def test_list_load(self):
        for enabled in (True, False):
            j = load(StringIO(self.input2), comments=enabled)
            self.assertListEqual(j, self.result2)

    def test_comment_load(self):
        # ensure comment functionality works
        j = loads(self.input3, comments=True)
        self.assertDictEqual(j, self.result3)

    def test_dumps(self):
        j = dumps(self.dump1)
        self.assertEqual(j.strip(), self.string1.strip())

    def test_dump(self):
        fp = StringIO('')
        dump(self.dump1, fp)
        fp.seek(0)
        self.assertEqual(fp.read().strip(), self.string1.strip())

    def test_scalar(self):
        # the json library allows raw scalar values... ensure this functionality is preserved.
        j = loads('1')
        self.assertEqual(j, 1)

        j = loads('"a"')
        self.assertEqual(j, "a")

    def test_bytes(self):
        j = loads(b'{}')
        self.assertDictEqual(j, {})


class TestJsonTemplating(unittest.TestCase):
    """Test json functionality when templating is used"""

    def test_variable_dict(self):
        j = loads('''{
            "one": 1,
            "abc": "{$.one}"
        }''')

        self.assertDictEqual(j, {'one': 1, 'abc': 1})

    def test_variable_list(self):
        j = loads('''[
            {"one": 1},
            {"abc": "{$.*[0].one}"}
        ]''')

        self.assertListEqual(j, [{'one': 1}, {'abc': 1}])

    def test_template_dict(self):
        j = loads('''{
            "abc": "{$.one}"
        }''', template={'one': 1})

        self.assertDictEqual(j, {'abc': 1})

    def test_template_list(self):
        j = loads('''[
            {"abc": "{$.*[0].one}"}
        ]''', template=[{'one': 1}])

        self.assertListEqual(j, [{'abc': 1}])

    def test_template_str(self):
        j = loads('''[
            {"abc": "{$.*[0].one}"}
        ]''', template='[{"one": 1}]')

        self.assertListEqual(j, [{'abc': 1}])

    def test_template_bytes(self):
        j = loads('''{
            "abc": "{$.one}"
        }''', template=b'{"one": 1}')

        self.assertDictEqual(j, {'abc': 1})

    def test_template_file(self):
        j = loads('''[
            {"abc": "{$.*[0].one}"}
        ]''', template=StringIO('[{"one": 1}]'))

        self.assertListEqual(j, [{'abc': 1}])


class TestJsonExceptions(unittest.TestCase):
    """Test json functionality when templating is used"""
    bad_json1 = '''
        {
            "a": 1,
            "b": 2,
            "c": 'asdf'
        }
    '''
    err_msg1 = '''Expecting value in JSON String
NEAR:
            {
                "a": 1,
                "b": 2,
            >>  "c": 'asdf'  <<
            }
...

TOTAL LENGTH: 89 chars

Error at: line 5 column 18 (char 68)'''

    error_msg1_commentjson = '''Error Decoding JSON String - Unexpected Character
            "c": 'asdf'
                 ^

NEAR:
                "a": 1,
                "b": 2,
            >>  "c": 'asdf'  <<
            }

...

TOTAL LENGTH: 89 chars

Error at: line 5 column 18 (char 68)'''

    def test_invalid_type_load(self):
        with pytest.raises(TypeError):
            load(False)
        with pytest.raises(TypeError):
            load(None)
        with pytest.raises(TypeError):
            load(1)
        with pytest.raises(TypeError):
            load([])
        with pytest.raises(TypeError):
            load({})
        with pytest.raises(TypeError):
            load(set())

    def test_invalid_type_dump(self):
        with pytest.raises(TypeError) as excinfo:
            dump({}, 'myfile.json')

        self.assertIn('second argument must be file-type', str(excinfo.value))

    def test_invalid_type_loads(self):
        with pytest.raises(TypeError):
            loads(False)
        with pytest.raises(TypeError):
            loads(None)
        with pytest.raises(TypeError):
            loads(1)
        with pytest.raises(TypeError):
            loads([])
        with pytest.raises(TypeError):
            loads({})
        with pytest.raises(TypeError):
            loads(set())

    def test_template_type(self):
        with pytest.raises(TypeError):
            loads('{}', template=1)

    def test_empty_string(self):
        with pytest.raises(json.JSONDecodeError) as excinfo:
            loads('')

        self.assertIn('Expecting value - cannot parse empty', str(excinfo.value))

    def test_colored(self):
        with pytest.raises(json.JSONDecodeError) as excinfo:
            loads('''
{
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4
// }
               ''')
        print(excinfo.value)
        self.assertIn('''Error Decoding JSON String - Unexpected Character''', str(excinfo.value))
        self.assertIn('''"four": 4''', str(excinfo.value))
        self.assertIn('''\x1b[30m\x1b[103m        "four": 4\x1b[0m''', str(excinfo.value))

    def test_json_exception(self):
        with pytest.raises(json.JSONDecodeError):
            loads('1:"a"', comments=False)
        with pytest.raises(json.JSONDecodeError):
            loads('{a}', comments=False)
        with pytest.raises(json.JSONDecodeError):
            loads('{} // test', comments=False)

    def test_commentjson_exception(self):
        with pytest.raises(json.JSONDecodeError):
            loads('1:"a"')
        with pytest.raises(json.JSONDecodeError):
            loads('{a}')
        with pytest.raises(json.JSONDecodeError):
            loads('{"hello"}')

    def test_commentjson_exception_eof(self):
        # test json structure with no closing
        with pytest.raises(json.JSONDecodeError) as excinfo:
            loads('{"hello": 1 //} #asdf', colored=False)

        self.assertIn('''Error Decoding JSON String - Unexpected Character''', str(excinfo.value))

        with pytest.raises(json.JSONDecodeError) as excinfo:
            loads('''
            {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4
            // }
            ''', colored=False)
        self.assertIn('''Error Decoding JSON String - Unexpected Character''', str(excinfo.value))
        self.assertIn('''>>  "four": 4  <<''', str(excinfo.value))

        with pytest.raises(json.JSONDecodeError) as excinfo:
            loads('   ', colored=False)
        self.assertIn('''Expecting value - cannot parse empty JSON String''', str(excinfo.value))

    def test_json_exception_context(self):
        with pytest.raises(json.JSONDecodeError) as excinfo:
            loads(self.bad_json1, comments=False, colored=False)

        self.assertIn('Expecting value in JSON String', str(excinfo.value))
        self.assertIn('''>>  "c": 'asdf'  <<''', str(excinfo.value))
        self.assertIn('''Error at: line 5 column 18 (char 68)''', str(excinfo.value))

    def test_commentjson_exception_context(self):
        with pytest.raises(json.JSONDecodeError) as excinfo:
            loads(self.bad_json1, colored=False)
        self.assertIn('''Error Decoding JSON String - Unexpected Character''', str(excinfo.value))
        self.assertIn('"c": \'asdf\'', str(excinfo.value))
        self.assertIn('''>>  "c": 'asdf'  <<''', str(excinfo.value))
        self.assertIn('''Error at: line 5 column 18 (char 68)''', str(excinfo.value))