"""
parser.py - Parsing and AST construction for the simple integer assignment language.

Grammar:
    Program     : Assignment*
    Assignment  : Identifier = Exp ;
                | let Identifier = Exp ;
    Exp         : Exp + Term | Exp - Term | Term
    Term        : Term * Fact | Fact
    Fact        : ( Exp ) | - Fact | + Fact | Literal | Identifier
    Identifier  : Letter (Letter | Digit)*
    Letter      : a-z | A-Z | _
    Literal     : 0 | NonZeroDigit Digit*
    NonZeroDigit: 1-9
    Digit       : 0-9

AST Nodes:
    AssignNode(is_let, name, expr)
    BinOpNode(op, left, right)       op in {'+', '-', '*'}
    UnaryOpNode(op, operand)         op in {'+', '-'}
    LiteralNode(value)               value: int
    IdentNode(name)                  name: str
"""

from tokenizer import (
    tokenize,
    TT_LET, TT_IDENT, TT_NUM, TT_ASSIGN, TT_SEMI,
    TT_PLUS, TT_MINUS, TT_STAR, TT_LPAREN, TT_RPAREN, TT_EOF
)


# ---------------------------------------------------------------------------
# AST node definitions
# ---------------------------------------------------------------------------

class AssignNode:
    """Represents one assignment statement."""
    def __init__(self, is_let, name, expr):
        self.is_let = is_let   # bool — True if declared with 'let'
        self.name   = name     # str  — variable name
        self.expr   = expr     # AST node — right-hand side expression

    def __repr__(self):
        kw = 'let ' if self.is_let else ''
        return f'AssignNode({kw}{self.name} = {self.expr!r})'


class BinOpNode:
    """Represents a binary operation: left op right."""
    def __init__(self, op, left, right):
        self.op    = op      # str: '+', '-', or '*'
        self.left  = left    # AST node
        self.right = right   # AST node

    def __repr__(self):
        return f'BinOpNode({self.op!r}, {self.left!r}, {self.right!r})'


class UnaryOpNode:
    """Represents a unary operation: op operand."""
    def __init__(self, op, operand):
        self.op      = op       # str: '+' or '-'
        self.operand = operand  # AST node

    def __repr__(self):
        return f'UnaryOpNode({self.op!r}, {self.operand!r})'


class LiteralNode:
    """Represents an integer literal."""
    def __init__(self, value):
        self.value = value   # int

    def __repr__(self):
        return f'LiteralNode({self.value})'


class IdentNode:
    """Represents a variable reference."""
    def __init__(self, name):
        self.name = name   # str

    def __repr__(self):
        return f'IdentNode({self.name!r})'


# ---------------------------------------------------------------------------
# Recursive-descent parser
# ---------------------------------------------------------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def peek(self):
        """Return the current token without consuming it."""
        return self.tokens[self.pos]

    def consume(self, expected_type=None):
        """
        Consume and return the current token.
        If expected_type is given, raise SyntaxError if it doesn't match.
        """
        tok = self.tokens[self.pos]
        if expected_type and tok.ttype != expected_type:
            raise SyntaxError(
                f"Expected {expected_type} but got {tok.ttype} ({tok.value!r})"
            )
        self.pos += 1
        return tok

    # --- Program ---

    def parse_program(self):
        """Program : Assignment*"""
        stmts = []
        while self.peek().ttype != TT_EOF:
            stmts.append(self.parse_assignment())
        return stmts

    # --- Assignment ---

    def parse_assignment(self):
        """
        Assignment : Identifier = Exp ;
                   | let Identifier = Exp ;
        """
        if self.peek().ttype == TT_LET:
            self.consume(TT_LET)
            is_let = True
        else:
            is_let = False

        name_tok = self.consume(TT_IDENT)
        self.consume(TT_ASSIGN)
        expr = self.parse_exp()
        self.consume(TT_SEMI)
        return AssignNode(is_let, name_tok.value, expr)

    # --- Exp (left-recursive → iterative) ---

    def parse_exp(self):
        """Exp : Exp + Term | Exp - Term | Term"""
        node = self.parse_term()
        while self.peek().ttype in (TT_PLUS, TT_MINUS):
            op    = self.consume().value
            right = self.parse_term()
            node  = BinOpNode(op, node, right)
        return node

    # --- Term (left-recursive → iterative) ---

    def parse_term(self):
        """Term : Term * Fact | Fact"""
        node = self.parse_fact()
        while self.peek().ttype == TT_STAR:
            op    = self.consume().value
            right = self.parse_fact()
            node  = BinOpNode(op, node, right)
        return node

    # --- Fact ---

    def parse_fact(self):
        """Fact : ( Exp ) | - Fact | + Fact | Literal | Identifier"""
        tok = self.peek()

        # Parenthesised expression
        if tok.ttype == TT_LPAREN:
            self.consume(TT_LPAREN)
            node = self.parse_exp()
            self.consume(TT_RPAREN)
            return node

        # Unary minus
        if tok.ttype == TT_MINUS:
            self.consume(TT_MINUS)
            return UnaryOpNode('-', self.parse_fact())

        # Unary plus
        if tok.ttype == TT_PLUS:
            self.consume(TT_PLUS)
            return UnaryOpNode('+', self.parse_fact())

        # Numeric literal
        if tok.ttype == TT_NUM:
            self.consume(TT_NUM)
            raw = tok.value
            # Reject leading zeros: only '0' alone is valid; '001', '07', etc. are not
            if len(raw) > 1 and raw[0] == '0':
                raise SyntaxError(f"Invalid literal (leading zero): {raw!r}")
            return LiteralNode(int(raw))

        # Identifier (variable reference)
        if tok.ttype == TT_IDENT:
            self.consume(TT_IDENT)
            return IdentNode(tok.value)

        raise SyntaxError(
            f"Unexpected token in expression: {tok.ttype} ({tok.value!r})"
        )


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def parse(source):
    """Tokenize source and return a list of AssignNode AST nodes."""
    tokens = tokenize(source)
    return Parser(tokens).parse_program()


# ---------------------------------------------------------------------------
# Run parser standalone for debugging:  python3 parser.py < program.txt
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    source = sys.stdin.read()
    try:
        stmts = parse(source)
        for stmt in stmts:
            print(stmt)
    except SyntaxError as e:
        print(f"error: {e}")
