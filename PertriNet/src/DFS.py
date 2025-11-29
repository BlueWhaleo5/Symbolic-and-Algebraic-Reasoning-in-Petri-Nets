import numpy as np
from .Parser import Parser
from typing import Set, Tuple

def dfs_algorithm(pn: Parser) -> Set[Tuple[int, ...]]:
    initial_marking = tuple(map(int, pn.M0))
    reachable = set()
    
    num_places = len(pn.place_ids)
    num_transitions = len(pn.trans_ids)
    
    I_matrix = pn.I
    O_matrix = pn.O
    
    final_I = np.zeros((num_places, num_transitions), dtype=int)
    final_O = np.zeros((num_places, num_transitions), dtype=int)
    
    if I_matrix.shape[0] == num_places and I_matrix.shape[1] <= num_transitions:
        rows_to_copy = min(I_matrix.shape[0], num_places)
        cols_to_copy = min(I_matrix.shape[1], num_transitions)
        final_I[:rows_to_copy, :cols_to_copy] = I_matrix[:rows_to_copy, :cols_to_copy]
        final_O[:rows_to_copy, :cols_to_copy] = O_matrix[:rows_to_copy, :cols_to_copy]
    elif I_matrix.shape[1] == num_places and I_matrix.shape[0] <= num_transitions:
        rows_to_copy = min(I_matrix.shape[0], num_transitions)
        cols_to_copy = min(I_matrix.shape[1], num_places)
        final_I[:cols_to_copy, :rows_to_copy] = I_matrix[:rows_to_copy, :cols_to_copy].T
        final_O[:cols_to_copy, :rows_to_copy] = O_matrix[:rows_to_copy, :cols_to_copy].T
    else:
        rows_to_copy = min(I_matrix.shape[0], num_places)
        cols_to_copy = min(I_matrix.shape[1], num_transitions)
        final_I[:rows_to_copy, :cols_to_copy] = I_matrix[:rows_to_copy, :cols_to_copy]
        final_O[:rows_to_copy, :cols_to_copy] = O_matrix[:rows_to_copy, :cols_to_copy]
    
    I_matrix = final_I
    O_matrix = final_O
    
    def dfs(marking):
        if marking in reachable:
            return
        
        reachable.add(marking)
        current_vector = np.array(marking)
        
        for trans_idx in range(num_transitions):
            enabled = True
            for place_idx in range(num_places):
                if I_matrix[place_idx, trans_idx] > current_vector[place_idx]:
                    enabled = False
                    break
            
            if enabled:
                new_vector = current_vector.copy()
                
                for place_idx in range(num_places):
                    new_vector[place_idx] -= I_matrix[place_idx, trans_idx]
                
                for place_idx in range(num_places):
                    new_vector[place_idx] += O_matrix[place_idx, trans_idx]
                
                new_marking = tuple(map(int, new_vector))
                
                if all(0 <= token <= 1 for token in new_marking):
                    dfs(new_marking)
    
    dfs(initial_marking)
    return reachable