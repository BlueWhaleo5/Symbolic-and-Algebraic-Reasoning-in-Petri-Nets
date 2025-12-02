import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
import numpy as np

def optimi_reachable_marking(
    place_ids: List[str], 
    bdd: BinaryDecisionDiagram, 
    c: np.ndarray
) -> Tuple[Optional[List[int]], Optional[int]]:

    if bdd.is_zero():
        return None, None
    
    if bdd.is_one():
        marking = [1 if c[i] > 0 else 0 for i in range(len(place_ids))]
        value = np.dot(c, marking)
        return marking, int(value)
    
    n = len(place_ids)
    best_marking = None
    best_value = -float('inf')
    
    var_mapping = {}
    for i, place_id in enumerate(place_ids):
        var_name = f"p{place_id}" if not place_id.startswith('p') else place_id
        for var in bdd.inputs:
            if var.name == var_name:
                var_mapping[var] = i
                break
    
    for i in range(min(5000, 2**n)):
        marking = []
        for j in range(n):
            marking.append(1 if (i >> j) & 1 else 0)
        
        assignment = {}
        for var, idx in var_mapping.items():
            assignment[var] = bool(marking[idx])
        
        if bdd.restrict(assignment).is_one():
            value = np.dot(c, marking)
            if value > best_value:
                best_value = value
                best_marking = marking
            elif value == best_value and best_marking is not None:
                if tuple(marking) > tuple(best_marking):
                    best_marking = marking
    
    return best_marking, int(best_value) if best_marking is not None else None
