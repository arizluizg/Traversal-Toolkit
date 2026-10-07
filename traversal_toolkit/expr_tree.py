"""Expression tree lesson: infix -> tree -> prefix / infix / postfix."""
import re

PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
RIGHT = {"^"}  # right-associative


class Node:
    def __init__(self, v):
        self.v, self.l, self.r = v, None, None


def tokenize(text):
    toks = re.findall(r"[A-Za-z0-9_.]+|[-+*/^()]", text)
    if "".join(text.split()) != "".join(toks):
        raise ValueError("Unsupported character. Use letters/numbers and + - * / ^ ( )")
    if not toks:
        raise ValueError("Type an expression first, e.g. A+B/D-E")
    return toks


def to_postfix(toks):
    """Shunting-yard: respects precedence and parentheses."""
    out, ops = [], []
    for t in toks:
        if t == "(":
            ops.append(t)
        elif t == ")":
            while ops and ops[-1] != "(":
                out.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses.")
            ops.pop()
        elif t in PREC:
            while ops and ops[-1] != "(" and (
                    PREC[ops[-1]] > PREC[t] or (PREC[ops[-1]] == PREC[t] and t not in RIGHT)):
                out.append(ops.pop())
            ops.append(t)
        else:
            out.append(t)
    while ops:
        if ops[-1] == "(":
            raise ValueError("Mismatched parentheses.")
        out.append(ops.pop())
    return out


def build(postfix):
    st = []
    for t in postfix:
        n = Node(t)
        if t in PREC:
            if len(st) < 2:
                raise ValueError("An operator is missing an operand.")
            n.r, n.l = st.pop(), st.pop()
        st.append(n)
    if len(st) != 1:
        raise ValueError("An operand is missing an operator.")
    return st[0]


def parse(text):
    return build(to_postfix(tokenize(text)))


def prefix(n):  return [] if not n else [n.v] + prefix(n.l) + prefix(n.r)
def postfix(n): return [] if not n else postfix(n.l) + postfix(n.r) + [n.v]
def infix(n):   return n.v if not n.l else "(" + infix(n.l) + n.v + infix(n.r) + ")"


def to_dict(root):
    """Nested dict; 'x' is the inorder position (used to lay out the drawing)."""
    c = [0]

    def go(n):
        if not n:
            return None
        l = go(n.l)
        x = c[0]
        c[0] += 1
        return {"v": n.v, "x": x, "l": l, "r": go(n.r)}
    return go(root)


def register(app):
    """Adds POST /api/expression to a Flask app (one call from app.py)."""
    from flask import jsonify, request

    @app.post("/api/expression")
    def api_expression():
        try:
            root = parse(request.get_json(force=True).get("expr", ""))
            return jsonify(tree=to_dict(root), prefix=" ".join(prefix(root)),
                           infix=infix(root), postfix=" ".join(postfix(root)))
        except ValueError as e:
            return jsonify(error=str(e)), 400
