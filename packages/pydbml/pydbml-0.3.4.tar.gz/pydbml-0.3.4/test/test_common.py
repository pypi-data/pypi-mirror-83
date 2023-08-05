from unittest import TestCase
from pyparsing import ParseSyntaxException, ParserElement
from pydbml.definitions.common import comment, _c, note, note_object


ParserElement.setDefaultWhitespaceChars(' \t\r')


class TestComment(TestCase):
    def test_comment_endstring(self):
        val = '//test comment'
        res = comment.parseString(val, parseAll=True)
        self.assertEqual(res[0], 'test comment')

    def test_comment_endline(self):
        val = '//test comment\n\n\n\n\n'
        res = comment.parseString(val)
        self.assertEqual(res[0], 'test comment')


class Test_c(TestCase):
    def test_comment(self):
        val = '\n\n\n\n//comment line 1\n\n//comment line 2'
        res = _c.parseString(val, parseAll=True)
        self.assertEqual(list(res), ['comment line 1', 'comment line 2'])


class TestNote(TestCase):
    def test_single_quote(self):
        val = "note: 'test note'"
        res = note.parseString(val, parseAll=True)
        self.assertEqual(res[0].text, 'test note')

    def test_double_quote(self):
        val = 'note: \n "test note"'
        res = note.parseString(val, parseAll=True)
        self.assertEqual(res[0].text, 'test note')

    def test_multiline(self):
        val = "note: '''line1\nline2\nline3'''"
        res = note.parseString(val, parseAll=True)
        self.assertEqual(res[0].text, 'line1\nline2\nline3')

    def test_unclosed_quote(self):
        val = 'note: "test note'
        with self.assertRaises(ParseSyntaxException):
            note.parseString(val, parseAll=True)

    def test_not_allowed_multiline(self):
        val = "note: 'line1\nline2\nline3'"
        with self.assertRaises(ParseSyntaxException):
            note.parseString(val, parseAll=True)


class TestNoteObject(TestCase):
    def test_single_quote(self):
        val = "note {'test note'}"
        res = note_object.parseString(val, parseAll=True)
        self.assertEqual(res[0].text, 'test note')

    def test_double_quote(self):
        val = 'note \n\n {\n\n"test note"\n\n}'
        res = note_object.parseString(val, parseAll=True)
        self.assertEqual(res[0].text, 'test note')

    def test_multiline(self):
        val = "note\n{ '''line1\nline2\nline3'''}"
        res = note_object.parseString(val, parseAll=True)
        self.assertEqual(res[0].text, 'line1\nline2\nline3')

    def test_unclosed_quote(self):
        val = 'note{ "test note}'
        with self.assertRaises(ParseSyntaxException):
            note_object.parseString(val, parseAll=True)

    def test_not_allowed_multiline(self):
        val = "note { 'line1\nline2\nline3' }"
        with self.assertRaises(ParseSyntaxException):
            note_object.parseString(val, parseAll=True)
