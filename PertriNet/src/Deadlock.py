import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
from .Parser import Parser
import numpy as np

def deadlock_detect(
    pn: Parser, 
    bdd: BinaryDecisionDiagram, 
) -> Optional[List[int]]:
    def is_marking_reachable(marking):
        assignment = {}
        for i, place_id in enumerate(pn.place_ids):
            var_name = f"p{place_id}" if not place_id.startswith('p') else place_id
            for var in bdd.inputs:
                if var.name == var_name:
                    assignment[var] = bool(marking[i])
                    break
        return bdd.restrict(assignment).is_one()
    
    visited = set()
    queue = deque([pn.M0.copy()])
    
    visited.add(tuple(pn.M0))
    
    while queue:
        current_marking = queue.popleft()
        current_array = np.array(current_marking)
        
        if is_dead_marking(pn, current_marking):
            return current_marking.tolist()
        
        for i, trans_id in enumerate(pn.trans_ids):
            input_vec = pn.I[i]
            output_vec = pn.O[i]
            
            if (np.all(current_array >= input_vec) and 
                np.all(current_array - input_vec + output_vec <= 1)):
                
                new_marking = current_array - input_vec + output_vec
                new_marking_tuple = tuple(new_marking)
                
                if new_marking_tuple not in visited:
                    if is_marking_reachable(new_marking):
                        visited.add(new_marking_tuple)
                        queue.append(new_marking.copy())
    
    return None

def is_dead_marking(pn: Parser, marking) -> bool:
    marking_array = np.array(marking)
    
    for i, trans_id in enumerate(pn.trans_ids):
        input_vec = pn.I[i]
        output_vec = pn.O[i]
        
        if not np.all(marking_array >= input_vec):
            continue
            
        result_marking = marking_array - input_vec + output_vec
        if np.all(result_marking <= 1):
            return False
    
    return True