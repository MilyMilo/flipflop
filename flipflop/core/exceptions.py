from .token import Token, TokenType


class ReaderError(Exception):
    """Base class for Reader exceptions"""

    pass


class OutOfBoundsError(ReaderError):
    """Exception raised when reader is attempting to read outside the text bounds"""

    def __init__(self, message="Attempted to access text outside of the text bounds"):
        self.message = message
        super().__init__(self.message)


class LexerError(Exception):
    """Base class for Lexer exceptions"""

    pass


class ParserError(Exception):
    """Base class for Parser exceptions"""

    pass


class InvalidUnaryTokenPlacement(LexerError):
    pass


class InvalidBinaryTokenPlacement(LexerError):
    pass


class InvalidVariableTokenPlacement(LexerError):
    pass


class InvalidParenthesisTokenPlacement(LexerError):
    pass


class UnexpectedTokenError(ParserError):
    """Exception raised for tokens which were unexpected in the current context."""

    def __init__(self, token: Token):
        self.token = token
        super().__init__(f"Unexpected token: {token}")


class TokenAssertionError(ParserError):
    """Exception raised when an expected token is not found."""

    def __init__(self, expected: TokenType | list[TokenType], found: TokenType | None):
        self.expected = expected
        self.found = found

        if isinstance(self.expected, list):
            super().__init__(
                f"Expected to find one of: {expected}, but found {found if found else 'end of input'}"
            )
            return

        super().__init__(
            f"Expected to find {expected}, but found {found if found else 'end of input'}"
        )
