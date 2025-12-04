# MATHEMATICAL MODELING ASSIGNMENT (CO2011)
# Symbolic and Algebraic Reasoning in Petri Nets

Petri nets are among the most fundamental and elegant mathematical models for describing concurrent, distributed, and event-driven systems. They provide a graphical and formal way to represent how conditions (places) and events (transitions) interact through the flow of tokens, enabling a precise analysis of system behavior.

## 📋 Table of Contents
- [Requirements](#requirements)
- [🚀 Quick Start](#quick-start)
- [🧪 Running Test](#testing-with-PNML-Files)
- [Project Structure](#project-structure)

## Requirements

Ensure you have the following Python packages installed:

| Package | Version |
|---------|---------|
| `python` | `>=3.8` |
| `numpy` | `>=1.24` |
| `pytest` | `>=7.0` |
| `pyeda` | `==0.28.0` |

- Operating System: macOS / Linux (recommended for PyEDA), or Windows.

## 🚀 Quick Start

Follow these steps to get the project up and running on your local machine.

1.  **Download requirements.txt and the PertriNet folder**
- Ensure that all source code files and the test cases (test1.pnml to test10.pnml) are located in the same directory (or adjust the path in main.py if necessary).
- Open your terminal or command prompt and navigate to the source code directory.
2.  **Set Up a Virtual Environment**
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment**
    *   **Windows (PowerShell):**
        ```powershell
        venv\Scripts\Activate.ps1
        ```
    *   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Application**
    ```bash
    python3 main.py
    ```
    or 
    ```bash
    python run.py > log.txt 2>&1   #to have output in log.txt file
    ```
    
##  PROJECT STRUCTURE
--------------------
- main.py         : The entry point of the program. It orchestrates the parsing, reachability analysis, deadlock detection, and optimization tasks for all test cases.
- Parser.py       : Parses PNML files into algebraic representations (Input/Output matrices).
- BFS.py          : Implements Explicit Reachability using Breadth-First Search.
- DFS.py          : Implements Explicit Reachability using Depth-First Search.
- BDD.py          : Implements Symbolic Reachability using Binary Decision Diagrams (Hybrid Symbolic-Explicit approach for strict 1-safe compliance).
- Deadlock.py     : Detects deadlocks using symbolic set operations on the computed BDD.
- Optimization.py : Finds the optimal marking based on a linear objective function using BDD iterators.
