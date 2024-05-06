### Wordifier
# Splits code into words for easier tokenization
# Most importantly parses the code into a list of statements, and creates words for variables
import string

from .reader import Reader


class Wordifier:
    def __init__(self, reader: Reader):
        self.reader = reader

    def wordify(self):
        words: [str] = []

        while self.reader.has_next():
            nxt = self.reader.next()

            match nxt:
                # Add a word (token) for the beginning of a sub-expressions
                case "(":
                    words.append("(")

                # Add a word (token) for the end of a sub-expression
                case ")":
                    words.append(")")

                # Skip whitespace
                case nxt if nxt in string.whitespace:
                    self.reader.skip_whitespace()

                # Wordify variables
                # Create a word until the next non-letter (whitespace or an operator)
                case nxt if nxt in string.ascii_letters:
                    self.reader.backstep()
                    token = self.reader.read_until(lambda c: c in string.ascii_letters)
                    words.append(token)

                # Wordify operators
                # Treat all non-letter and non-whitespace characters as operators
                case _:
                    words.append(nxt)

        return words
