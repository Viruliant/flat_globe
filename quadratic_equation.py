#!/usr/bin/env python3
# p2j -o -t quadratic_equation.ipynb quadratic_equation.py && jupyter notebook quadratic_equation.ipynb
import math
import sympy as sp

# _______________________________________________________________

# Quadratic Equation

# Define symbols
x, a, b, c = sp.symbols('x a b c')

# ## Derivation of the Quadratic Formula

# 1. Start with the standard quadratic equation
eq = sp.Eq(a * x**2 + b * x + c, 0)
display(eq)

# 2. Divide by 'a' and move the constant term to the right side
# Operation: Subtract c from both sides, then divide by a
eq = sp.Eq(x**2 + (b / a) * x, -c / a)
display(eq)

# 3 & 4. Complete the square by adding (b / (2a))^2 to both sides
# Operation: Calculate h^2 = (b / 2a)^2 and add to both sides
h_sq = (b / (2 * a))**2
eq = sp.Eq(eq.lhs + h_sq, eq.rhs + h_sq)
display(eq)

# 5. Factor the left side as (x + h)^2 and simplify the right side
# Operation: Rewrite LHS as a squared binomial and simplify RHS
h = b / (2 * a)
factored_lhs = (x + h)**2
simplified_rhs = sp.simplify(eq.rhs)
eq = sp.Eq(factored_lhs, simplified_rhs)
display(eq)

# 6. Take the square root of both sides and solve for x
# Operation: Apply square root and isolate x (yielding plus/minus)
solutions = sp.solve(eq, x)
for i, sol in enumerate(solutions, 1):
    display(sp.Eq(sp.Symbol(f'x_{i}'), sp.simplify(sol)))