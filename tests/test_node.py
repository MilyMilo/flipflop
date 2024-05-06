import unittest

from flipflop.core import Node, Token, TokenType


class NodeTestCase(unittest.TestCase):

    def test_nodes_are_not_equal_to_different_objects(self):
        node = Node(token=Token(type=TokenType.VARIABLE, value="p"))
        obj = type("obj", (object,), {"test": "test"})
        self.assertFalse(node == obj)

    def test_nodes_are_equal_if_token_and_children_are_equal(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertTrue(node1 == node2)

    def test_nodes_are_not_equal_if_token_is_different(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.AND),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertFalse(node1 == node2)

    def test_nodes_are_not_equal_if_children_are_different_variables(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="a")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="b")),
        )

        self.assertFalse(node1 == node2)

    def test_nodes_are_not_equal_if_children_are_different_tokens(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.OR),
            left=Node(
                token=Token(type=TokenType.AND),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
            ),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertFalse(node1 == node2)

    def test_node_hash_is_the_same_for_equal_nodes(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertTrue(hash(node1) == hash(node2))

    def test_node_hash_is_different_for_different_nodes(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.AND),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertFalse(hash(node1) == hash(node2))

    def test_binary_operation_nodes_have_string_representation(self):
        for token_type in TokenType:
            if token_type in [
                TokenType.NOT,
                TokenType.VARIABLE,
                TokenType.L_PAR,
                TokenType.R_PAR,
            ]:
                continue

            with self.subTest(token_type=token_type):
                node = Node(
                    token=Token(type=token_type),
                    left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                    right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
                )
                self.assertEqual(f"(p {token_type.value} q)", str(node))

    def test_unary_operation_nodes_have_string_representation(self):
        node = Node(
            token=Token(type=TokenType.NOT),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
        )

        self.assertEqual("NOT(p)", str(node))

    def test_binary_and_unary_operation_nodes_have_string_representation(self):
        node = Node(
            token=Token(type=TokenType.OR),
            left=Node(
                token=Token(type=TokenType.NOT),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            ),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertEqual("(NOT(p) OR q)", str(node))

    def test_nodes_support_gt_and_lt_operators_by_length_of_string_representation(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.OR),
            left=Node(
                token=Token(type=TokenType.AND),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
            ),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertTrue(node1 < node2)
        self.assertTrue(node2 > node1)
        self.assertFalse(node1 > node2)
        self.assertFalse(node2 < node1)

    def test_nodes_support_gt_and_lt_operators_alphabetically_if_the_same_length_of_representation(
        self,
    ):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="a")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="b")),
        )

        node2 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertTrue(node1 < node2)
        self.assertTrue(node2 > node1)
        self.assertFalse(node1 > node2)
        self.assertFalse(node2 < node1)

    def test_nodes_can_be_sorted_by_length_of_string_representation(self):
        node1 = Node(
            token=Token(type=TokenType.OR),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node2 = Node(
            token=Token(type=TokenType.OR),
            left=Node(
                token=Token(type=TokenType.AND),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
            ),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        node3 = Node(
            token=Token(type=TokenType.AND),
            left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        nodes = [node1, node2, node3]
        sorted_nodes = sorted(nodes)
        self.assertListEqual([node1, node3, node2], sorted_nodes)

        reverse_sorted_nodes = sorted(nodes, reverse=True)
        self.assertListEqual([node2, node3, node1], reverse_sorted_nodes)

    def test_nodes_have_json_representation(self):
        node = Node(
            token=Token(type=TokenType.OR),
            left=Node(
                token=Token(type=TokenType.AND),
                left=Node(token=Token(type=TokenType.VARIABLE, value="p")),
                right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
            ),
            right=Node(token=Token(type=TokenType.VARIABLE, value="q")),
        )

        self.assertDictEqual(
            {
                "token": {"type": "OR"},
                "left": {
                    "token": {"type": "AND"},
                    "left": {"token": {"type": "VARIABLE", "value": "p"}},
                    "right": {"token": {"type": "VARIABLE", "value": "q"}},
                },
                "right": {
                    "token": {"type": "VARIABLE", "value": "q"},
                },
            },
            node.to_json_serializable(),
        )
