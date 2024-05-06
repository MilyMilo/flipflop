from .node import Node
from .token import TokenType


### Evaluator
# Helper class for evaluating logical expressions
class Evaluator:
    def evaluate(self, node: Node | None, variable_values: dict[str, bool]):
        """Evaluate the AST node recursively given a dictionary of variable values"""

        # None is an edge-case which may happen
        if node is None:
            return False

        match node.token.type:
            case TokenType.VARIABLE:
                return variable_values[node.token.value]

            case TokenType.NOT:
                return not self.evaluate(node.left, variable_values)

            case TokenType.AND:
                left_val = self.evaluate(node.left, variable_values)
                right_val = self.evaluate(node.right, variable_values)
                return left_val and right_val

            case TokenType.OR:
                left_val = self.evaluate(node.left, variable_values)
                right_val = self.evaluate(node.right, variable_values)
                return left_val or right_val

            case TokenType.NAND:
                left_val = self.evaluate(node.left, variable_values)
                right_val = self.evaluate(node.right, variable_values)
                return not (left_val and right_val)

            case TokenType.NOR:
                left_val = self.evaluate(node.left, variable_values)
                right_val = self.evaluate(node.right, variable_values)
                return not (left_val or right_val)

            case TokenType.XOR:
                left_val = self.evaluate(node.left, variable_values)
                right_val = self.evaluate(node.right, variable_values)
                return left_val != right_val

            case TokenType.IF:
                left_val = self.evaluate(node.left, variable_values)
                right_val = self.evaluate(node.right, variable_values)
                return not left_val or right_val

            case TokenType.EQ:
                left_val = self.evaluate(node.left, variable_values)
                right_val = self.evaluate(node.right, variable_values)
                return left_val == right_val

            case _:
                raise ValueError(f"Unsupported operator {node.token.type}")
