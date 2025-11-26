from collections import deque
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple

def bfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:
    # Start with initial marking
    initial_marking = tuple(map(int, pn.M0))
    reachable = set()
    reachable.add(initial_marking)
    
    # Queue for BFS
    queue = deque()
    queue.append(initial_marking)
    
    # Get actual dimensions
    num_places = len(pn.place_ids)
    num_transitions = len(pn.trans_ids)
    
    # Handle matrix dimensions - they might not match exactly
    I_matrix = pn.I
    O_matrix = pn.O
    
    # Create properly sized matrices
    final_I = np.zeros((num_places, num_transitions), dtype=int)
    final_O = np.zeros((num_places, num_transitions), dtype=int)
    
    # Copy available data based on matrix orientation
    if I_matrix.shape[0] == num_places and I_matrix.shape[1] <= num_transitions:
        # Place x Transition format
        rows_to_copy = min(I_matrix.shape[0], num_places)
        cols_to_copy = min(I_matrix.shape[1], num_transitions)
        final_I[:rows_to_copy, :cols_to_copy] = I_matrix[:rows_to_copy, :cols_to_copy]
        final_O[:rows_to_copy, :cols_to_copy] = O_matrix[:rows_to_copy, :cols_to_copy]
    elif I_matrix.shape[1] == num_places and I_matrix.shape[0] <= num_transitions:
        # Transition x Place format - transpose
        rows_to_copy = min(I_matrix.shape[0], num_transitions)
        cols_to_copy = min(I_matrix.shape[1], num_places)
        final_I[:cols_to_copy, :rows_to_copy] = I_matrix[:rows_to_copy, :cols_to_copy].T
        final_O[:cols_to_copy, :rows_to_copy] = O_matrix[:rows_to_copy, :cols_to_copy].T
    else:
        # Unknown format - try to fit what we can
        rows_to_copy = min(I_matrix.shape[0], num_places)
        cols_to_copy = min(I_matrix.shape[1], num_transitions)
        final_I[:rows_to_copy, :cols_to_copy] = I_matrix[:rows_to_copy, :cols_to_copy]
        final_O[:rows_to_copy, :cols_to_copy] = O_matrix[:rows_to_copy, :cols_to_copy]
    
    I_matrix = final_I
    O_matrix = final_O
    
    while queue:
        current_marking = queue.popleft()
        current_vector = np.array(current_marking)
        
        # Check all transitions for enabledness
        for trans_idx in range(num_transitions):
            # Check if transition is enabled
            enabled = True
            for place_idx in range(num_places):
                if I_matrix[place_idx, trans_idx] > current_vector[place_idx]:
                    enabled = False
                    break
            
            if enabled:
                # Create new marking by firing the transition
                new_vector = current_vector.copy()
                
                # Remove tokens from input places
                for place_idx in range(num_places):
                    new_vector[place_idx] -= I_matrix[place_idx, trans_idx]
                
                # Add tokens to output places  
                for place_idx in range(num_places):
                    new_vector[place_idx] += O_matrix[place_idx, trans_idx]
                
                # Convert to tuple of Python ints
                new_marking = tuple(map(int, new_vector))
                
                # Only add if it's 1-safe AND new
                if all(0 <= token <= 1 for token in new_marking) and new_marking not in reachable:
                    reachable.add(new_marking)
                    queue.append(new_marking)
    
    return reachable