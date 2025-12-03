from collections import deque
import numpy as np
from .Parser import Parser
from typing import Set, Tuple

def bfs_algorithm(pn: Parser) -> Set[Tuple[int, ...]]:
    initial_marking = tuple(map(int, pn.M0))
    reachable = set()
    reachable.add(initial_marking)
    
    queue = deque()
    queue.append(initial_marking)
    
    num_places = len(pn.place_ids)
    
    I_matrix = pn.I
    O_matrix = pn.O
    
    num_transitions_in_matrix = I_matrix.shape[0]
    
    # print(f"[BFS] Checking {num_transitions_in_matrix} transitions, {num_places} places")
    # print(f"[BFS] I shape: {I_matrix.shape}, O shape: {O_matrix.shape}")
    
    while queue:
        current_marking = queue.popleft()
        current_vector = np.array(current_marking)
        
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
                # Trừ input tokens
                new_vector[place_idx] -= I_matrix[trans_idx, place_idx]
                # Cộng output tokens
                new_vector[place_idx] += O_matrix[trans_idx, place_idx]
            
            is_1_safe = True
            for token in new_vector:
                if token < 0 or token > 1:
                    is_1_safe = False
                    break
            
            if not is_1_safe:
                # print(f"BFS rejected: {current_marking} --t{trans_idx}--> {tuple(new_vector)}")
                continue
            
            new_marking = tuple(map(int, new_vector))
            
            if new_marking not in reachable:
                reachable.add(new_marking)
                queue.append(new_marking)
    
    # print(f"[BFS] Total reachable markings: {len(reachable)}")
    
    # # Debug: in ra một vài marking
    # if len(reachable) > 0:
    #     print("[BFS] First 5 markings:")
    #     for i, marking in enumerate(list(reachable)):
    #         print(f"  {i+1}: {marking}")
    
    return reachable