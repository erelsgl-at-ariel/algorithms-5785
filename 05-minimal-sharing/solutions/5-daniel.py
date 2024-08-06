from typing import List, Literal
import numpy as np
from copy import deepcopy

import time
from itertools import product, combinations
import matplotlib.pyplot as plt

from egal_allocation_discrete import assert_values_valid
from pareto_eff_netx import is_pareto_efficient

def state_space_search_min_sharing(values: List[List[float]],
                                            is_prune_a=False,
                                            is_prune_b=False,
                                            is_prune_c=False,
                                            is_print=True
                                            ):
    #state space search

    def allocate_item(state, item):
        def add_ith_value(tup, i):
            return tup[:i]+(tup[i]+values[i][item], *tup[i+1:])

        def add_ith_item(tup, i):
            curr_set = tup[i]
            curr_set.add(item)
            return tup[:i]+(curr_set, *tup[i+1:])

        values_so_far, n_items_allocated, allocated_items_so_far = state
        new_allocations = [(add_ith_value(values_so_far, i), n_items_allocated + 1, add_ith_item(deepcopy(allocated_items_so_far), i)) for i in range(n_participants)]
        
        return new_allocations

    def prune_a(state_space):
        unique_states = set([state[0] for state in state_space])
        new_unique_states = []
        for state in state_space:
            if state[0] in unique_states:
                unique_states.remove(state[0])
                new_unique_states.append(state)
        return new_unique_states

    def prune_b(state_space):
        def pessimistic_bound(state):
            curr_values, curr_n_items_allocated, curr_items = state
            remaining_items = set(range(n_items)) - set(range(curr_n_items_allocated))

            final_items = tuple(curr_items[i].union(remaining_items) if i==0 else curr_items[i] for i in range(n_participants)) # give everything to 0
            assert set().union(*final_items) == set(range(n_items)), f'{set().union(*final_items)}'
            sums = tuple(sum(values[i][j] for j in final_items[i]) for i in range(n_participants))
            
            return min(sums)
        
        def optimistic_bound(state):
            curr_values, curr_n_items_allocated, curr_items = state
            remaining_items = set(range(n_items)) - set(range(curr_n_items_allocated))

            final_items = tuple(curr_items[i].union(remaining_items) for i in range(n_participants))

            sums = tuple(sum(values[i][j] for j in final_items[i]) for i in range(n_participants))
            return min(sums)
            
        def check_state(state):
            pes = pessimistic_bound(state)
            opt = optimistic_bound(state)

            return state[1]==n_items or pes < opt
            

        new_state_space = list(filter(check_state, state_space))

        return new_state_space

    def prune_c(state_space):
        def is_sorted(state):
            curr_values, curr_n_items_allocated, curr_items = state
            if curr_n_items_allocated == 0 or len(curr_items[0]) == 0 or len(curr_items[1]) == 0:
                return True
            min_a_ratio = min(ratios[j] for j in curr_items[0])
            return all(ratios[j] <= min_a_ratio for j in curr_items[1])
        
        return list(filter(is_sorted, state_space))

    n_participants, n_items = assert_values_valid(values)
    assert n_participants == 2, 'Only 2 participants supported'
    assert all(sum(values[i])==100 for i in range(n_participants)), 'Sum of values for each participant must be 100'
    
    ratios = [values[0][j]/values[1][j] for j in range(n_items)]

    # alloc: (values_so_far (n_participants, ),  n_items_allocated_so_far, allocated_items_so_far (n_participants, set))
    empty_allocation = tuple([0]*n_participants), 0, tuple(set() for _ in range(n_participants))
    state_space = [empty_allocation]
    curr_round = 0
    while curr_round < n_items:
        if state_space[0][1] != curr_round:
            curr_round+=1
            if curr_round == n_items:
                break
            
            if is_prune_a:
                state_space=prune_a(state_space)
            if is_prune_b:
                state_space=prune_b(state_space)
            
            if is_prune_c:
                state_space=prune_c(state_space)

        state = state_space.pop(0)
        state_space.extend(allocate_item(state, state[1]))
    
    # state_space = [((72, 72), 5, ({3,4}, {0,1,2}))]

    # if rule == 'egalitarian':
    #     rule_fn = lambda state: min(state[0])
    # elif rule == 'max_product':
    #     rule_fn = lambda state: np.prod(state[0])
    # print(f'Number of states: {len(state_space)}')
    # print(state_space)
    state_space = list(filter(lambda state: state[0][0]==state[0][1], state_space))
    
    if len(state_space) == 0:
        if is_print:
            print('No valid allocation found with no sharing')
        return None, None
    best_allocation = max(state_space, key=lambda state: sum(state[0]))
    acc_values, _, items = best_allocation
    if is_print:
        for i in range(n_participants):
            print(f'Participant {i} gets items {items[i]} with value {acc_values[i]}')
            
    assert is_pareto_efficient(values, [list(map(lambda x: 1 if x in items[i] else 0, range(n_items))) for i in range(n_participants)])
    
    return acc_values, items

if __name__ == '__main__':
    values = [[15, 15, 40, 30], [40, 25, 30, 5]]
    state_space_search_min_sharing(values, is_prune_a=True, is_prune_b=True, is_prune_c=True, is_print=True)
    
    values = [[50, 50], [50, 50]]
    state_space_search_min_sharing(values, is_prune_a=True, is_prune_b=True, is_prune_c=True, is_print=True)
    
    values = [[10, 6, 12, 22, 50], [15, 36, 21, 8, 20]]
    state_space_search_min_sharing(values, is_prune_a=True, is_prune_b=False, is_prune_c=True, is_print=True)
    