import numpy as np
from .Parser import Parser
from typing import Set, Tuple

def dfs_algorithm(pn: Parser) -> Set[Tuple[int, ...]]:
    initial_marking = tuple(map(int, pn.M0))
    reachable = set()
    
    num_places = len(pn.place_ids)
    
    I_matrix = pn.I
    O_matrix = pn.O
    
    num_transitions_in_matrix = I_matrix.shape[0]
    
    # print(f"[DFS] Checking {num_transitions_in_matrix} transitions, {num_places} places")
    # print(f"[DFS] I shape: {I_matrix.shape}, O shape: {O_matrix.shape}")
    
    def dfs(marking):
        if marking in reachable:
            return
        
        reachable.add(marking)
        current_vector = np.array(marking)
        
        for trans_idx in range(num_transitions_in_matrix):
            enabled = True
            for place_idx in range(num_places):
                if I_matrix[trans_idx, place_idx] > current_vector[place_idx]:
                    enabled = False
                    break
            
            if not enabled:
                continue
            
            new_vector = current_vector.copy()
            for place_idx in range(num_places):
                new_vector[place_idx] -= I_matrix[trans_idx, place_idx]
                new_vector[place_idx] += O_matrix[trans_idx, place_idx]
            
            is_1_safe = True
            for token in new_vector:
                if token < 0 or token > 1:
                    is_1_safe = False
                    break
            
            if not is_1_safe:
                # print(f"DFS rejected: {current_vector} --t{trans_idx}--> {tuple(new_vector)}")
                continue
            
            
            new_marking = tuple(map(int, new_vector))
            dfs(new_marking)
    
    dfs(initial_marking)
    
    # print(f"[DFS] Total reachable markings: {len(reachable)}")
    
    # # Debug: in ra một vài marking
    # if len(reachable) > 0:
    #     print("[DFS] First 5 markings:")
    #     for i, marking in enumerate(list(reachable)):
    #         print(f"  {i+1}: {marking}")
    
    return reachable