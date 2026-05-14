# Simple Integer Language Interpreter

A recursive-descent interpreter for a simple integer assignment language, built in Python 3 with no external dependencies. The pipeline is split across three stages — tokenizer, parser, and interpreter — each in its own module.

## Running the Interpreter

```bash
python3 interpreter.py < program.txt
```

Or pipe directly:

```bash
echo "let x = 1; y = 2; z = x + y;" | python3 interpreter.py
```

## Language

A program is a sequence of assignment statements. All variables are integers.

Two kinds of assignments:

- **Normal:** `x = Exp;` — `x` can reference any previously assigned variable.
- **Let:** `let x = Exp;` — `x` is single-assignment; the RHS may only use constants or other `let` variables.

### Grammar

```
Program      : Assignment*
Assignment   : Identifier = Exp ;
             | let Identifier = Exp ;
Exp          : Exp + Term | Exp - Term | Term
Term         : Term * Fact | Fact
Fact         : ( Exp ) | - Fact | + Fact | Literal | Identifier
Identifier   : Letter (Letter | Digit)*
Letter       : a–z | A–Z | _
Literal      : 0 | NonZeroDigit Digit*
NonZeroDigit : 1–9
Digit        : 0–9
```

## Errors

| Condition | Output |
|-----------|--------|
| Syntax error (bad token, leading zero, missing `;`, etc.) | `error` |
| Uninitialized variable | `error` |
| Normal variable referenced in a `let` expression | `error, normal variables in let expression` |

If no error is found, every variable is printed in declaration order:
```
name = value
```

## Sample Inputs and Outputs

```
Input:   x = 001;
Output:  error

Input:   x_2 = 0;
Output:  x_2 = 0

Input:   x = 0
         y = x;
         z = ---(x+y);
Output:  error

Input:   let x = 1;
         y = 2;
         z = ---(x+y)*(x+-y);
Output:  x = 1
         y = 2
         z = 3

Input:   let x = 1;
         y = 2;
         let z = x + y;
Output:  error, normal variables in let expression
```

## Project Structure

```
.
├── tokenizer.py        # Lexical analysis: source → tokens
├── parser.py           # Parsing: tokens → AST
├── interpreter.py      # Semantic checks + evaluation (main entry point)
└── test_interpreter.py # Regression tests for all sample cases
```

Each module can also be run standalone for debugging:

```bash
echo "let x = 1;" | python3 tokenizer.py   # prints token stream
echo "let x = 1;" | python3 parser.py      # prints AST nodes
```

## Running Tests

```bash
python3 test_interpreter.py
```

## Requirements

- Python 3.6+
- No external packages
