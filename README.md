# Traversal Toolkit

A web app for learning binary trees, string operations, sets, and DFAs. Build a binary tree from preorder/inorder/postorder traversals, then explore tree properties, string operations, set theory, and deterministic finite automata.

## Features

### Binary Tree
- Build trees from traversals: preorder + inorder, or postorder + inorder
- Visualize the tree structure
- View tree properties: height, leaves, level-order traversal, BST validation

### Text Operations
- Single input field for any text
- Operations: length, reverse, palindrome check (trims spaces, ignores case), case conversion
- First/last 3 characters, unique character count

### Sets
- Manual set input or auto-generate from tree
- Set A = left subtree + root, Set B = right subtree + root
- Operations: union, intersection, difference, symmetric difference, cardinality

### DFA (Deterministic Finite Automaton)
- Define custom DFAs with simple text format
- Test strings against the DFA
- View state trace and acceptance result
- Default DFA included: accepts strings of even length

## Run

```bash
cd /path/to/Traversal-Toolkit
flask/bin/python app.py  # or: python3 app.py (if dependencies installed)
```

Then open: `http://127.0.0.1:5000`

## Setup (First Time)

```bash
cd /path/to/Traversal-Toolkit
python3 -m venv flask
flask/bin/pip install -r requirements.txt
flask/bin/python app.py
```

Or without venv:

```bash
pip install -r requirements.txt
python3 app.py
```

## Layout

- `app.py` – Flask app with `/api/analyze` endpoint
- `traversal_toolkit/` – Core logic:
  - `tree.py` – Binary tree building and traversals
  - `text_ops.py` – String operations (concatenation, length, case, find/replace)
  - `string_extra.py` – Extra string operations (prefix, suffix, reverse, palindrome)
  - `set_ops.py` – Set operations (union, intersection, difference)
  - `dfa.py` – DFA parser and simulator
- `templates/index.html` – Web UI with collapsible sidebar
- `static/app.js` – Frontend logic and page navigation
- `static/style.css` – Responsive styling
- `samples/examples.json` – Example trees
- `tests/test_core.py` – Unit tests

## Input Format

### Tree Traversals
- Format: space-separated or comma-separated values, or single string with each char as a node
- Examples:
  - `A B D E C F` (space-separated)
  - `A,B,C` (comma-separated)
  - `ABCDEF` (each char is a node)
- Rule: provide inorder + (preorder OR postorder). All node values must be unique.

### Sets
- Format: space-separated or comma-separated values
- Example: `A B C` or `1,2,3`

### DFA Definition
```
start: q0
accept: q0 q1
q0,a,q1
q1,b,q0
q0,*,q0
```
- `start:` – starting state
- `accept:` – accepting states (comma-separated)
- State transitions: `from_state,symbol,to_state` (use `*` for any symbol)

## Tests

```bash
flask/bin/python -m pytest tests/
```

## UI Features

- **Collapsible Sidebar** – Click ☰ to collapse/expand navigation
- **Page-based Navigation** – Separate pages for Binary Tree, Text Operations, Sets, DFA
- **Responsive Design** – Adapts to desktop, tablet, and mobile
- **Centered Layouts** – Input forms and results centered on page
- **Live Analysis** – Instant results as you input data

## Example: Text Operations

1. Click "Text Operations" in sidebar
2. Enter: `race car`
3. Results show:
   - Text, Length, Reversed, **Palindrome: Yes** (spaces trimmed, case ignored)
   - Uppercase, Lowercase, etc.

## Example: Binary Tree

1. Click "Binary Tree" in sidebar
2. Load example or enter traversals
3. View tree diagram and properties
4. Analyze with string/set/DFA tools
