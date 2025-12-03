from src.Parser import Parser
from src.BDD import bdd_marking
from src.Optimization import optimi_reachable_marking
from src.BFS import bfs_algorithm
from src.DFS import dfs_algorithm
from src.Deadlock import deadlock_detect
from pyeda.inter import * 
import numpy as np
import time
import memory_profiler

def main():
    # ------------------------------------------------------
    # 1. Load Petri Net từ file PNML
    # ------------------------------------------------------
    filename = "./pnml/test6.pnml"   # change file path here
    print("Loading PNML:", filename)

    pn = Parser.from_pnml(filename)
    print("\n--- Petri Net Loaded ---")
    print(pn)

    # ------------------------------------------------------
    # 2. BFS reachable
    # ------------------------------------------------------
    print("\n--- BFS Reachable Markings ---")
    start_time = time.time()
    start_mem = memory_profiler.memory_usage()[0]
    bfs_set = bfs_algorithm(pn)
    end_mem = memory_profiler.memory_usage()[0]
    end_time = time.time()
    # for m in bfs_set:
    #     print(np.array(m))
    print("Total BFS reachable =", len(bfs_set))
    print(f"BFS Time: {end_time - start_time:.4f} seconds")
    print(f"BFS Memory: {end_mem - start_mem:.4f} MB")

    # ------------------------------------------------------
    # 3. DFS reachable
    # ------------------------------------------------------
    print("\n--- DFS Reachable Markings ---")
    start_time = time.time()
    start_mem = memory_profiler.memory_usage()[0]
    dfs_set = dfs_algorithm(pn)
    end_mem = memory_profiler.memory_usage()[0]
    end_time = time.time()
    # for m in dfs_set:
    #     print(np.array(m))
    print("Total DFS reachable =", len(dfs_set))
    print(f"DFS Time: {end_time - start_time:.4f} seconds")
    print(f"DFS Memory: {end_mem - start_mem:.4f} MB")

    # ------------------------------------------------------
    # 4. BDD reachable
    # ------------------------------------------------------
    valid_places = [f"p{i}" for i in range(len(pn.place_ids))]
    pn.place_ids = valid_places 
    print("\n--- BDD Reachable ---")
    start_time = time.time()
    start_mem = memory_profiler.memory_usage()[0]
    bdd, count = bdd_marking(pn)
    end_mem = memory_profiler.memory_usage()[0]
    end_time = time.time()
    # print("Satisfying all:", list(bdd.satisfy_all()))
    # print("Minimized =", espresso_exprs(bdd2expr(bdd)))
    print("BDD reachable markings =", count)
    print(f"BDD Time: {end_time - start_time:.4f} seconds")
    print(f"BDD Memory: {end_mem - start_mem:.4f} MB")

    # ------------------------------------------------------
    # 5. Deadlock detection
    # ------------------------------------------------------
    print("\n--- Deadlock reachable marking ---")
    start_time = time.time()
    start_mem = memory_profiler.memory_usage()[0]
    dead = deadlock_detect(pn, bdd)
    end_time = time.time()
    end_mem = memory_profiler.memory_usage()[0]
    if dead is not None:
        print("Deadlock marking:", dead)
    else:
        print("No deadlock reachable.")
    print(f"Deadlock Time: {end_time - start_time:.4f} seconds")
    print(f"Deadlock Memory: {end_mem - start_mem:.4f} MB")

    # ------------------------------------------------------
    # 6. Optimization: maximize c·M
    # ------------------------------------------------------
    start_time = time.time()
    start_mem = memory_profiler.memory_usage()[0]
    c = np.array([1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5, 1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5, 1, -2, 3, -1, 1, 2]) #change base on number of places
    print("\n--- Optimize c·M ---")
    opt_marking, opt_value = optimi_reachable_marking(pn.place_ids, bdd, c)
    end_time = time.time()
    end_mem = memory_profiler.memory_usage()[0]
    print(f'Optimization (c = {c})')
    if opt_marking is not None:
        print(f"Optimal marking: {opt_marking}")
        print(f"Optimal value: {opt_value}")
    else:
        print("No reachable marking found")
    print(f"Optimization Time: {end_time - start_time:.4f} seconds")
    print(f"Optimization Memory: {end_mem - start_mem:.4f} MB")


if __name__ == "__main__":
    main()

# Test 1: 3 places, 3 transitions      c = np.array([1, -2, 3])
# Test 2: 4 places, 4 transitions      c = np.array([1, -2, 3, -1])
# Test 3: 6 places, 6 transitions      c = np.array([1, -2, 3, -1, 1, 2])
# Test 4: 10 places, 10 transitions    c = np.array([1, -2, 3, -1, 1, 2, 3, 1, -1, -2])
# Test 5: 12 places, 10 transitions    c = np.array([1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5])
# Test 6: 30 places, 30 transitions    c = np.array([1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5, 1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5, 1, -2, 3, -1, 1, 2])


# To test with more than 30 places, please modify the code in Optimization.py to increase the limit of iterations in the optimization function.
# In Optimization.py, find and change 500000 to a larger number in the line:
    # for i in range(min(500000, 2**n)):
