# Symbolic-and-Algebraic-Reasoning-in-Petri-Nets
Petri nets are among the most fundamental and elegant mathematical models for describing concurrent, distributed, and event-driven systems. They provide a graphical and formal way to represent how conditions (places) and events (transitions) interact through the flow of tokens, enabling a precise analysis of system behavior.


## Requirement
numpy>=1.24
pytest>=7.0
pyeda==0.28.0

## Running step
- Donwload PetriNet folder
- Open folder in terminal
- Create virtual enviroment:          python3 -m venv venv
- Activate virtual enviroment: 
     Window:                          venv\Scripts\Activate.ps1
     Linux/MacOS:                     source venv/bin/activate
- Install requirement libaries:       pip install -r requirements.txt
- Run code:                           python3 run.py
- Run all test:                       python3 -m pytest tests/ -v
- Run single task:                    python3 -m pytest tests/[test_petriNet].py -v
- Run single test in task:            python3 -m pytest tests/[test_petriNet].py::test_001 -v
