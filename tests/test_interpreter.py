import unittest

from flipflop.core import (
    Interpreter,
    Lexer,
    Node,
    Parser,
    Reader,
    Token,
    TokenType,
    Wordifier,
)


class InterpreterTestCase(unittest.TestCase):
    def test_interpreter_can_collect_variables(self):
        code = "p or q"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
        interpreter = Interpreter(Parser(tokens).parse())

        variables = interpreter._collect_variables()
        self.assertEqual(["p", "q"], variables)

    def test_interpreter_can_collect_expressions(self):
        code = "p or q"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
        interpreter = Interpreter(Parser(tokens).parse())

        expressions = interpreter._collect_expressions()
        expected_expressions = [
            Node(token=Token(type=TokenType.VARIABLE, value="p")),
            Node(token=Token(type=TokenType.VARIABLE, value="q")),
            Node(
                token=Token(type=TokenType.OR),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
            ),
        ]

        self.assertEqual(expected_expressions, expressions)

    def test_interpreter_can_determine_tautology(self):
        code = "p or not p"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
        interpreter = Interpreter(Parser(tokens).parse())
        results = interpreter.evaluate()
        self.assertTrue(results["is_tautology"])

    def test_interpreter_can_produce_truth_table(self):
        code = "p or q"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
        interpreter = Interpreter(Parser(tokens).parse())
        results = interpreter.evaluate()

        self.assertDictEqual(
            {
                "header": ["p", "q", "(p OR q)"],
                "values": [
                    [False, False, False],
                    [False, True, True],
                    [True, False, True],
                    [True, True, True],
                ],
                "is_tautology": False,
            },
            results,
        )

    def test_interpreter_can_produce_complex_truth_tables(self):
        expressions = [
            # Test case for nested expressions including each sub-expression
            (
                "not (p xor (q nand (not p)))",
                {
                    "header": [
                        "p",
                        "q",
                        "NOT(p)",
                        "(q NAND NOT(p))",
                        "(p XOR (q NAND NOT(p)))",
                        "NOT((p XOR (q NAND NOT(p))))",
                    ],
                    "values": [
                        [False, False, True, True, True, False],
                        [False, True, True, False, False, True],
                        [True, False, False, True, False, True],
                        [True, True, False, True, False, True],
                    ],
                    "is_tautology": False,
                },
            ),
            # Further cases adjusted for detailed sub-expression output
            (
                "(p and (q or not p))",
                {
                    "header": [
                        "p",
                        "q",
                        "NOT(p)",
                        "(q OR NOT(p))",
                        "(p AND (q OR NOT(p)))",
                    ],
                    "values": [
                        [False, False, True, True, False],
                        [False, True, True, True, False],
                        [True, False, False, False, False],
                        [True, True, False, True, True],
                    ],
                    "is_tautology": False,
                },
            ),
            # Adding more complex and nested expressions
            (
                "(p if (q if p))",
                {
                    "header": ["p", "q", "(q IF p)", "(p IF (q IF p))"],
                    "values": [
                        [False, False, True, True],
                        [False, True, False, True],
                        [True, False, True, True],
                        [True, True, True, True],
                    ],
                    "is_tautology": True,
                },
            ),
            (
                "((p xor q) and (q xor p))",
                {
                    "header": [
                        "p",
                        "q",
                        "(p XOR q)",
                        "(q XOR p)",
                        "((p XOR q) AND (q XOR p))",
                    ],
                    "values": [
                        [False, False, False, False, False],
                        [False, True, True, True, True],
                        [True, False, True, True, True],
                        [True, True, False, False, False],
                    ],
                    "is_tautology": False,
                },
            ),
        ]

        for expression, expected in expressions:
            with self.subTest(expression=expression):
                code = expression
                tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
                interpreter = Interpreter(Parser(tokens).parse())
                results = interpreter.evaluate()
                self.assertDictEqual(expected, results)

    def test_interpreter_can_produce_complex_truth_tables_with_more_than_two_variables(
        self,
    ):
        expressions = [
            # Simple expressions with 3 and 4 variables
            (
                "p or q or r",
                {
                    "header": ["p", "q", "r", "(p OR q)", "((p OR q) OR r)"],
                    "values": [
                        [False, False, False, False, False],
                        [False, False, True, False, True],
                        [False, True, False, True, True],
                        [False, True, True, True, True],
                        [True, False, False, True, True],
                        [True, False, True, True, True],
                        [True, True, False, True, True],
                        [True, True, True, True, True],
                    ],
                    "is_tautology": False,
                },
            ),
            (
                "p and q and r and s",
                {
                    "header": [
                        "p",
                        "q",
                        "r",
                        "s",
                        "(p AND q)",
                        "((p AND q) AND r)",
                        "(((p AND q) AND r) AND s)",
                    ],
                    "values": [
                        [False, False, False, False, False, False, False],
                        [False, False, False, True, False, False, False],
                        [False, False, True, False, False, False, False],
                        [False, False, True, True, False, False, False],
                        [False, True, False, False, False, False, False],
                        [False, True, False, True, False, False, False],
                        [False, True, True, False, False, False, False],
                        [False, True, True, True, False, False, False],
                        [True, False, False, False, False, False, False],
                        [True, False, False, True, False, False, False],
                        [True, False, True, False, False, False, False],
                        [True, False, True, True, False, False, False],
                        [True, True, False, False, True, False, False],
                        [True, True, False, True, True, False, False],
                        [True, True, True, False, True, True, False],
                        [True, True, True, True, True, True, True],
                    ],
                    "is_tautology": False,
                },
            ),
            # More complex expression with 3 variables
            (
                "(p and q) or (r and not (p or q))",
                {
                    "header": [
                        "p",
                        "q",
                        "r",
                        "(p OR q)",
                        "(p AND q)",
                        "NOT((p OR q))",
                        "(r AND NOT((p OR q)))",
                        "((p AND q) OR (r AND NOT((p OR q))))",
                    ],
                    "values": [
                        [False, False, False, False, False, True, False, False],
                        [False, False, True, False, False, True, True, True],
                        [False, True, False, True, False, False, False, False],
                        [False, True, True, True, False, False, False, False],
                        [True, False, False, True, False, False, False, False],
                        [True, False, True, True, False, False, False, False],
                        [True, True, False, True, True, False, False, True],
                        [True, True, True, True, True, False, False, True],
                    ],
                    "is_tautology": False,
                },
            ),
        ]

        for expression, expected in expressions:
            with self.subTest(expression=expression):
                code = expression
                tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
                interpreter = Interpreter(Parser(tokens).parse())
                results = interpreter.evaluate()
                self.assertDictEqual(expected, results)
