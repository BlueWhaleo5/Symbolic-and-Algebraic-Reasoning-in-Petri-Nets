# Symbolic and Algebraic Reasoning in Petri Nets

Petri nets are among the most fundamental and elegant mathematical models for describing concurrent, distributed, and event-driven systems. They provide a graphical and formal way to represent how conditions (places) and events (transitions) interact through the flow of tokens, enabling a precise analysis of system behavior.

## 📋 Table of Contents
- [Requirements](#requirements)
- [🚀 Quick Start](#quick-start)
- [🧪 Running Tests](#running-tests)

## Requirements

Ensure you have the following Python packages installed:

| Package | Version |
|---------|---------|
| `numpy` | `>=1.24` |
| `pytest` | `>=7.0` |
| `pyeda` | `==0.28.0` |

## 🚀 Quick Start

Follow these steps to get the project up and running on your local machine.

1.  **Download requirements.txt and the PertriNet folder**

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
    python3 run.py
    ```
    
## Testing with PNML Files

**Important:** Please read all the comment in run.py as it is all important notes to run test pnml

You can change the PNML file for testing by modifying line:
```python
filename = "./pnml/test6.pnml"
```

# For testing Optimization task:

|   Test   |    Place    | Transitions | Array c |
|------------|---------------|------------------|-----------------------------|
| `Test 1` | `3 places` | `3 transitions` | `c = np.array([1, -2, 3])` |
| `Test 2` | `4 places` | `4 transitions` | `c = np.array([1, -2, 3, -1])` |
| `Test 3` | `6 places` | `6 transitions` | `c = np.array([1, -2, 3, -1, 1, 2])` |
| `Test 4` | `10 places` | `10 transitions` | `c = np.array([1, -2, 3, -1, 1, 2, 3, 1, -1, -2])` |
| `Test 5` | `12 places` | `10 transitions` | `c = np.array([1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5])` |
| `Test 6` | `30 places` | `30 transitions` | `c = np.array([1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5, 1, -2, 3, -1, 1, 2, 3, 1, -1, -2, 4, 5, 1, -2, 3, -1, 1, 2])` |

To test with more than 30 places, please modify the code in Optimization.py to increase the limit of iterations in the optimization function.

In Optimization.py, find and change 500000 to a larger number in the line:
```bash
for i in range(min(500000, 2**n)):
```

