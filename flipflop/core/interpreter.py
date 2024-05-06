import itertools

from .evaluator import Evaluator
from .node import Node
from .token import Token, TokenType


### Interpreter
# Interprets the Syntax Tree to generate a truth table for all expressions in all possible variable states
class Interpreter:
    def __init__(self, root_node: Node):
        self.root_node = root_node
        self.evaluator = Evaluator()

    def evaluate(self, full: bool = True):
        """Evaluate the AST to determine the state of all expressions in all possible variable states"""
        variables = self._collect_variables()

        if full:
            expressions = self._collect_expressions()
        else:
            # Only include variables + final expression if intermediate (sub-expression) output is not necessary
            expressions = [Node(Token(TokenType.VARIABLE, v)) for v in variables] + [
                self.root_node
            ]

        # Generate all combinations of truth values for the variables
        combinations = list(itertools.product([False, True], repeat=len(variables)))

        # Generate a truth table with rows for each expression
        truth_table = {repr(expr): [] for expr in expressions}

        # Evaluate each expression for each combination
        values = []
        for combination in combinations:
            # Map variable names to their current values in this specific combination
            current_variable_values = dict(zip(variables, combination))

            row = []
            for expression in expressions:
                result = self.evaluator.evaluate(expression, current_variable_values)
                truth_table[repr(expression)].append(result)
                row.append(result)

            values.append(row)

        headers = [repr(expr) for expr in expressions]
        return {
            "header": headers,
            "values": values,
            "is_tautology": self._is_tautology(),
        }

    def _collect_variables(
        self, node: Node | None = None, variables: set[str] | None = None
    ) -> list[str]:
        """
        Collect all variables from a Node.
        Variables are also considered expressions, however this method allows to easily extract only variables.
        """
        if node is None:
            node = self.root_node

        if variables is None:
            variables = set()

        if node.token.type == TokenType.VARIABLE:
            if getattr(node.token, "value", None) is None:
                raise ValueError("Encountered a variable token without a value (name)")

            variables.add(node.token.value)

        if node.left:
            self._collect_variables(node.left, variables)

        if node.right:
            self._collect_variables(node.right, variables)

        return sorted(variables)

    def _collect_expressions(self, node: Node | None = None) -> list[Node]:
        """Collect all expressions, including the variables, all sub-expressions, and the full expression."""
        if node is None:
            node = self.root_node

        expressions = []

        if node.left:
            expressions.extend(self._collect_expressions(node.left))

        if node.right:
            expressions.extend(self._collect_expressions(node.right))

        expressions.append(node)

        # Cast to set to remove duplicates, then sort which will return a list
        return sorted(set(expressions))

    def _is_tautology(self) -> bool:
        """Check if the root expression is a tautology."""
        variables = self._collect_variables()

        # Generate all combinations of truth values for the variables
        combinations = list(itertools.product([False, True], repeat=len(variables)))

        # Evaluate the root expression for each combination
        for combination in combinations:
            current_variable_values = dict(zip(variables, combination))
            result = self.evaluator.evaluate(self.root_node, current_variable_values)

            # If any combination yields False, the expression is not a tautology
            if result is not True:
                return False

        return True
