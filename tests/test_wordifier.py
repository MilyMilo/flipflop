from unittest import TestCase

from flipflop.core import Reader, Wordifier


class WordifierTestCase(TestCase):

    def test_wordifies_simple_expressions(self):
        code = "p or q"
        words = Wordifier(Reader(code)).wordify()
        self.assertEqual(words, ["p", "∨", "q"])

    def test_wordifies_parenthesis(self):
        code = "(p or q) xor not q"
        words = Wordifier(Reader(code)).wordify()
        self.assertEqual(words, ["(", "p", "∨", "q", ")", "⊕", "~", "q"])

    def test_wordifies_longer_variables(self):
        code = "(tst or test) xor not teest"
        words = Wordifier(Reader(code)).wordify()
        self.assertEqual(words, ["(", "tst", "∨", "test", ")", "⊕", "~", "teest"])
