### Flip-Flop Logical Interpreted Language
from flipflop.core import Interpreter, Lexer, Parser, Reader, Wordifier


def flipflop(code: str, full: bool = True):
    words = Wordifier(Reader(code)).wordify()
    tokens = Lexer(words).tokenize()
    ast = Parser(tokens).parse()
    return Interpreter(ast).evaluate(full=full)
