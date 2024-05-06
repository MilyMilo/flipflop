from .exceptions import ParserError, TokenAssertionError, UnexpectedTokenError
from .node import Node
from .token import Token, TokenType


### Parser
# Structures the tokens into a Syntax Tree
class Parser:
    """
    The key to understanding this parsing logic is to recognize that the parse tree needs to be structured
    to evaluate expressions from the most tightly bound operations (deepest nodes) outward to the least tightly
    bound (root nodes). By starting with the lowest precedence operators, we ensure that these operators form
    the uppermost nodes of the tree. This setup allows higher precedence operations, parsed subsequently,
    to be nested deeper within the tree structure.

    This parsing approach ensures that when the tree is evaluated, the high precedence operations (deeper nodes)
    are processed first, with their results propagating up to be further processed by the lower precedence
    operators at higher levels of the tree. This method effectively allows each operator to operate on the results
    of more tightly bound sub-expressions, respecting the intended order of operations and encapsulation of
    logical units within the expression.

    Complete operator precedence:
    1. Parentheses (Highest)
    2. NOT
    3. NAND
    4. AND
    5. NOR
    6. OR
    7. XOR
    8. IF
    9. EQ (Lowest)
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0
        self.length = len(tokens)

    def parse(self) -> Node:
        """Parse the entire tree and return the root node"""
        return self.eq_expr()

    # 1. Handle equivalence (EQ) expressions
    def eq_expr(self) -> Node:
        node = self.imp_expr()
        while self.match(TokenType.EQ):
            token = Token(TokenType.EQ)
            right = self.imp_expr()
            node = Node(token, left=node, right=right)
        return node

    # 2. Handle implication (IF) expressions
    def imp_expr(self) -> Node:
        node = self.xor_expr()
        while self.match(TokenType.IF):
            token = Token(TokenType.IF)
            right = self.xor_expr()
            node = Node(token, left=node, right=right)
        return node

    # 3. Handle exclusive OR (XOR) expressions
    def xor_expr(self) -> Node:
        node = self.or_expr()
        while self.match(TokenType.XOR):
            token = Token(TokenType.XOR)
            right = self.or_expr()
            node = Node(token, left=node, right=right)
        return node

    # 4. Handle OR expressions
    def or_expr(self) -> Node:
        node = self.nor_expr()
        while self.match(TokenType.OR):
            token = Token(TokenType.OR)
            right = self.nor_expr()
            node = Node(token, left=node, right=right)
        return node

    # 5. Handle NOR expressions
    def nor_expr(self) -> Node:
        node = self.and_expr()
        while self.match(TokenType.NOR):
            token = Token(TokenType.NOR)
            right = self.and_expr()
            node = Node(token, left=node, right=right)
        return node

    # 6. Handle AND expressions
    def and_expr(self) -> Node:
        node = self.nand_expr()
        while self.match(TokenType.AND):
            token = Token(TokenType.AND)
            right = self.nand_expr()
            node = Node(token, left=node, right=right)
        return node

    # 7. Handle NAND expressions
    def nand_expr(self) -> Node:
        node = self.factor()
        while self.match(TokenType.NAND):
            token = Token(TokenType.NAND)
            right = self.factor()
            node = Node(token, left=node, right=right)
        return node

    # 8. Handle the highest priority and nested logical units (VARS, PARENS, NOT)
    def factor(self) -> Node:
        token = self.current()

        if getattr(token, "type", None) is None:
            raise TokenAssertionError(
                [TokenType.VARIABLE, TokenType.L_PAR, TokenType.NOT], None
            )

        match token.type:
            case TokenType.VARIABLE:
                self.consume()
                return Node(token)

            case TokenType.L_PAR:
                self.consume()
                node = self.parse()
                self.expect(TokenType.R_PAR)
                return node

            case TokenType.NOT:
                self.consume()
                not_token = Token(TokenType.NOT)
                return Node(not_token, left=self.factor())

            case _:
                raise UnexpectedTokenError(token)

    def match(self, token_type: TokenType) -> bool:
        if self.current() and self.current().type == token_type:
            self.consume()
            return True
        return False

    def expect(self, token_type: TokenType) -> None:
        if not self.match(token_type):
            token = self.current()
            raise TokenAssertionError(token_type, token.type if token else None)

    def current(self) -> Token | None:
        if self.position < self.length:
            return self.tokens[self.position]

        return None

    def consume(self) -> None:
        if self.position < self.length:
            self.position += 1
        else:
            raise ParserError("Attempted to consume() after end of statement")
