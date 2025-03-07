"""
cvxpy for piecewise-linear valuations
"""

import cvxpy

# Create two scalar optimization variables.
ps = cvxpy.Variable()
pm = cvxpy.Variable()

# Build the constraints.
constraints1 = [
    ps + pm >= 1000,
    3000 <= ps,
    3000 <= pm,
    -1800-ps >= -11000-pm,
    -11000-pm >= -4500-ps,
    ]

constraints2 = [
    ps + pm >= 1000,
    3000 <= ps,
    200 <= pm, pm <= 3000,
    -1800-ps >= 1000-5*pm,
    1000-5*pm >= -4500-ps,
    ]


constraints = [
    ps + pm >= 1000,
    400 <= ps, ps <= 3000,
    200 <= pm, pm <= 3000,
    1200-2*ps >= 1000-5*pm,
    1000-5*pm >= 1500-3*ps,
    ]


# Build an objective function.
obj = cvxpy.Minimize(ps+pm)

# Form and solve problem.
prob = cvxpy.Problem(obj, constraints)
prob.solve()  # Returns the optimal value.

print("status:", prob.status)
print(f"ps={ps.value}, pm={pm.value}")