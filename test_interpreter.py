#!/usr/bin/env python3
"""
test_interpreter.py
Regression tests against all sample inputs from the project spec.
Run with:  python3 test_interpreter.py
"""

import subprocess, sys

TESTS = [
    # (description, input_str, expected_output)
    ("Input 1 – leading zero literal",
     "x = 001;",
     "error"),

    ("Input 2 – simple assignment",
     "x_2 = 0;",
     "x_2 = 0"),

    ("Input 3 – missing semicolon / uninitialized var",
     "x = 0\ny = x;\nz = ---(x+y);",
     "error"),

    ("Input 4 – let + normal, complex expression",
     "let x = 1;\ny = 2;\nz = ---(x+y)*(x+-y);",
     "x = 1\ny = 2\nz = 3"),

    ("Input 5 – normal var in let expression",
     "let x = 1;\ny = 2;\nlet z = x + y;",
     "error, normal variables in let expression"),
]

passed = 0
for desc, src, expected in TESTS:
    result = subprocess.run(
        [sys.executable, "interpreter.py"],
        input=src, capture_output=True, text=True
    )
    got    = result.stdout.strip()
    ok     = got == expected
    status = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        print(f"[{status}] {desc}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")
        continue
    print(f"[{status}] {desc}")

print(f"\n{passed}/{len(TESTS)} tests passed.")
sys.exit(0 if passed == len(TESTS) else 1)
