import unittest

from flipflop.core import (Lexer, Node, Parser, Reader, Token, TokenType,
                           Wordifier)


class ParserTestCase(unittest.TestCase):

    def _variable_node(self, value: str) -> Node:
        return Node(token=Token(type=TokenType.VARIABLE, value=value))

    def _operator_node(self, operator_type: TokenType, left: Node, right: Node) -> Node:
        return Node(token=Token(type=operator_type), left=left, right=right)

    def _unary_node(self, operator_type: TokenType, operand: Node) -> Node:
        return Node(token=Token(type=operator_type), left=operand, right=None)

    def test_produces_simple_syntax_tree(self):
        code = "p or q"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
        root_node = Parser(tokens).parse()

        self.assertIsInstance(root_node, Node)

        expected_root_node = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertEqual(expected_root_node, root_node)

    def test_respects_left_to_right_order_of_operations(self):
        code = "p or q or x"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
        root_node = Parser(tokens).parse()

        self.assertIsInstance(root_node, Node)

        expected_root_node = Node(
            token=Token(type=TokenType.OR),
            left=Node(
                token=Token(type=TokenType.OR),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
            ),
            right=Node(token=Token(type=TokenType.VARIABLE, value="x")),
        )

        self.assertEqual(expected_root_node, root_node)

    def test_respects_parentheses_in_order_of_operations(self):
        code = "(p or q) and x"
        tokens = Lexer(Wordifier(Reader(code)).wordify()).tokenize()
        root_node = Parser(tokens).parse()

        expected_root_node = Node(
            token=Token(type=TokenType.AND),
            left=Node(
                token=Token(type=TokenType.OR),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
            ),
            right=Node(token=Token(type=TokenType.VARIABLE, value="x")),
        )

        self.assertEqual(expected_root_node, root_node)

    def test_respects_operator_order_of_operations(self):
        operators = [
            ("nand", TokenType.NAND),
            ("and", TokenType.AND),
            ("nor", TokenType.NOR),
            ("or", TokenType.OR),
            ("xor", TokenType.XOR),
            ("if", TokenType.IF),
            ("eq", TokenType.EQ),
        ]

        for priority_1, (operator_1, type_1) in enumerate(operators):
            for priority_2, (operator_2, type_2) in enumerate(operators):
                if priority_1 == priority_2:
                    continue  # Skip testing an operator with itself

                with self.subTest(operator_1=operator_1, operator_2=operator_2):
                    expression = f"a {operator_1} b {operator_2} c"

                    # Determine which operation is primary based on precedence
                    if priority_1 < priority_2:
                        primary_op, secondary_op = type_1, type_2
                        primary_left, primary_right = "a", "b"
                        secondary_left = self._operator_node(
                            primary_op,
                            self._variable_node(primary_left),
                            self._variable_node(primary_right),
                        )
                        secondary_right = self._variable_node("c")
                    else:
                        primary_op, secondary_op = type_2, type_1
                        primary_left, primary_right = "b", "c"
                        secondary_left = self._variable_node("a")
                        secondary_right = self._operator_node(
                            primary_op,
                            self._variable_node(primary_left),
                            self._variable_node(primary_right),
                        )

                    expected_root_node = self._operator_node(
                        secondary_op, secondary_left, secondary_right
                    )

                    tokens = Lexer(Wordifier(Reader(expression)).wordify()).tokenize()
                    root_node = Parser(tokens).parse()
                    self.assertEqual(expected_root_node, root_node)

    def test_respects_unary_operator_order_of_operations(self):
        operators = [
            ("nand", TokenType.NAND),
            ("and", TokenType.AND),
            ("nor", TokenType.NOR),
            ("or", TokenType.OR),
            ("xor", TokenType.XOR),
            ("if", TokenType.IF),
            ("eq", TokenType.EQ),
        ]

        # Test the NOT operator against all other operators
        not_type = TokenType.NOT

        for _, (operator, op_type) in enumerate(operators):
            with self.subTest(operator=operator):
                expression = f"not a {operator} b"

                # The expected structure should always evaluate 'not a' first
                not_node = self._unary_node(not_type, self._variable_node("a"))
                expected_root_node = self._operator_node(
                    op_type, not_node, self._variable_node("b")
                )

                tokens = Lexer(Wordifier(Reader(expression)).wordify()).tokenize()
                root_node = Parser(tokens).parse()
                self.assertEqual(expected_root_node, root_node)
