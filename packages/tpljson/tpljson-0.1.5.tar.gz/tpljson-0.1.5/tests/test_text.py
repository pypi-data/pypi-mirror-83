import unittest
from tpljson.text import surround_text, preview_text, highlight_text


class TestTextFunctions(unittest.TestCase):
    TEXT = '''{
    "replaces": "0.9.1",
    "hash": "f082b775fc70cf973d91c31ddbbcf36f21088377",
    "depends": "conda",
    "components": [
        {
            "version": "3.4.1",
            "name": "conda"
        }
    ],
    "conflicts": "",
    "package": "tpljson-1.0.0"
}
'''

    def test_highlight_text_defaults(self):
        t = highlight_text('test')
        self.assertEqual(t, '\x1b[30m\x1b[103mtest\x1b[0m')

    def test_surround_text_defaults(self):
        t = surround_text('     hello world     ')
        self.assertEqual(t, ' >>  hello world  << ')

    def test_surround_text_custom(self):
        t = surround_text('    hello world    ', left='[', right=']', pad=0)
        self.assertEqual(t, '   [hello world]   ')

    def test_surround_text_no_ws(self):
        t = surround_text('    hello world    ', left='[', right=']', pad=1, preserve_whitespace=False)
        self.assertEqual(t, '[ hello world ]')

    # TODO test highlight_text()

    def test_preview_text_defaults(self):
        t = preview_text(self.TEXT)
        self.assertEqual(t, '''    {
        "replaces": "0.9.1",
        "hash": "f082b775fc70cf973d91c31ddbbcf36f21088377",
        "depends": "conda",
        "components": [''')

    def test_preview_text_dedent(self):
        t = preview_text('  a\n  b', indent=0, dedent=True)
        self.assertEqual(t, 'a\nb')

    def test_preview_center_line(self):
        t = preview_text('one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine', indent=2, max_lines=3, center_line=4)
        self.assertEqual(t, '  three\n  four\n  five')

    def test_preview_max_chars(self):
        pass
        t = preview_text('united states of america\ncanada\nrepublic of congo\nsouth africa\n'
                         'democratic republic of tao tom\nunited federation of russia\n'
                         'united kingdom of great britain and northern ireland',
                         indent=2, max_lines=5, center_line=4, max_chars=100)
        self.assertEqual(t, '''  canada
  republic of congo
  south africa
  democratic republic...
  united federation o...''')

    def test_preview_prefix_suffix(self):
        t = preview_text('one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine',
                         indent=2, max_lines=3, center_line=4, prefix='  PREFIX\n', suffix='\n  SUFFIX')
        self.assertEqual(t, '  PREFIX\n  three\n  four\n  five\n  SUFFIX')

    def test_preview_highlight(self):
        text = 'one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine'
        t1 = preview_text(text, indent=2, max_lines=3, center_line=4, highlight=4)
        t2 = preview_text(text, indent=2, max_lines=3, center_line=4, highlight=4, colored=True)
        self.assertEqual(t1, '  three\n\x1b[30m\x1b[103m  four\x1b[0m\n  five')
        self.assertEqual(t1, t2)

    def test_preview_surround(self):
        t = preview_text('one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine',
                         indent=2, max_lines=3, center_line=4, highlight=4, colored=False)
        self.assertEqual(t, '  three\n>>  four  <<\n  five')