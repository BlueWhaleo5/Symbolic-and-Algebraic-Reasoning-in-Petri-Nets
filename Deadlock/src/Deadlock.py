import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
from .PetriNet import PetriNet
import numpy as np

def deadlock_reachable_marking(
    pn: PetriNet, 
    bdd: BinaryDecisionDiagram, 
) -> Optional[List[int]]:
    """
    Detect a deadlock using reachability graph simulation.
    A deadlock is a reachable marking where no transition is enabled.
    """
    # Use BDD to check if a marking is in the reachable set
    def is_marking_reachable(marking):
        # Convert marking to variable assignment
        assignment = {}
        for i, place_id in enumerate(pn.place_ids):
            var_name = f"p{place_id}" if not place_id.startswith('p') else place_id
            # Find the corresponding variable in BDD
            for var in bdd.inputs:
                if var.name == var_name:
                    assignment[var] = bool(marking[i])
                    break
        return bdd.restrict(assignment).is_one()
    
    # Perform BFS to explore reachable markings
    visited = set()
    queue = deque([pn.M0.copy()])
    
    visited.add(tuple(pn.M0))
    
    while queue:
        current_marking = queue.popleft()
        current_array = np.array(current_marking)
        
        # Check if current marking is a deadlock
        if is_dead_marking(pn, current_marking):
            return current_marking.tolist()
        
        # Try to fire each transition from current marking
        for i, trans_id in enumerate(pn.trans_ids):
            input_vec = pn.I[i]
            output_vec = pn.O[i]
            
            # Check if transition is enabled
            if (np.all(current_array >= input_vec) and 
                np.all(current_array - input_vec + output_vec <= 1)):
                
                # Fire the transition
                new_marking = current_array - input_vec + output_vec
                new_marking_tuple = tuple(new_marking)
                
                if new_marking_tuple not in visited:
                    # Check if new marking is in BDD reachable set
                    if is_marking_reachable(new_marking):
                        visited.add(new_marking_tuple)
                        queue.append(new_marking.copy())
    
    return None

def is_dead_marking(pn: PetriNet, marking) -> bool:
    """
    Check if a marking is dead (no transition is enabled).
    For 1-safe Petri nets, a transition is enabled if:
    1. M >= I[t] (input places have tokens)
    2. M - I[t] + O[t] <= 1 (output places will not exceed 1 token after firing)
    """
    marking_array = np.array(marking)
    
    for i, trans_id in enumerate(pn.trans_ids):
        # Get input and output vectors for this transition
        input_vec = pn.I[i]
        output_vec = pn.O[i]
        
        # Check condition 1: M >= I[t]
        if not np.all(marking_array >= input_vec):
            continue
            
        # Check condition 2: M - I[t] + O[t] <= 1 (for 1-safe nets)
        result_marking = marking_array - input_vec + output_vec
        if np.all(result_marking <= 1):
            # This transition is enabled, so marking is not dead
            return False
    
    # No enabled transitions found
    return True