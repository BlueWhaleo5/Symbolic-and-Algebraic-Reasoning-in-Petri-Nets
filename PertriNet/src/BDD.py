import collections
from typing import Tuple, List, Optional, Dict
from pyeda.inter import *
from .Parser import Parser
import numpy as np


def bdd_marking(pn: Parser) -> Tuple[BinaryDecisionDiagram, int]:
    I = np.array(pn.I, dtype=int)
    O = np.array(pn.O, dtype=int)
    M0_arr = np.array(pn.M0, dtype=int)
    place_ids = list(pn.place_ids)

    num_places = len(place_ids)

    if I.shape[1] != num_places:
        raise ValueError(
            f"Shape của I = {I.shape} không khớp số place = {num_places}"
        )
    if O.shape != I.shape:
        raise ValueError(
            f"Shape của O = {O.shape} không khớp I = {I.shape}"
        )

    # M0 phải là marking 0/1
    start_marking = tuple(int(v) for v in M0_arr)
    if any(v not in (0, 1) for v in start_marking):
        raise ValueError("M0 phải là marking 0/1 (safe net).")

    # Tạo BDD variable cho từng place
    bdd_vars = {p_name: bddvar(p_name) for p_name in place_ids}

    reachable = _enumerate_reachable_markings(I, O, start_marking)

    result_bdd = _bdd_false(bdd_vars)

    for m in reachable:
        cube = _marking_to_bdd(m, place_ids, bdd_vars)
        result_bdd = result_bdd | cube
    return result_bdd, len(reachable)


def _enumerate_reachable_markings(
    I: np.ndarray,
    O: np.ndarray,
    start: Tuple[int, ...],
) -> List[Tuple[int, ...]]:
    num_trans = I.shape[0]

    visited = {start}
    frontier = {start}

    while frontier:
        new_frontier = set()

        for marking in frontier:
            m_vec = np.fromiter(marking, dtype=int)

            for t in range(num_trans):
                pre = I[t, :]
                post = O[t, :]

                if np.all(m_vec >= pre):
                    next_vec = m_vec - pre + post

                    if np.any((next_vec != 0) & (next_vec != 1)):
                        continue

                    next_marking = tuple(int(x) for x in next_vec)

                    if next_marking not in visited:
                        visited.add(next_marking)
                        new_frontier.add(next_marking)

        frontier = new_frontier
    return list(visited)

def _marking_to_bdd(marking, place_ids, bdd_vars):
    result = _bdd_true(bdd_vars)

    if isinstance(marking, np.ndarray) or isinstance(marking, list) or isinstance(marking, tuple):
        for i, place in enumerate(place_ids):
            if marking[i] >= 1:
                result &= bdd_vars[place]
            else:
                result &= ~bdd_vars[place]
    else:
        # marking là dict: {place_id: token}
        for place in place_ids:
            if marking.get(place, 0) >= 1:
                result &= bdd_vars[place]
            else:
                result &= ~bdd_vars[place]
    return result

def _bdd_true(bdd_vars):
    if not bdd_vars:
        return expr2bdd(expr(1))
    first_var = list(bdd_vars.values())[0]
    return first_var | ~first_var


def _bdd_false(bdd_vars):
    if not bdd_vars:
        return expr2bdd(expr(0))
    first_var = list(bdd_vars.values())[0]
    return first_var & ~first_var
