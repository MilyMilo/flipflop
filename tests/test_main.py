import unittest

from flipflop import flipflop


class TestMainFunction(unittest.TestCase):
    def test_basic_entrypoint_usage(self):
        code = "p and not q"
        result = flipflop(code, full=False)
        expected = {
            "header": ["p", "q", "(p AND NOT(q))"],
            "values": [
                [False, False, False],
                [False, True, False],
                [True, False, True],
                [True, True, False],
            ],
            "is_tautology": False,
        }
        self.assertEqual(result, expected)

    def test_complex_entrypoint_usage(self):
        code = "(p or q) and (not p xor q)"
        result = flipflop(code)
        expected = {
            "header": [
                "p",
                "q",
                "NOT(p)",
                "(p OR q)",
                "(NOT(p) XOR q)",
                "((p OR q) AND (NOT(p) XOR q))",
            ],
            "values": [
                [False, False, True, False, True, False],
                [False, True, True, True, False, False],
                [True, False, False, True, False, False],
                [True, True, False, True, True, True],
            ],
            "is_tautology": False,
        }
        self.assertEqual(result, expected)
