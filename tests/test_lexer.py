import unittest

from flipflop.core import Lexer, Reader, Token, TokenType, Wordifier
from flipflop.core.exceptions import (InvalidBinaryTokenPlacement,
                                      InvalidParenthesisTokenPlacement,
                                      InvalidUnaryTokenPlacement,
                                      InvalidVariableTokenPlacement)


class LexerTestCase(unittest.TestCase):

    def test_tokenizes_simple_variables(self):
        code = "p or q"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()

        self.assertEqual(
            [
                Token(type=TokenType.VARIABLE, value="p"),
                Token(type=TokenType.OR),
                Token(type=TokenType.VARIABLE, value="q"),
            ],
            tokens,
        )

    def test_tokenizes_longer_variables(self):
        code = "tst or test"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()

        self.assertEqual(
            [
                Token(type=TokenType.VARIABLE, value="tst"),
                Token(type=TokenType.OR),
                Token(type=TokenType.VARIABLE, value="test"),
            ],
            tokens,
        )

    def test_tokenizes_parentheses(self):
        code = "(p or q)"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()

        self.assertEqual(
            [
                Token(type=TokenType.L_PAR),
                Token(type=TokenType.VARIABLE, value="p"),
                Token(type=TokenType.OR),
                Token(type=TokenType.VARIABLE, value="q"),
                Token(type=TokenType.R_PAR),
            ],
            tokens,
        )

    def test_tokenizes_binary_operators(self):
        operators = {
            "∧": TokenType.AND,
            "∨": TokenType.OR,
            "→": TokenType.IF,
            "⇔": TokenType.EQ,
            "⊕": TokenType.XOR,
            "∣": TokenType.NAND,
            "↓": TokenType.NOR,
        }

        for op_sym, op_type in operators.items():
            code = f"p {op_sym} q"

            with self.subTest(code=code):
                tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
                self.assertEqual(
                    [
                        Token(type=TokenType.VARIABLE, value="p"),
                        Token(type=op_type),
                        Token(type=TokenType.VARIABLE, value="q"),
                    ],
                    tokens,
                )

    def test_tokenizes_unary_operators(self):
        for code in ["p and not q", "p ∧ ~q", "p ∧ ¬q"]:
            with self.subTest(code=code):
                tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
                self.assertEqual(
                    [
                        Token(type=TokenType.VARIABLE, value="p"),
                        Token(type=TokenType.AND),
                        Token(type=TokenType.NOT),
                        Token(type=TokenType.VARIABLE, value="q"),
                    ],
                    tokens,
                )

    def test_validates_unary_token_placement(self):
        for code in ["p ~ q", "p ¬ q"]:
            with self.subTest(code=code):
                with self.assertRaises(InvalidUnaryTokenPlacement):
                    Lexer(Wordifier(Reader(code)).wordify()).tokenize()

    def test_validates_binary_token_placement(self):
        operators = {
            "∧": TokenType.AND,
            "∨": TokenType.OR,
            "→": TokenType.IF,
            "⇔": TokenType.EQ,
            "⊕": TokenType.XOR,
            "∣": TokenType.NAND,
            "↓": TokenType.NOR,
        }

        for operator in operators.keys():
            with self.subTest(operator=operator):
                code = f"{operator} q"

                with self.assertRaises(InvalidBinaryTokenPlacement):
                    Lexer(Wordifier(Reader(code)).wordify()).tokenize()

    def test_validates_variable_token_placement(self):
        for code in ["a a", "(a or b) c"]:
            with self.subTest(code=code):
                with self.assertRaises(InvalidVariableTokenPlacement):
                    Lexer(Wordifier(Reader(code)).wordify()).tokenize()

    def test_validates_parenthesis_token_placement(self):
        for code in [")", "())"]:
            with self.subTest(code=code):
                with self.assertRaises(InvalidParenthesisTokenPlacement):
                    Lexer(Wordifier(Reader(code)).wordify()).tokenize()
