import unittest

from flipflop.core import Evaluator, Node, Token, TokenType


class EvaluatorTestCase(unittest.TestCase):
    def setUp(self):
        self.evaluator = Evaluator()

    def test_logical_operations(self):
        test_cases = [
            # operator, left_value, right_value, expected_result
            ("NOT", True, None, False),
            ("NOT", False, None, True),
            ("AND", True, True, True),
            ("AND", True, False, False),
            ("AND", False, False, False),
            ("OR", True, True, True),
            ("OR", True, False, True),
            ("OR", False, False, False),
            ("NAND", True, True, False),
            ("NAND", True, False, True),
            ("NAND", False, False, True),
            ("NOR", True, True, False),
            ("NOR", True, False, False),
            ("NOR", False, False, True),
            ("XOR", True, True, False),
            ("XOR", True, False, True),
            ("XOR", False, False, False),
            ("IF", True, False, False),
            ("IF", True, True, True),
            ("IF", False, True, True),
            ("EQ", True, True, True),
            ("EQ", True, False, False),
            ("EQ", False, False, True),
        ]

        for operator, left_val, right_val, expected in test_cases:
            with self.subTest(
                operator=operator, left=left_val, right=right_val, expected=expected
            ):
                node = Node(
                    token=Token(TokenType[operator]),
                    left=(
                        Node(Token(TokenType.VARIABLE, "p"))
                        if left_val is not None
                        else None
                    ),
                    right=(
                        Node(Token(TokenType.VARIABLE, "q"))
                        if right_val is not None
                        else None
                    ),
                )

                variable_values = (
                    {"p": left_val, "q": right_val}
                    if right_val is not None
                    else {"p": left_val}
                )
                result = self.evaluator.evaluate(node, variable_values)
                self.assertEqual(
                    result,
                    expected,
                    f"Failed for {operator} with left: {left_val}, right: {right_val}",
                )

    def test_returns_false_if_node_is_none(self):
        result = self.evaluator.evaluate(None, {})
        self.assertFalse(
            result, "Evaluating None node did not return False as expected."
        )
