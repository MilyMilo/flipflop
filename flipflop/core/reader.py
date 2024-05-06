from typing import Callable

from .exceptions import OutOfBoundsError


### Reader
# Reads the input code while providing syntax sugar translations,
# as well as replacing ambiguous characters and whitespace
class Reader:
    ambiguous_characters_translations = {
        ord("|"): ord("∣"),
        ord("v"): ord("∨"),
        ord("^"): ord("∧"),
    }

    # The order here is important, as evaluating OR before NOR / XOR would replace 'or' from these statements first
    # leading to errors. In python 3.7+ the dicts are ordered by default - this may break on lower versions.
    syntax_sugar_translations = {
        "xor": "⊕",
        "nand": "∣",
        "nor": "↓",
        "not": "~",
        "and": "∧",
        "or": "∨",
        "if": "→",
        "eq": "⇔",
    }

    def __init__(self, code: str):
        self.i = 0
        self.code = self._cleanup_code(code)

    def _cleanup_code(self, code: str):
        # Remove wrapping whitespace
        _code = code.strip().lower()

        # Replace ambiguous characters with their unicode equivalents
        # This is necessary as the Wordifier will treat all ascii words as variables
        # Operators are implemented as unicode characters out of the ascii range
        _code = _code.translate(self.ambiguous_characters_translations)

        # Replace syntax sugar operators with their unicode equivalents
        # Again, ascii operators have to be converted to unicode to not be treated as variables
        for k, v in self.syntax_sugar_translations.items():
            _code = _code.replace(k, v)

        return _code

    def backstep(self) -> None:
        if self.i > 0:
            self.i -= 1

        # Do not raise if attempting to backstep before the first character
        # This is a valid scenario, in which we just stay at index 0

    def peek(self) -> str:
        if self.i < len(self.code):
            return self.code[self.i]

        raise OutOfBoundsError("Attempted to peek() outside of the text bounds")

    def next(self) -> str:
        if self.i < len(self.code):
            current = self.peek()
            self.i += 1
            return current

        raise OutOfBoundsError("Attempted to get next() outside of the text bounds")

    def has_next(self) -> bool:
        return self.i < len(self.code)

    def read_until(self, predicate: Callable[[str], bool]) -> str:
        result = ""

        while self.has_next() and predicate(self.peek()):
            result += self.next()

        return result

    def skip_whitespace(self) -> None:
        self.read_until(lambda c: c.isspace())
