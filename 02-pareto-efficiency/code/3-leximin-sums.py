#!python3

"""
Using cvxpy - the contex optimization package of Python -
to find a leximin-egalitarian ditision.

AUTHOR: Erel Segal-Halevi
SINCE:  2024-01
"""

import cvxpy
from itertools import combinations

num_of_players = 4

xw = cvxpy.Variable(num_of_players)  # fractions of wood
xo = cvxpy.Variable(num_of_players)  # fractions of oil
xs = cvxpy.Variable(num_of_players)  # fractions of steel

A=0
B=1
C=2
D=3

utilities = [
    xw[A]*4,                  
    xo[B]*3,                  
    xw[C]*5+xo[C]*5+xs[C]*10, 
    xw[D]*5+xo[D]*5+xs[D]*10] 

fixed_constraints = \
    [0<=t for t in xw] + [t<=1 for t in xw] + \
    [0<=t for t in xo] + [t<=1 for t in xo] + \
    [0<=t for t in xs] + [t<=1 for t in xs] + \
    [sum(xw)==1, sum(xo)==1, sum(xs)==1]

print("\nITERATION 1: Egalitarian division")

min_utility = cvxpy.Variable()    # smallest utility of a single agent
prob = cvxpy.Problem(
    cvxpy.Maximize(min_utility),
    constraints = fixed_constraints + [min_utility <= u for u in utilities])
prob.solve()
print("optimal value: ", prob.value)
print("Utilities: ", [u.value for u in utilities])
print(f"  Wood: {xw.value.round(2)},\n  oil: {xo.value.round(2)},\n  steel: {xs.value.round(2)}")
# min_utility = 3

print("\nITERATION 2: Max the smallest sum of two:")

min_utility_of_two = cvxpy.Variable()    
prob = cvxpy.Problem(
    cvxpy.Maximize(min_utility_of_two),
    constraints = fixed_constraints + 
        [min_utility.value <= u for u in utilities] +
        [min_utility_of_two  <= u+v for u,v in combinations(utilities,2)]
    )
prob.solve()
print("optimal value: ", prob.value)
print("Utilities: ", [u.value for u in utilities])
print(f"  Wood: {xw.value.round(2)},\n  oil: {xo.value.round(2)},\n  steel: {xs.value.round(2)}")
# min_utility_of_two = 7

print("\nITERATION 3: Max the smallest sum of three")

min_utility_of_three = cvxpy.Variable()  
prob = cvxpy.Problem(
    cvxpy.Maximize(min_utility_of_three),
    constraints = fixed_constraints + 
        [min_utility.value <= u for u in utilities] +
        [min_utility_of_two.value  <= u+v for u,v in combinations(utilities,2)] +
        [min_utility_of_three  <= u+v+w for u,v,w in combinations(utilities,3)] 
    )
prob.solve()
print("optimal value: ", prob.value)
print("Utilities: ", [u.value for u in utilities])
print(f"  Wood: {xw.value.round(2)},\n  oil: {xo.value.round(2)},\n  steel: {xs.value.round(2)}")
# min_utility_of_three = 12


print("\nITERATION 4: Max the smallest sum of four")

min_utility_of_four = cvxpy.Variable()  
prob = cvxpy.Problem(
    cvxpy.Maximize(min_utility_of_four),
    constraints = fixed_constraints + 
        [min_utility.value <= u for u in utilities] +
        [min_utility_of_two.value  <= u+v for u,v in combinations(utilities,2)] +
        [min_utility_of_three.value  <= u+v+w for u,v,w in combinations(utilities,3)] +
        [min_utility_of_four  <= u+v+w+x for u,v,w,x in combinations(utilities,4)] 
    )
prob.solve()
print("optimal value: ", prob.value)
print("Utilities: ", [u.value for u in utilities])
print(f"  Wood: {xw.value.round(2)},\n  oil: {xo.value.round(2)},\n  steel: {xs.value.round(2)}")
