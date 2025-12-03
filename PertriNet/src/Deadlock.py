import pulp
import numpy as np
from typing import Optional, List
from pyeda.inter import BinaryDecisionDiagram, bddvar
from .Parser import Parser

def deadlock_detect(pn: Parser, bdd: BinaryDecisionDiagram) -> Optional[List[int]]:
    place_ids = list(pn.place_ids)
    trans_ids = list(pn.trans_ids)
    num_places = len(place_ids)
    num_trans = len(trans_ids)

    I = np.array(pn.I, dtype=int)
    O = np.array(pn.O, dtype=int)

    m_vars = {p: pulp.LpVariable(f"m_{p}", lowBound=0, upBound=1, cat='Binary') 
              for p in place_ids}
    e_vars = {t: pulp.LpVariable(f"e_{t}", lowBound=0, upBound=1, cat='Binary') 
              for t in trans_ids}

    prob = pulp.LpProblem("Deadlock_Detection", pulp.LpMinimize)
    prob += 0, "Objective"

    sat_points = list(bdd.satisfy_all())
    if not sat_points:
        return None

    expanded_assignments = []
    for point in sat_points:
        present_vars = set(str(var) for var in point.keys())
        missing_vars = [p for p in place_ids if p not in present_vars]
        
        if not missing_vars:
            assignment = {p: (1 if point.get(bddvar(p), False) else 0) for p in place_ids}
            expanded_assignments.append(assignment)
        else:
            k = len(missing_vars)
            for i in range(2 ** k):
                assignment = {}
                for p in place_ids:
                    if p in present_vars:
                        assignment[p] = 1 if point.get(bddvar(p), False) else 0
                
                for j, p in enumerate(missing_vars):
                    bit = (i >> j) & 1
                    assignment[p] = bit
                
                expanded_assignments.append(assignment)
    
    unique_assignments = []
    seen = set()
    for assign in expanded_assignments:
        key = tuple(assign[p] for p in place_ids)
        if key not in seen:
            seen.add(key)
            unique_assignments.append(assign)
    
    z_list = [pulp.LpVariable(f"z_{i}", lowBound=0, upBound=1, cat='Binary') 
              for i in range(len(unique_assignments))]
    prob += pulp.lpSum(z_list) == 1

    for i, p in enumerate(place_ids):
        coeffs = []
        for idx, assignment in enumerate(unique_assignments):
            val = assignment[p]
            coeffs.append(z_list[idx] * val)
        prob += m_vars[p] == pulp.lpSum(coeffs)

    for t_idx, t in enumerate(trans_ids):
        input_indices = [i for i in range(num_places) if I[t_idx, i] == 1]
        output_indices = [i for i in range(num_places) if O[t_idx, i] == 1]
                
        # Điều kiện 1: e_t ≤ m[p] cho mỗi input place
        for p_idx in input_indices:
            p = place_ids[p_idx]
            prob += e_vars[t] <= m_vars[p]
        
        # Điều kiện 2: e_t ≤ (1 - m[p]) cho mỗi output place không phải input
        for p_idx in output_indices:
            if p_idx not in input_indices:
                p = place_ids[p_idx]
                prob += e_vars[t] <= 1 - m_vars[p]
        
        # Điều kiện đủ: e_t ≥ (tổng điều kiện đúng) - (tổng số điều kiện - 1)
        input_sum = pulp.lpSum(m_vars[place_ids[p_idx]] for p_idx in input_indices)
        
        output_only_indices = [p_idx for p_idx in output_indices if p_idx not in input_indices]
        output_only_sum = pulp.lpSum(1 - m_vars[place_ids[p_idx]] for p_idx in output_only_indices)
        
        total_conditions = len(input_indices) + len(output_only_indices)
        if total_conditions > 0:
            prob += e_vars[t] >= input_sum + output_only_sum - (total_conditions - 1)
        else:
            prob += e_vars[t] == 1

    for t in trans_ids:
        prob += e_vars[t] == 0

    solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    if pulp.LpStatus[prob.status] == 'Optimal':
        return [int(pulp.value(m_vars[p])) for p in place_ids]
    else:
        return None
