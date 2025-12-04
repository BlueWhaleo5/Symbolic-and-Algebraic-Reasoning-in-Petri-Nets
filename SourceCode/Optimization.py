from typing import Tuple, List, Optional
from pyeda.inter import *
import numpy as np

def optimi_reachable_marking(
    place_ids: List[str], 
    bdd: BinaryDecisionDiagram, 
    c: np.ndarray
) -> Tuple[Optional[List[int]], Optional[int]]:

    if bdd.is_zero():
        return None, None
    
    n_places = len(place_ids)
    
    var_name_to_index = {f"p{i}": i for i in range(n_places)}
    
    best_marking = None
    best_value = -float('inf')
    
    count = 0
    max_iter = 500000 
    
    try:
        for point in bdd.satisfy_all():
            current_marking = [0] * n_places
            
            for var, val in point.items():
                v_name = str(var)
                if v_name in var_name_to_index:
                    idx = var_name_to_index[v_name]
                    current_marking[idx] = 1 if val else 0
            
            current_val = np.dot(c, current_marking)
            
            if current_val > best_value:
                best_value = current_val
                best_marking = list(current_marking)
            
            count += 1
            if count >= max_iter:
                print(f"  [Opt] Stopped after checking {max_iter} states.")
                break
                
    except Exception as e:
        print(f"Optimization Error: {e}")
        return None, None

    return best_marking, int(best_value) if best_marking is not None else None