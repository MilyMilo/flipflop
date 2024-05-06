import unittest

from flipflop.core import OutOfBoundsError, Reader


class ReaderTestCase(unittest.TestCase):

    def test_replaces_ambiguous_characters(self):
        code = "(p | q) v (p | q) v (p ^ q)"
        reader = Reader(code)
        self.assertEqual("(p ∣ q) ∨ (p ∣ q) ∨ (p ∧ q)", reader.code)

    def test_replaces_syntax_sugar(self):
        code = "a or b and c nor d xor not e nand f nor g eq h if i"
        reader = Reader(code)
        self.assertEqual("a ∨ b ∧ c ↓ d ⊕ ~ e ∣ f ↓ g ⇔ h → i", reader.code)

    def test_removes_leading_and_trailing_whitespace(self):
        code = """
        p or q
        """

        reader = Reader(code)
        self.assertEqual("p ∨ q", reader.code)

    def test_backstep_cannot_reach_less_than_zero(self):
        code = "p or q"
        reader = Reader(code)

        self.assertEqual(reader.i, 0)
        reader.backstep()
        self.assertEqual(reader.i, 0)

    def test_peek_does_not_increment_i(self):
        code = "p or q"
        reader = Reader(code)

        self.assertEqual(reader.i, 0)
        reader.peek()
        self.assertEqual(reader.i, 0)

    def test_peek_returns_correct_char(self):
        code = "p or q"
        reader = Reader(code)
        self.assertEqual("p", reader.peek())

    def test_next_cannot_exceed_code_length(self):
        code = "p ∨ q"
        reader = Reader(code)

        for i in range(5):
            reader.next()

        with self.assertRaises(OutOfBoundsError):
            reader.next()

    def test_next_returns_correct_char(self):
        code = "p ∨ q"
        reader = Reader(code)

        self.assertEqual("p", reader.next())
        self.assertEqual(" ", reader.next())
        self.assertEqual("∨", reader.next())
        self.assertEqual(" ", reader.next())
        self.assertEqual("q", reader.next())

    def test_next_increments_i(self):
        code = "p ∨ q"
        reader = Reader(code)

        self.assertEqual(reader.i, 0)
        reader.next()
        self.assertEqual(reader.i, 1)

    def test_has_next_determines_if_code_is_finished(self):
        code = "p ∨ q"
        reader = Reader(code)

        for i in range(5):
            self.assertTrue(reader.has_next())
            reader.next()

        self.assertFalse(reader.has_next())

    def test_read_until_reads_until_predicate_condition_unmet(self):
        code = "p ∨ q"
        reader = Reader(code)

        result = reader.read_until(lambda c: c != "∨")

        self.assertEqual("p ", result)
        self.assertTrue("∨", reader.peek())
        self.assertEqual(2, reader.i)

    def test_read_until_does_not_exceed_code_length(self):
        code = "p ∨ q"
        reader = Reader(code)

        result = reader.read_until(lambda c: True)
        self.assertEqual("p ∨ q", result)

    def test_skip_whitespace_skips_whitespace(self):
        code = "p     ∨      q"
        reader = Reader(code)

        reader.next()
        reader.skip_whitespace()

        self.assertEqual("∨", reader.peek())
        self.assertEqual(reader.i, 6)
