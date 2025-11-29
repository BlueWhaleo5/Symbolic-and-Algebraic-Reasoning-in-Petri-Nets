from project.PetriNet.PertriNet.src.Parser import Parser
from src.BDD import bdd_marking
from src.Optimization import optimi_reachable_marking
from src.BFS import bfs_algorithm
from src.DFS import dfs_algorithm
from src.Deadlock import deadlock_detect
from pyeda.inter import * 
import numpy as np
## from graphviz import Source

def main():
    # ------------------------------------------------------
    # 1. Load Petri Net từ file PNML
    # ------------------------------------------------------
    filename = "example.pnml"   # đổi file tại đây
    print("Loading PNML:", filename)

    pn = Parser.from_pnml(filename)
    print("\n--- Petri Net Loaded ---")
    print(pn)

    # ------------------------------------------------------
    # 2. BFS reachable
    # ------------------------------------------------------
    print("\n--- BFS Reachable Markings ---")
    bfs_set = bfs_algorithm(pn)
    for m in bfs_set:
        print(np.array(m))
    print("Total BFS reachable =", len(bfs_set))

    # ------------------------------------------------------
    # 3. DFS reachable
    # ------------------------------------------------------
    print("\n--- DFS Reachable Markings ---")
    dfs_set = dfs_algorithm(pn)
    for m in dfs_set:
        print(np.array(m))
    print("Total DFS reachable =", len(dfs_set))

    # ------------------------------------------------------
    # 4. BDD reachable
    # ------------------------------------------------------
    valid_places = [f"p{i}" for i in range(len(pn.place_ids))]  # p0, p1, p2,...
    pn.place_ids = valid_places  # Gán lại place IDs hợp lệ
    print("\n--- BDD Reachable ---")
    bdd, count = bdd_marking(pn)
    print("Satisfying all:", list(bdd.satisfy_all()))
    print("Minimized =", espresso_exprs(bdd2expr(bdd)))
    print("BDD reachable markings =", count)
    ## Source(bdd.to_dot()).render("bdd", format="png", cleanup=True)

    # ------------------------------------------------------
    # 5. Deadlock detection
    # ------------------------------------------------------
    print("\n--- Deadlock reachable marking ---")
    dead = deadlock_detect(pn, bdd)
    if dead is not None:
        print("Deadlock marking:", dead)
    else:
        print("No deadlock reachable.")

    # ------------------------------------------------------
    # 6. Optimization: maximize c·M
    # ------------------------------------------------------
    c = np.array([1, -2, 3, -1, 1, 2])
    print("\n--- Optimize c·M ---")
    max_mark, max_val = optimi_reachable_marking(
        pn.place_names, bdd, c
    )
    print("c:", c)
    print("Max marking:", max_mark)
    print("Max value:", max_val)


if __name__ == "__main__":
    main()
