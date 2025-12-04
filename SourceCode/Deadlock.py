import numpy as np
from typing import Optional, List
from pyeda.inter import *
from Parser import Parser

def deadlock_detect(pn: Parser, reachable_bdd: BinaryDecisionDiagram) -> Optional[List[int]]:
    bdd_vars = {}
    place_ids = pn.place_ids
    for i, pid in enumerate(place_ids):
        bdd_vars[pid] = bddvar(f"p{i}")
        
    one = list(bdd_vars.values())[0] | ~list(bdd_vars.values())[0]
    zero = list(bdd_vars.values())[0] & ~list(bdd_vars.values())[0]
    
    any_enabled = zero
    n_transitions = len(pn.trans_ids)
    
    for t_idx in range(n_transitions):
        t_enabled = one
        input_indices = np.where(pn.I[t_idx] > 0)[0]
        
        if len(input_indices) == 0:
            t_enabled = one
        else:
            for idx in input_indices:
                p_name = place_ids[idx]
                t_enabled &= bdd_vars[p_name]
        
        any_enabled = any_enabled | t_enabled
        
    potential_deadlock = ~any_enabled
    
    real_deadlocks = reachable_bdd & potential_deadlock
    
    if real_deadlocks.is_zero():
        return None
    
    example_point = real_deadlocks.satisfy_one()
    
    result_marking = [0] * len(place_ids)
    
    for i, pid in enumerate(place_ids):
        p_var = bdd_vars[pid]
        
        if p_var in example_point:
            result_marking[i] = 1 if example_point[p_var] else 0
        else:
            result_marking[i] = 0
            
    return result_marking