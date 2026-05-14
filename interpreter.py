"""
interpreter.py - Semantic analysis and execution for the simple integer assignment language.

Responsibilities:
    1. Detect use of uninitialized variables.
    2. Detect normal (non-let) variables used inside a let expression.
    3. Evaluate all assignments in order.
    4. Print each variable's final value as "name = value".

Usage:
    python3 interpreter.py < program.txt
"""

import sys

from parser import (
    parse,
    AssignNode, BinOpNode, UnaryOpNode, LiteralNode, IdentNode
)


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------

class Interpreter:
    def __init__(self):
        # Maps variable name → integer value for all assigned variables
        self.env = {}
        # Tracks which variables were declared with 'let'
        self.let_vars = set()
        # Preserves declaration order for final output
        self.order = []

    def run(self, stmts):
        """Execute a list of AssignNode statements, then print results."""
        for stmt in stmts:
            self._exec_assignment(stmt)
        for name in self.order:
            print(f"{name} = {self.env[name]}")

    # --- Statement execution ---

    def _exec_assignment(self, node):
        if node.is_let:
            # Validate RHS before evaluating: no normal variables allowed
            self._check_let_expr(node.expr)

        value = self._eval(node.expr)

        if node.name not in self.env:
            self.order.append(node.name)
        self.env[node.name] = value

        if node.is_let:
            self.let_vars.add(node.name)

    # --- Let expression checker ---

    def _check_let_expr(self, node):
        """
        Walk the expression tree and raise an error if:
          - any referenced variable is uninitialized, or
          - any referenced variable was NOT declared with 'let'
        """
        if isinstance(node, IdentNode):
            if node.name not in self.env:
                raise NameError(f"Uninitialized variable: {node.name!r}")
            if node.name not in self.let_vars:
                raise TypeError("error, normal variables in let expression")

        elif isinstance(node, LiteralNode):
            pass  # literals are always allowed

        elif isinstance(node, UnaryOpNode):
            self._check_let_expr(node.operand)

        elif isinstance(node, BinOpNode):
            self._check_let_expr(node.left)
            self._check_let_expr(node.right)

    # --- Expression evaluator ---

    def _eval(self, node):
        if isinstance(node, LiteralNode):
            return node.value

        if isinstance(node, IdentNode):
            if node.name not in self.env:
                raise NameError(f"Uninitialized variable: {node.name!r}")
            return self.env[node.name]

        if isinstance(node, UnaryOpNode):
            v = self._eval(node.operand)
            return -v if node.op == '-' else v

        if isinstance(node, BinOpNode):
            l = self._eval(node.left)
            r = self._eval(node.right)
            if node.op == '+': return l + r
            if node.op == '-': return l - r
            if node.op == '*': return l * r

        raise RuntimeError(f"Unknown AST node: {type(node)}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    source = sys.stdin.read()
    try:
        stmts = parse(source)
        interp = Interpreter()
        interp.run(stmts)
    except SyntaxError:
        print("error")
    except NameError:
        print("error")
    except TypeError as e:
        msg = str(e)
        if "normal variables in let expression" in msg:
            print("error, normal variables in let expression")
        else:
            print("error")


if __name__ == '__main__':
    main()
