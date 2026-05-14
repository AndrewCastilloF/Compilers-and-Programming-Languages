"""
tokenizer.py - Lexical analysis for the simple integer assignment language.

Tokens:
    LET    : 'let'
    IDENT  : identifier (letter/underscore followed by letters/digits/underscores)
    NUM    : integer literal (0, or NonZeroDigit Digit*)
    ASSIGN : '='
    SEMI   : ';'
    PLUS   : '+'
    MINUS  : '-'
    STAR   : '*'
    LPAREN : '('
    RPAREN : ')'
    EOF    : end of input
"""

# ---------------------------------------------------------------------------
# Token types
# ---------------------------------------------------------------------------

TT_LET    = 'LET'
TT_IDENT  = 'IDENT'
TT_NUM    = 'NUM'
TT_ASSIGN = 'ASSIGN'
TT_SEMI   = 'SEMI'
TT_PLUS   = 'PLUS'
TT_MINUS  = 'MINUS'
TT_STAR   = 'STAR'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF    = 'EOF'


# ---------------------------------------------------------------------------
# Token class
# ---------------------------------------------------------------------------

class Token:
    def __init__(self, ttype, value):
        self.ttype = ttype
        self.value = value

    def __repr__(self):
        return f'Token({self.ttype}, {self.value!r})'


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

def tokenize(source):
    """
    Scan source string and return a list of Token objects.
    The last token is always Token(EOF, None).
    Raises SyntaxError on any unrecognized character.
    """
    tokens = []
    i = 0
    n = len(source)

    while i < n:
        # --- Skip whitespace ---
        if source[i].isspace():
            i += 1
            continue

        # --- Identifier or keyword ---
        if source[i].isalpha() or source[i] == '_':
            j = i
            while j < n and (source[j].isalnum() or source[j] == '_'):
                j += 1
            word = source[i:j]
            if word == 'let':
                tokens.append(Token(TT_LET, 'let'))
            else:
                tokens.append(Token(TT_IDENT, word))
            i = j
            continue

        # --- Numeric literal ---
        if source[i].isdigit():
            j = i
            while j < n and source[j].isdigit():
                j += 1
            tokens.append(Token(TT_NUM, source[i:j]))
            i = j
            continue

        # --- Single-character tokens ---
        ch = source[i]
        if   ch == '=': tokens.append(Token(TT_ASSIGN, '='))
        elif ch == ';': tokens.append(Token(TT_SEMI,   ';'))
        elif ch == '+': tokens.append(Token(TT_PLUS,   '+'))
        elif ch == '-': tokens.append(Token(TT_MINUS,  '-'))
        elif ch == '*': tokens.append(Token(TT_STAR,   '*'))
        elif ch == '(': tokens.append(Token(TT_LPAREN, '('))
        elif ch == ')': tokens.append(Token(TT_RPAREN, ')'))
        else:
            raise SyntaxError(f"Unexpected character: {ch!r}")
        i += 1

    tokens.append(Token(TT_EOF, None))
    return tokens


# ---------------------------------------------------------------------------
# Run tokenizer standalone for debugging:  python3 tokenizer.py < program.txt
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    source = sys.stdin.read()
    try:
        tokens = tokenize(source)
        for tok in tokens:
            print(tok)
    except SyntaxError as e:
        print(f"error: {e}")
