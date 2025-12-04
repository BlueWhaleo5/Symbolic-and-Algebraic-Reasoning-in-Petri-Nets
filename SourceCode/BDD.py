import collections
from typing import Tuple, List, Optional, Dict
from pyeda.inter import *
from Parser import Parser
import numpy as np
import itertools

def bdd_reachable(pn: Parser) -> Tuple[BinaryDecisionDiagram, int]:
    
    bdd_vars = {} 
    for i, pid in enumerate(pn.place_ids):
        safe_name = f"p{i}"
        bdd_vars[pid] = bddvar(safe_name)
    
    is_conservative = _check_conservative(pn)
    print(f"Conservative: {is_conservative}")
    
    R = _marking_to_bdd(pn.M0, pn.place_ids, bdd_vars)
    
    if is_conservative:
        total_tokens = sum(pn.M0)
        constraint = _create_token_constraint(total_tokens, pn.place_ids, bdd_vars, pn)
        R = R & constraint
    
    R_old = None
    iteration = 0
    
    while R_old is None or not R.equivalent(R_old):
        iteration += 1
        R_old = R
        
        current_count = _count_actual_states(R, bdd_vars, pn.place_ids)
        print(f"Iteration {iteration}: {current_count} states")
        
        img_total = _bdd_false(bdd_vars)
        n_transitions = min(len(pn.trans_ids), pn.I.shape[0])
        
        for t_idx in range(n_transitions):
            img_bdd = _compute_transition_image(R, t_idx, pn, bdd_vars, is_conservative)
            img_total = img_total | img_bdd
        
        R_next = R | img_total
        
        if is_conservative:
            R_next = R_next & constraint
            
        R = R_next
        
        if iteration >= 50:
            print("Warning: Reached max iterations")
            break
    
    final_count = _count_actual_states(R, bdd_vars, pn.place_ids)
    print(f"COMPLETION: {final_count} reachable states")
    return R, final_count

def _check_conservative(pn):
    n_transitions = min(len(pn.trans_ids), pn.I.shape[0])
    for t_idx in range(n_transitions):
        input_sum = sum(pn.I[t_idx])
        output_sum = sum(pn.O[t_idx])
        if input_sum != output_sum:
            return False
    return True

def _compute_transition_image(R, trans_idx, pn, bdd_vars, is_conservative):
    places = pn.place_ids
    n_places = len(places)
    
    enabling = _bdd_true(bdd_vars)
    for j in range(n_places):
        is_input = pn.I[trans_idx, j] >= 1
        is_output = pn.O[trans_idx, j] >= 1
        
        p_var = bdd_vars[places[j]]
        
        if is_input and not is_output:
            enabling &= p_var
        elif is_output and not is_input:
            enabling &= ~p_var
        elif is_input and is_output:
            enabling &= p_var
    
    enabled_states = R & enabling
    
    if enabled_states.is_zero():
        return _bdd_false(bdd_vars)
    
    img_bdd = _bdd_false(bdd_vars)
    
    for assignment in _get_bdd_assignments(enabled_states, bdd_vars, places):
        new_marking = assignment.copy()
        
        for j in range(n_places):
            is_input = pn.I[trans_idx, j] >= 1
            is_output = pn.O[trans_idx, j] >= 1
            
            if is_input and not is_output:
                new_marking[places[j]] = 0
            elif is_output and not is_input:
                new_marking[places[j]] = 1
        
        if is_conservative:
            if sum(assignment.values()) != sum(new_marking.values()):
                continue
        
        new_bdd = _marking_to_bdd(new_marking, places, bdd_vars)
        img_bdd = img_bdd | new_bdd
    
    return img_bdd

def _create_token_constraint(total_tokens, place_ids, bdd_vars, pn):
    from itertools import combinations
    constraint = _bdd_false(bdd_vars)
    n_places = len(place_ids)
    
    for token_positions in combinations(range(n_places), total_tokens):
        marking_bdd = _bdd_true(bdd_vars)
        for i, place in enumerate(place_ids):
            p_var = bdd_vars[place]
            if i in token_positions:
                marking_bdd &= p_var
            else:
                marking_bdd &= ~p_var
        constraint = constraint | marking_bdd
    return constraint

def _marking_to_bdd(marking, place_ids, bdd_vars):
    result = _bdd_true(bdd_vars)
    if hasattr(marking, 'tolist'): marking = marking.tolist()

    if isinstance(marking, list) or isinstance(marking, tuple):
        for i, place in enumerate(place_ids):
            p_var = bdd_vars[place]
            if marking[i] >= 1: result &= p_var
            else: result &= ~p_var
    else:
        for place in place_ids:
            p_var = bdd_vars[place]
            if marking.get(place, 0) >= 1: result &= p_var
            else: result &= ~p_var
    return result

def _get_bdd_assignments(bdd, bdd_vars, places):
    if bdd.is_zero(): return []
    
    assignments = []
    for point in bdd.satisfy_all():
        missing_vars = []
        present_vars = {}
        
        for place in places:
            var = bdd_vars[place]
            if var in point:
                present_vars[place] = 1 if point[var] else 0
            else:
                missing_vars.append(place)
        
        if not missing_vars:
            assignments.append(present_vars)
        else:
            for values in itertools.product([0, 1], repeat=len(missing_vars)):
                new_assign = present_vars.copy()
                for i, val in enumerate(values):
                    new_assign[missing_vars[i]] = val
                assignments.append(new_assign)
                
    return assignments

def _count_actual_states(bdd, bdd_vars, places):
    return len(_get_bdd_assignments(bdd, bdd_vars, places))

def _bdd_true(bdd_vars):
    if not bdd_vars: return expr2bdd(expr(1))
    first_var = list(bdd_vars.values())[0]
    return first_var | ~first_var

def _bdd_false(bdd_vars):
    if not bdd_vars: return expr2bdd(expr(0))
    first_var = list(bdd_vars.values())[0]
    return first_var & ~first_var