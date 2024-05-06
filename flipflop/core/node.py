import json
from typing import Self

from .token import Token


class Node:
    def __init__(
        self, token: Token, left: Self | None = None, right: Self | None = None
    ):
        self.token = token
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented

        # Nodes are considered equal if the tokens, left children, and right children are equal
        return (
            self.token == other.token
            and self.left == other.left
            and self.right == other.right
        )

    def __hash__(self):
        return hash((self.token, self.left, self.right))

    def __lt__(self, other):
        """
        Note: The Nodes do not have a meaningful way of being less or more than other nodes.
        They also abide by the order defined in the AST. This method is implemented purely to sort
        them visually in the truth table, and should be considered in this implementation only.
        """
        if not isinstance(other, Node):
            return NotImplemented

        if len(repr(self)) == len(repr(other)):
            return repr(self) < repr(other)

        return len(repr(self)) < len(repr(other))

    def __gt__(self, other):
        """
        Note: The Nodes do not have a meaningful way of being less or more than other nodes.
        They also abide by the order defined in the AST. This method is implemented purely to sort
        them visually in the truth table, and should be considered in this implementation only.
        """
        if not isinstance(other, Node):
            return NotImplemented

        if len(repr(self)) == len(repr(other)):
            return repr(self) > repr(other)

        return len(repr(self)) > len(repr(other))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        # Handle binary operations (e.g. AND, OR, XOR)
        if self.left and self.right:
            return f"({self._repr_child(self.left)} {self.token.type.value} {self._repr_child(self.right)})"

        # Handle unary operations (e.g. NOT)
        elif self.left:
            return f"{self.token.type.value}({self._repr_child(self.left)})"

        # Handle leaf nodes (e.g. VARS)
        else:
            return self._format_leaf()

    def _repr_child(self, child):
        """Format child nodes"""
        return repr(child)

    def _format_leaf(self):
        """Format leaf node which will be variables"""
        return str(self.token.value)

    def to_json_serializable(self):
        data = {
            "token": self.token.to_json_serializable(),
        }

        if self.left is not None:
            data["left"] = self.left.to_json_serializable()

        if self.right is not None:
            data["right"] = self.right.to_json_serializable()

        return data

    def as_json(self):
        return json.dumps(self.to_json_serializable(), indent=4)
