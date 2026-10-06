# Traversal Toolkit

Enter a preorder / inorder / postorder and the app builds the binary tree, then runs the
string-operator, set-operation and DFA lessons on it.

## Run
```
pip install -r requirements.txt
python app.py        # open http://127.0.0.1:5000
python -m pytest     # run the tests
```

## Layout
- `app.py` – Flask app (page + `/api/analyze`)
- `traversal_toolkit/` – lesson code: `tree.py`, `text_ops.py`, `set_ops.py`, `dfa.py`
- `templates/`, `static/` – web UI
- `samples/` – example inputs shown in the Examples dropdown
- `tests/` – pytest tests

Input rule: give the inorder plus a preorder or postorder (or all three).
