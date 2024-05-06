import json
from enum import Enum


class TokenType(Enum):
    NOT = "NOT"  # negation '~' / '¬'
    AND = "AND"  # conjunction '∧'
    OR = "OR"  # alternative '∨'
    IF = "IF"  # implication '→'
    EQ = "EQ"  # equivalence '⇔'
    XOR = "XOR"  # exclusive alternative '⊕'
    NAND = "NAND"  # negated conjunction '∣'
    NOR = "NOR"  # negated alternative '↓'
    L_PAR = "L_PAR"  # left parenthesis '('
    R_PAR = "R_PAR"  # right parenthesis ')'
    VARIABLE = "VARIABLE"  # terms e.g. 'p' / 'q'

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return self.value


class Token:
    def __init__(self, type: TokenType, value: str | None = None):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented

        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash((self.type, self.value))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        # Return value if the token has one - because it must be a variable
        # otherwise, return the type name
        return self.value if self.value else self.type.name

    def to_json_serializable(self):
        data = {
            "type": self.type.value,
        }

        if self.value is not None:
            data["value"] = self.value

        return data

    def as_json(self):
        return json.dumps(self.to_json_serializable(), indent=4)
