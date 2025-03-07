#!python3

"""
A demo of cvxpy - the convex-optimization package of python.

EXAMPLE PROBLEM:

Minimize     (x-y)^2 
subject to   x+y==1
"""

import cvxpy

# x, y = cvxpy.Variable(2)
# prob = cvxpy.Problem(objective=cvxpy.Maximize(x*y), constraints=[x+y==10, x>=0, y>=0])
# # prob = cvxpy.Problem(objective=cvxpy.Maximize(cvxpy.log(x)+cvxpy.log(y)), constraints=[x+y==10, x>=0, y>=0])
# prob.solve()  # cvxpy.error.DCPError: Problem does not follow DCP rules. Specifically: The objective is not DCP. Its following subexpressions are not: var1[0] @ var1[1]
# print("status:", prob.status)
# print("optimal value", prob.value)
# print("optimal var", x.value, y.value)

t = 2/3
x  = cvxpy.Variable(1)
prob = cvxpy.Problem(objective=cvxpy.Maximize(cvxpy.log(x) + cvxpy.log(1-t*x)), constraints=[x>=0, x<=1])
prob.solve()  # cvxpy.error.DCPError: Problem does not follow DCP rules. Specifically: The objective is not DCP. Its following subexpressions are not: var1[0] @ var1[1]
print("status:", prob.status)
print("optimal value", prob.value)
print("optimal var", x.value)

# x= 1/2t
