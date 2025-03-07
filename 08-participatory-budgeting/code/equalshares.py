"""
Code from the official website of the Method of Equal Shares:
https://equalshares.net/implementation/computation
"""

import numpy as np

def equal_shares(N, C, cost, approvers, B):
    """
    * Approval ballots,
    * Breaking ties In favor of lower cost, then higher vote count.
    * Completion method: Repeated increase of voter budgets by 1 currency unit (Add1)
    * Use floating point numbers (faster to compute, recommended for testing)
    """
    mes = equal_shares_fixed_budget(N, C, cost, approvers, B)
    # add1 completion
    # start with integral per-voter budget
    budget = int(B / len(N)) * len(N)
    current_cost = sum(cost[c] for c in mes)
    while True:
        # is current outcome exhaustive?
        is_exhaustive = True
        for extra in C:
            if extra not in mes and current_cost + cost[extra] <= B:
                is_exhaustive = False
                break
        # if so, stop
        if is_exhaustive:
            break
        # would the next highest budget work?
        next_budget = budget + len(N)
        next_mes = equal_shares_fixed_budget(N, C, cost, approvers, next_budget)
        current_cost = sum(cost[c] for c in next_mes)
        if current_cost <= B:
            # yes, so continue with that budget
            budget = next_budget
            mes = next_mes
        else:
            # no, so stop
            break
    return mes

def break_ties(N, C, cost, approvers, choices):
    remaining = choices.copy()
    best_cost = min(cost[c] for c in remaining)
    remaining = [c for c in remaining if cost[c] == best_cost]
    best_count = max(len(approvers[c]) for c in remaining)
    remaining = [c for c in remaining if len(approvers[c]) == best_count]
    return remaining

def equal_shares_fixed_budget(N, C, cost, approvers, B):
    print("\n  MES WITH BUDGET= ", B)
    budget = {i: B / len(N) for i in N}
    remaining = {} # map a remaining candidate to previous effective vote count
    for c in C:
        if cost[c] > 0 and len(approvers[c]) > 0:
            remaining[c] = len(approvers[c])       # effective vote count for candidate c
    winners = []
    while True:
        print("\n  Budgets: ", budget)
        best = []
        best_eff_vote_count = 0
        # go through remaining candidates in order of decreasing previous effective vote count
        remaining_sorted = sorted(remaining, key=lambda c: remaining[c], reverse=True)
        for c in remaining_sorted:
            previous_eff_vote_count = remaining[c]
            if previous_eff_vote_count < best_eff_vote_count:
                # c cannot be better than the best so far
                break
            money_behind_now = sum(budget[i] for i in approvers[c])
            if money_behind_now < cost[c]:
                # c is not affordable
                del remaining[c]   # remove candidate c from the dict of effective vote counts
                continue
            # calculate the new effective vote count of c
            approvers[c].sort(key=lambda i: budget[i])
            paid_so_far = 0
            denominator = len(approvers[c])
            for i in approvers[c]:
                # compute payment if remaining approvers pay equally
                max_payment = (cost[c] - paid_so_far) / denominator
                eff_vote_count = cost[c] / max_payment
                if max_payment > budget[i]:
                    # i cannot afford the payment, so pays entire remaining budget
                    paid_so_far += budget[i]
                    denominator -= 1
                else:
                    # i (and all later approvers) can afford the payment; stop here
                    remaining[c] = eff_vote_count
                    if eff_vote_count > best_eff_vote_count:
                        best_eff_vote_count = eff_vote_count
                        best = [c]
                    elif eff_vote_count == best_eff_vote_count:
                        best.append(c)
                    break
        print("  Best projects: ", best)
        if not best:
            # no remaining candidates are affordable
            break
        best = break_ties(N, C, cost, approvers, best)
        if len(best) > 1:
            best.sort()
        best = best[0]
        print("  Best best project: ", best)
        winners.append(best)
        del remaining[best]
        # charge the approvers of best
        best_max_payment = cost[best] / best_eff_vote_count
        for i in approvers[best]:
            if budget[i] > best_max_payment:
                budget[i] -= best_max_payment
            else:
                budget[i] = 0
    return winners

def equal_shares_budget_aggregation(votes:list[list[float]], minima:list):
    print("votes: ",votes)
    num_voters = len(votes)
    N = list(range(num_voters))        # voters

    num_issues   = len(votes[0])
    total_budget = sum(votes[0])

    C = []
    cost = {}
    approvers = {}
    for issue in range(num_issues):
        min_per_issue = minima[issue]
        if min_per_issue==0:
            min_per_issue=1
        for part in range(min_per_issue,total_budget+1):
            candidate_name = f"{issue}-{part:0>2}"
            C.append(candidate_name)
            cost[candidate_name]=min_per_issue if part==min_per_issue else 1
            approvers[candidate_name] = [i for i in range(num_voters) if votes[i][issue] >= part]

    funded_candidates = equal_shares_fixed_budget(N, C, cost, approvers, total_budget)

    budget = {}
    for issue in range(num_issues):
        amount = max([candidate for candidate in funded_candidates if candidate.startswith(f"{issue}-")])
        budget[issue] = amount

    return budget



def random_partition(total_budget:int, count:int):
    """
    >>> np.random.seed(1)
    >>> list(random_partition(100, 2))
    [37, 63]
    >>> np.random.seed(1)
    >>> list(random_partition(100, 3))
    [37, 43, 20]
    """
    result = np.zeros(count, dtype=np.int32)
    for i in range(count-1):
        next_part = np.random.randint(0,total_budget)
        result[i] = next_part
        total_budget -= next_part
    result[-1] = total_budget
    return result
    


if __name__=="__main__":
    import doctest
    # print(doctest.testmod())
    # print(equal_shares_fixed_budget(N=[1,2,3], C=["x","y","z"], cost={"x":100,"y":200,"z":300}, approvers={"x":[1],"y":[2],"z":[3]}, B=600))
    # print(equal_shares(N=["a","b","c"], C=["x","y","z"], cost={"x":100,"y":200,"z":300}, approvers={"x":["a"],"y":["b"],"z":["c"]}, B=600))
    # print(equal_shares_budget_aggregation([random_partition(100,3),random_partition(100,3)]))
    # print(equal_shares_budget_aggregation([[20,20,60],[40,40,20]]))

    omer_example = [
        [18,2],
        [18,2],
        [10,10],
        [0,12]
    ]
    omer_example_complete_budget = [
        [18,2,0],
        [18,2,0],
        [10,10,0],
        [0,12,8]
    ]

    # print(equal_shares_budget_aggregation(omer_example, minima=[10,2]))
    print(equal_shares_budget_aggregation([list(reversed(c)) for c in omer_example], minima=list(reversed([10,2]))))
