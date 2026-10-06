"""Set operations lesson."""
from .tree import inorder


def default_sets(root):
    """A = left subtree + root, B = right subtree + root."""
    return [root.v] + inorder(root.l), [root.v] + inorder(root.r)


def _fmt(s):
    return "{" + ", ".join(sorted(s)) + "}"


def set_ops(a, b):
    A, B = set(a), set(b)
    return [
        ("Set A", _fmt(A)), ("Set B", _fmt(B)),
        ("Union (A ∪ B)", _fmt(A | B)),
        ("Intersection (A ∩ B)", _fmt(A & B)),
        ("Difference (A − B)", _fmt(A - B)),
        ("Difference (B − A)", _fmt(B - A)),
        ("Symmetric difference (A Δ B)", _fmt(A ^ B)),
        ("A ⊆ B", A <= B), ("A ⊇ B", A >= B),
        ("Disjoint", A.isdisjoint(B)),
        ("|A| / |B|", f"{len(A)} / {len(B)}"),
    ]
