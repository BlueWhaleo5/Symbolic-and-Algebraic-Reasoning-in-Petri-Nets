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

1.  **Download the PertriNet folder**

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

## 🧪 Running Tests

This project uses `pytest` for testing.

| Action | Command |
|--------|---------|
| Run all tests | `python3 -m pytest tests/ -v` |
| Run a single test file | `python3 -m pytest tests/test_petriNet.py -v` |
| Run a single test case | `python3 -m pytest tests/test_petriNet.py::test_001 -v` |
