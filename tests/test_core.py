import pytest

from traversal_toolkit import dfa, set_ops, string_extra, text_ops, tree

PRE, INO, POST = ["A", "B", "D", "E", "C", "F"], ["D", "B", "E", "A", "F", "C"], ["D", "E", "B", "F", "C", "A"]


def test_build_from_pre_in():
    r = tree.build(PRE, INO, [])
    assert tree.postorder(r) == POST and tree.height(r) == 3


def test_build_from_post_in():
    assert tree.preorder(tree.build([], INO, POST)) == PRE


def test_mismatched_traversals_rejected():
    with pytest.raises(ValueError):
        tree.build(PRE, INO, list(reversed(POST)))


def test_needs_inorder():
    with pytest.raises(ValueError):
        tree.build(PRE, [], POST)


def test_string_ops():
    rows = dict(text_ops.string_ops("ABC", "XY"))
    assert rows["Concatenation (A + B)"] == "ABCXY" and rows["Reverse of A"] == "CBA"


def test_set_ops():
    rows = dict(set_ops.set_ops(["A", "B"], ["B", "C"]))
    assert rows["Intersection (A ∩ B)"] == "{B}" and rows["Symmetric difference (A Δ B)"] == "{A, C}"


def test_dfa_even_length():
    assert dfa.run(dfa.DEFAULT, "ABCD")["accepted"] is True
    assert dfa.run(dfa.DEFAULT, "ABC")["accepted"] is False


def test_string_extra_ops():
    rows = dict(string_extra.string_extra_ops("race car", "ABC"))
    assert rows["Prefix of A"] == "rac"
    assert rows["Suffix of A"] == "car"
    assert rows["Reverse of A"] == "rac ecar"
    assert rows["A is a palindrome (trim spaces, ignore case)"] is True
    assert rows["Reverse of B"] == "CBA"
    assert rows["B is a palindrome (trim spaces, ignore case)"] is False
