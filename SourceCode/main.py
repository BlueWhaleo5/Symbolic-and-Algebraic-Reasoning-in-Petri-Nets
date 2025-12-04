import time
import numpy as np
import os
import sys

from Parser import Parser
import BFS
import DFS
import BDD
import Deadlock
import Optimization

def run_single_test(filename):
    if not os.path.exists(filename):
        print(f"\n⚠️  File {filename} not found! Skipping...")
        return None

    print("\n" + "="*80)
    print(f"TESTING FILE: {filename}")
    print("="*80)

    result_summary = {
        "file": filename,
        "bfs_states": 0,
        "bfs_time": 0.0,
        "dfs_states": 0,
        "dfs_time": 0.0,
        "bdd_states": 0,
        "bdd_time": 0.0,
        "pass": False,
        "deadlock": "Safe",
        "opt_val": "None"
    }

    try:
        pn = Parser.from_pnml(filename)
        
        start_t = time.time()
        bfs_reachable = BFS.bfs_algorithm(pn)
        bfs_time = time.time() - start_t
        result_summary["bfs_states"] = len(bfs_reachable)
        result_summary["bfs_time"] = bfs_time
        
        print(f"BFS Reachable: {len(bfs_reachable)}")
        print(f"BFS Time: {bfs_time:.4f}s")

        start_t = time.time()
        dfs_reachable = DFS.dfs_algorithm(pn)
        dfs_time = time.time() - start_t
        result_summary["dfs_states"] = len(dfs_reachable)
        result_summary["dfs_time"] = dfs_time
        
        print(f"DFS Reachable: {len(dfs_reachable)}")
        print(f"DFS Time: {dfs_time:.4f}s")

        start_t = time.time()
        reachable_bdd, bdd_count = BDD.bdd_reachable(pn)
        bdd_time = time.time() - start_t
        result_summary["bdd_states"] = bdd_count
        result_summary["bdd_time"] = bdd_time
        
        print(f"BDD Reachable: {bdd_count}")
        print(f"BDD Time: {bdd_time:.4f}s")

        bfs_count = len(bfs_reachable)
        dfs_count = len(dfs_reachable)
        
        if bfs_count == dfs_count == bdd_count:
            result_summary["pass"] = True
        else:
            print(f"!!! WARNING: Mismatch BFS({bfs_count}) | DFS({dfs_count}) | BDD({bdd_count})")

        print("Deadlock Check:")
        start_t = time.time()
        deadlock_res = Deadlock.deadlock_detect(pn, reachable_bdd)
        deadlock_time = time.time() - start_t
        
        if deadlock_res:
            result_summary["deadlock"] = "FOUND"
            print(f"Result: Deadlock Found (Marking: {deadlock_res})")
        else:
            result_summary["deadlock"] = "Safe"
            print("Result: Safe")
            
        print(f"Deadlock Time: {deadlock_time:.4f}s")

        weights = np.ones(len(pn.place_ids), dtype=int)
        
        print(f"Optimization (c = {weights.tolist()}):")
        
        start_t = time.time()
        opt_marking, opt_value = Optimization.optimi_reachable_marking(pn.place_ids, reachable_bdd, weights)
        opt_time = time.time() - start_t
        
        if opt_marking:
            result_summary["opt_val"] = str(opt_value)
            print(f"Max Value: {opt_value}")
            print(f"Optimal Marking: {opt_marking}")
        else:
            print("Max Value: None")
            print("Optimal Marking: None")
            
        print(f"Optimization Time: {opt_time:.4f}s")

    except Exception as e:
        print(f"CRITICAL ERROR running {filename}: {e}")
        import traceback
        traceback.print_exc()
        result_summary["pass"] = False
        result_summary["opt_val"] = "Error"
    
    return result_summary

def main():
    test_files = [f"test{i}.pnml" for i in range(1, 11)]
    
    results = []
    
    for file in test_files:
        res = run_single_test(file)
        if res:
            results.append(res)
            
    print("\n\n")
    print("="*135)
    print(f"{'FINAL SUMMARY REPORT':^135}")
    print("="*135)
    
    header = f"{'File':<12} | {'BFS':<6} | {'DFS':<6} | {'BDD':<6} | {'T.BFS':<8} | {'T.DFS':<8} | {'T.BDD':<8} | {'Status':<8} | {'Deadlock':<9} | {'Opt Val':<8}"
    print(header)
    print("-" * 135)

    passed_count = 0
    total_run = 0

    for res in results:
        total_run += 1
        status_str = "PASS" if res["pass"] else "FAIL"
        if res["pass"]:
            passed_count += 1
        
        row = (
            f"{res['file']:<12} | "
            f"{res['bfs_states']:<6} | "
            f"{res['dfs_states']:<6} | "
            f"{res['bdd_states']:<6} | "
            f"{res['bfs_time']:<8.4f} | "
            f"{res['dfs_time']:<8.4f} | "
            f"{res['bdd_time']:<8.4f} | "
            f"{status_str:<8} | "
            f"{res['deadlock']:<9} | "
            f"{res['opt_val']:<8}"
        )
        print(row)

    print("-" * 135)
    print(f"Success Rate: {passed_count}/{total_run}")
    print("="*135)

if __name__ == "__main__":
    main()