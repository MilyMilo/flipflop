import unittest

from flipflop.core import Token, TokenType


class TokenTestCase(unittest.TestCase):

    def test_tokens_are_not_equal_to_different_objects(self):
        token = Token(type=TokenType.OR)
        obj = type("obj", (object,), {"test": "test"})
        self.assertFalse(token == obj)

    def test_operator_tokens_are_equal_if_token_type_is_the_same(self):
        token1 = Token(type=TokenType.OR)
        token2 = Token(type=TokenType.OR)
        self.assertTrue(token1 == token2)

    def test_operator_tokens_are_not_equal_if_token_type_is_different(self):
        token1 = Token(type=TokenType.OR)
        token2 = Token(type=TokenType.AND)
        self.assertFalse(token1 == token2)

    def test_variable_tokens_are_equal_if_token_type_and_value_are_the_same(self):
        token1 = Token(type=TokenType.VARIABLE, value="p")
        token2 = Token(type=TokenType.VARIABLE, value="p")
        self.assertTrue(token1 == token2)

    def test_variable_tokens_are_not_equal_if_token_type_is_different(self):
        token1 = Token(type=TokenType.L_PAR)
        token2 = Token(type=TokenType.VARIABLE, value="p")
        self.assertFalse(token1 == token2)

    def test_variable_tokens_are_not_equal_if_token_value_is_different(self):
        token1 = Token(type=TokenType.VARIABLE, value="p")
        token2 = Token(type=TokenType.VARIABLE, value="q")
        self.assertFalse(token1 == token2)

    def test_token_hash_is_the_same_for_equal_tokens(self):
        token1 = Token(type=TokenType.VARIABLE, value="p")
        token2 = Token(type=TokenType.VARIABLE, value="p")
        self.assertTrue(hash(token1) == hash(token2))

    def test_token_hash_is_different_for_different_tokens(self):
        token1 = Token(type=TokenType.VARIABLE, value="p")
        token2 = Token(type=TokenType.VARIABLE, value="q")
        self.assertFalse(hash(token1) == hash(token2))

    def test_variable_tokens_have_json_representation(self):
        token = Token(type=TokenType.VARIABLE, value="p")
        self.assertDictEqual(
            {"type": "VARIABLE", "value": "p"}, token.to_json_serializable()
        )

    def test_variable_tokens_have_string_representation(self):
        token = Token(type=TokenType.VARIABLE, value="p")
        self.assertEqual("p", str(token))

    def test_operator_tokens_have_string_representation(self):
        for token_type in TokenType:
            token = Token(type=token_type)
            self.assertEqual(token_type.value, str(token))

    def test_operator_tokens_have_json_representation(self):
        for token_type in TokenType:
            with self.subTest(token_type=token_type.value):
                token = Token(type=token_type)
                self.assertDictEqual(
                    {"type": token_type.value}, token.to_json_serializable()
                )
