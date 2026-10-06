# Traversal Toolkit

A modular web app for learning binary trees, string operations, sets, and deterministic finite automata. The project has been refactored into a cleaner tab-based layout with separate UI sections and independent per-tab logic, while keeping the core toolkit operations accessible from a single Flask app.

## What was implemented

### Modern UI refactor
- Reworked the app into a collapsible sidebar with separate pages for:
  - Binary Tree
  - Text Operations
  - Sets
  - DFA
- Split the interface into reusable template sections in `templates/toolkit/`
- Split JavaScript behavior by tab into independent files in `static/`
- Kept the shared app shell and styling in `static/app.js` and `static/style.css`
- Preserved the sidebar navigation and broad app layout while separating each tool into its own page state

### Independent tab logic
- Each tool section now has its own independent inputs and handlers
- The tree tab no longer depends on DFA or shared form state
- The DFA tab no longer depends on tree inputs or shared payload structure
- This prevents cross-tab collisions and keeps each module easier to maintain

### DFA behavior and parsing
- Kept a simple DFA definition format based on state transitions
- Supported accept-state parsing with either space or comma separation
- Kept the default DFA flow consistent with a `q0 -> q1 -> qf` pattern structure
- Included support for `*`-style transitions and standard trace output for each state change

### Styling update
- Dark UI theme with readable contrast
- Sidebar, cards, inputs, buttons, and output panels aligned for a consistent interface
- Improved readability for DFA trace output and results panels

## Project structure

- `app.py` – Flask entry point and `/api/analyze` routes
- `traversal_toolkit/` – toolkit logic
  - `tree.py` – binary tree building and traversal logic
  - `text_ops.py` – string operations
  - `string_extra.py` – extra string utilities
  - `set_ops.py` – set operations
  - `dfa.py` – DFA parsing, transitions, and simulation
- `templates/`
  - `index.html` – shell layout
  - `sidebar.html` – sidebar navigation
  - `toolkit/` – individual page templates for each tool
- `static/`
  - `app.js` – page switching and shared shell behavior
  - `tree.js` – tree tab logic
  - `text.js` – text tab logic
  - `set.js` – set tab logic
  - `dfa.js` – DFA tab logic
  - `style.css` – dark responsive styling
- `samples/examples.json` – example data
- `tests/test_core.py` – project tests and regression checks

## Features

### Binary Tree
- Build trees from preorder + inorder or postorder + inorder
- Visualize output trees
- Compute tree properties such as height and traversal results

### Text Operations
- Input strings and run multiple text transformations
- Reverse, length, case conversion, palindrome checks, prefix/suffix logic
- Combine operations and inspect output clearly

### Sets
- Work with custom sets or generated values
- Perform union, intersection, difference, and symmetric difference
- View cardinality and set relationships

### DFA (Deterministic Finite Automaton)
- Define a DFA in text format
- Test strings through transitions
- View the trace from start to final state
- Confirm accepted or rejected states

## Run

```bash
cd /path/to/Traversal-Toolkit
./flask/bin/python app.py
```

Or with a normal virtual environment:

```bash
python3 -m venv flask
./flask/bin/pip install -r requirements.txt
./flask/bin/python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## DFA format

```text
start: q0
accept: q1 qf
q0,a,q1
q1,b,qf
qf,b,qf
```

- `start:` defines the start state
- `accept:` defines the accepting states
- Each transition is written as `from_state,symbol,to_state`
- Accept states may be separated by spaces or commas

## Tests

```bash
./flask/bin/python -m pytest -q
```

## Notes

The app has been restructured to support cleaner modular development while preserving the original educational toolkit behavior. The sidebar, tab separation, and dark styling are the main UI improvements, while the core toolkit logic remains focused on the original traversal and automata concepts.

