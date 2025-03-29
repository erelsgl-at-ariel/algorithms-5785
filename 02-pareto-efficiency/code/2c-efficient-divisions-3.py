#!python3

"""
Using cvxpy - the convex optimization package of Python -
to find an egalitarian division.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-10
"""

import cvxpy
import numpy as np

print("\n\n\nPROBLEM #1")
print("Three resources (Apple, Banana, Clementine) has to be divided among two people with values:")
print("8 4 2")
print("2 6 5")

xa, xb, xc = cvxpy.Variable(3)   # fractions of the three regions given to Ami

utility_ami =  xa*8 + xb*4 + xc*2
utility_tami = (1-xa)*2 + (1-xb)*6 + (1-xc)*5

budget_ami = 60
budget_tami = 40

print("\nmaximize the sum of logarithms:")
prob = cvxpy.Problem(
    cvxpy.Maximize(budget_ami * cvxpy.log(utility_ami) + budget_tami * cvxpy.log(utility_tami)),
    constraints = [0 <= xa, xa <= 1, 0 <= xb, xb <= 1, 0 <= xc, xc <= 1])
prob.solve()
print("status:", prob.status)
print("optimal value", prob.value)
print("Fractions given to Ami: ", np.round(xa.value,3), np.round(xb.value,3), np.round(xc.value,3))
print("Utility of Ami", utility_ami.value)
print("Utility of Tami", utility_tami.value)
