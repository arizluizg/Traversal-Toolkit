"""Binary tree lesson: build a tree from traversals and inspect it."""


class Node:
    def __init__(self, v):
        self.v, self.l, self.r = v, None, None


def tokens(text):
    """'A B C' / 'A,B,C' / 'ABC' -> ['A', 'B', 'C']"""
    t = text.replace(",", " ").split()
    return list(t[0]) if len(t) == 1 and len(t[0]) > 1 else t


def _from_pre(pre, ino):
    idx, it = {v: i for i, v in enumerate(ino)}, iter(pre)

    def go(lo, hi):
        if lo > hi:
            return None
        n = Node(next(it))
        m = idx[n.v]
        n.l = go(lo, m - 1)
        n.r = go(m + 1, hi)
        return n
    return go(0, len(ino) - 1)


def _from_post(post, ino):
    idx, it = {v: i for i, v in enumerate(ino)}, iter(reversed(post))

    def go(lo, hi):
        if lo > hi:
            return None
        n = Node(next(it))
        m = idx[n.v]
        n.r = go(m + 1, hi)  # reverse postorder: right subtree first
        n.l = go(lo, m - 1)
        return n
    return go(0, len(ino) - 1)


def preorder(n):  return [] if not n else [n.v] + preorder(n.l) + preorder(n.r)
def inorder(n):   return [] if not n else inorder(n.l) + [n.v] + inorder(n.r)
def postorder(n): return [] if not n else postorder(n.l) + postorder(n.r) + [n.v]
def height(n):    return 0 if not n else 1 + max(height(n.l), height(n.r))


def leaves(n):
    if not n:
        return []
    return [n.v] if not n.l and not n.r else leaves(n.l) + leaves(n.r)


def level_order(n):
    out, q = [], [n]
    while q:
        x = q.pop(0)
        if x:
            out.append(x.v)
            q += [x.l, x.r]
    return out


def build(pre, ino, post):
    """Inorder + (preorder or postorder) -> root Node. Raises ValueError on bad input."""
    if not ino:
        raise ValueError("Inorder is required (together with preorder or postorder).")
    if len(set(ino)) != len(ino):
        raise ValueError("Node values must be unique.")
    other = pre or post
    if not other:
        raise ValueError("Add a preorder or postorder as well.")
    if sorted(other) != sorted(ino):
        raise ValueError("Traversals must contain the same nodes.")
    root = _from_pre(pre, ino) if pre else _from_post(post, ino)
    for given, calc in ((pre, preorder(root)), (ino, inorder(root)), (post, postorder(root))):
        if given and given != calc:
            raise ValueError("These traversals don't describe the same tree.")
    return root


def to_dict(n):
    return None if not n else {"v": n.v, "l": to_dict(n.l), "r": to_dict(n.r)}


def summary(root):
    ino = inorder(root)
    try:
        keys = [float(v) for v in ino]
    except ValueError:
        keys = ino
    return [
        ("Root", root.v), ("Nodes", len(ino)), ("Height (levels)", height(root)),
        ("Leaves", " ".join(leaves(root))), ("Level-order", " ".join(level_order(root))),
        ("Preorder", " ".join(preorder(root))), ("Inorder", " ".join(ino)),
        ("Postorder", " ".join(postorder(root))), ("Is a BST", keys == sorted(keys)),
    ]
