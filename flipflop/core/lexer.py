from .exceptions import (InvalidBinaryTokenPlacement,
                         InvalidParenthesisTokenPlacement,
                         InvalidUnaryTokenPlacement,
                         InvalidVariableTokenPlacement)
from .token import Token, TokenType


### Lexer
# Tokenizes the words into tokens
class Lexer:
    def __init__(self, words: list[str]):
        self.words = words
        self.tokens = []

    def tokenize(self) -> list[Token]:
        for word in self.words:
            self.add_token(word)

        return self.tokens

    def add_token(self, word: str):
        match word:
            case "~" | "¬":
                self.expect_unary_position(word)
                self.tokens.append(Token(TokenType.NOT))
            case "∧":
                self.expect_binary_position(word)
                self.tokens.append(Token(TokenType.AND))
            case "∨":
                self.expect_binary_position(word)
                self.tokens.append(Token(TokenType.OR))
            case "→":
                self.expect_binary_position(word)
                self.tokens.append(Token(TokenType.IF))
            case "⇔":
                self.expect_binary_position(word)
                self.tokens.append(Token(TokenType.EQ))
            case "⊕":
                self.expect_binary_position(word)
                self.tokens.append(Token(TokenType.XOR))
            case "∣":
                self.expect_binary_position(word)
                self.tokens.append(Token(TokenType.NAND))
            case "↓":
                self.expect_binary_position(word)
                self.tokens.append(Token(TokenType.NOR))
            case "(":
                self.tokens.append(Token(TokenType.L_PAR))
            case ")":
                self.expect_closing_parenthesis(word)
                self.tokens.append(Token(TokenType.R_PAR))
            case _:
                self.expect_variable_position(word)
                self.tokens.append(Token(TokenType.VARIABLE, value=word))

    def expect_unary_position(self, word: str):
        """
        Expect a unary operator to be placed only after a left parenthesis, another unary, or as the first token.
        """
        if self.tokens and self.tokens[-1].type not in {
            TokenType.L_PAR,
            TokenType.NOT,
            TokenType.AND,
            TokenType.OR,
            TokenType.IF,
            TokenType.EQ,
            TokenType.XOR,
            TokenType.NAND,
            TokenType.NOR,
        }:
            raise InvalidUnaryTokenPlacement(
                f"Invalid placement of unary operator '{word}' after '{self.tokens[-1].type}'"
            )

    def expect_binary_position(self, word: str):
        """
        Expect a binary operator to follow either a variable or a right parenthesis.
        """
        if not self.tokens or self.tokens[-1].type not in {
            TokenType.VARIABLE,
            TokenType.R_PAR,
        }:
            raise InvalidBinaryTokenPlacement(
                f"Invalid placement of binary operator '{word}' at the start or after an invalid token"
            )

    def expect_variable_position(self, word: str):
        """
        Expect a variable to follow a left parenthesis, any operator, or as the first token.
        Disallow variable immediately after another variable or right parenthesis without an operator.
        """
        if self.tokens and self.tokens[-1].type not in {
            TokenType.L_PAR,
            TokenType.NOT,
            TokenType.AND,
            TokenType.OR,
            TokenType.IF,
            TokenType.EQ,
            TokenType.XOR,
            TokenType.NAND,
            TokenType.NOR,
        }:
            raise InvalidVariableTokenPlacement(
                f"Invalid placement of variable '{word}' immediately following '{self.tokens[-1].type}'"
            )

    def expect_closing_parenthesis(self, word: str):
        """
        Expect a closing parenthesis to follow a variable or another right parenthesis,
        indicating the closure of an open expression.
        """
        if not self.tokens or self.tokens[-1].type not in {
            TokenType.VARIABLE,
            TokenType.R_PAR,
        }:
            raise InvalidParenthesisTokenPlacement(
                "Invalid placement of closing parenthesis ')' without a matching opening '(' or improperly placed"
            )
