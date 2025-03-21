# FlipFlop

## FlipFlow is an interpreted language for evaluating discrete math expressions

### Syntax

FlipFlip supports two types of syntax:

- Human: `(p or q) and not r`
- Mathematical: `(p ∨ q) ∧ ~r`

The math syntax will cast regular characters `|`, `v`, `^` to their mathematical (non-ascii) equivalents `∣`, `∨`, `∧`.

The variables are not limited to single characters, you can use long names if you prefer: `test or tst`, but using 
numbers is not supported.

### Usage

#### Library

Install as a regular dependency:

```bash
pip install git+https://github.com/MilyMilo/flipflop.git # with pip
uv add git+https://github.com/MilyMilo/flipflop.git # with uv
```

FlipFlop can be used as a library:

```python
from flipflop import flipflop

result = flipflop("p or q")
```

Which returns a dictionary with the truth table:
```python
{
    'header': ['p', 'q', '(p OR q)'],
    'values': [
        [False, False, False], 
        [False, True, True], 
        [True, False, True], 
        [True, True, True]
    ], 
    'is_tautology': False
}
```

#### CLI

Install using a global command / tool manager:

```bash
pipx install git+https://github.com/MilyMilo/flipflop.git && flipflop # with pipx
uvx --from 'git+https://github.com/MilyMilo/flipflop.git' flipflop # with uvx
```

FlipFlop exposes a simple CLI:

```bash
python -m flipflop -i "p or q"
```

Which prints out a nice truth table:

```text
┌───────┬───────┬────────────┐
│ p     │ q     │ (p OR q)   │
├───────┼───────┼────────────┤
│ False │ False │ False      │
├───────┼───────┼────────────┤
│ False │ True  │ True       │
├───────┼───────┼────────────┤
│ True  │ False │ True       │
├───────┼───────┼────────────┤
│ True  │ True  │ True       │
└───────┴───────┴────────────┘
Expression IS NOT a tautology
```

##### Additional Parameters

```bash
python -m flipflop --help
```

```text
Usage: python -m flipflop [OPTIONS]

Options:
  -i, --inline-input TEXT  Singular inline expression to execute
  -s, --simple             Only include variables and final expression
  -t, --table-format TEXT  Chosen table format (see python-tabulate for more details)
  --help                   Show this message and exit.
```

Currently, there aren't many options:

- `-s / --simple` - Will only include the variables and final expression in the truth table. 
By default, if the expression is more complex, the truth table will contain the state of each 
individual sub expression.
- `-t / --table-format` - Allows to specify the table format, as per [python-tabulate](https://github.com/astanin/python-tabulate)
For example you could generate a nice table for GitHub markdown:

```bash
python -m flipflop -i "p or q" -t github
```

```text
| p     | q     | (p OR q)   |
|-------|-------|------------|
| False | False | False      |
| False | True  | True       |
| True  | False | True       |
| True  | True  | True       |
```

| p     | q     | (p OR q)   |
|-------|-------|------------|
| False | False | False      |
| False | True  | True       |
| True  | False | True       |
| True  | True  | True       |


### Testing

Some unit tests have been implemented in the `./tests`. 
You can run them by using `make test` or just `python -m unittest discover -s tests`


### OS and Python Version Support

This is a fun side-project, so I've only tested it in my environment (OSX / Python 3.12).
I do not know whether it'll work on Windows and other python versions. 
It utilizes match statements and some more modern typing, so I'd recommend using python 3.12.
